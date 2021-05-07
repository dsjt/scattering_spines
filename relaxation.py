# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
import geometry
from collections import defaultdict
from spine import Spine
from utils import sign
from general import random_spines, display, spines_plot
from geometry import Point, iSP
from contact_manager import ContactManager

logger = logging.getLogger(__name__)

INF = float("infinity")

def relaxation(H, W, L, N) -> list[Spine]:
    """自然な接触を考慮することで平衡状態を目指すアプローチで針の位置・向きを求める。

    1. 貫入を許してランダムに針を生成
    2. 針同士が接触していなければ終了。接触している場合は、接触に応じて位置・角
    度を更新する。手順２の最初に戻る

    問題点：
    - 局所解に陥った場合に抜け出す手段がないため、最初からやり直す必要がある。
    - 収束までに要する時間を見積もる方法がわからない
    """
    # 更新量を制御するグローバルパラメータ
    pos_epsilon = 0.1
    angle_epsilon = 0.1
    # 最大反復回数を制御するグローバルパラメータ
    max_iteration = 50

    # ランダムな生成
    spines = random_spines(H, W, L, N)
    cm = ContactManager()
    for spine in spines:
        cm.register(spine)

    fig = plt.figure(figsize=(8, 6))
    frames = []
    cp = list(cm.contact_pairs())
    for epoch in range(max_iteration):
        logger.debug(f"{epoch=}")
        ax = fig.add_subplot(1, 1, 1, aspect="equal")
        spines_plot(H, W, spines, ax)
        frames.append(ax.get_children())

        if len(cp) == 0:
            logger.debug("iteration end")
            break

        # obj1, obj2の重なりによる更新量を求める
        deltas_dict = defaultdict(lambda: Spine(Point(0, 0), 0, 0))
        for obj1, obj2 in cp:
            update = calc_delta(obj1, obj2)
            for key, val in update.items():
                deltas_dict[key] += val

        if logger.level == logging.DEBUG:
            for key, value in deltas_dict.items():
                logger.debug(f"update {key.identifier=}, {value=}")

        # 更新量にしたがって更新する。
        apply_update(deltas_dict, pos_epsilon, angle_epsilon)

        # 接触情報を更新
        cp = list(cm.contact_pairs())

    ani = animation.ArtistAnimation(fig, frames, interval=100)
    ani.save("relaxation.gif", writer="imagemagick")
    return spines


def calc_delta(obj1: Spine, obj2: Spine):
    """
    重なりのある二つのオブジェクトに関し、更新量を計算する。
    現状、Spineであることを前提とする。

    位置はお互いに遠ざかる方向に更新する。境界に当たる場合は滑るように移動する。
    角度は、互いの針の中心位置を見て、反発するように移動する。
    """
    update = {}
    # 角度
    # 交点を求める
    cross_point = obj1.cross(obj2)
    logger.debug(f"{type(cross_point)} {Point}")
    if (type(cross_point) is not Point):
        # 交差する２点を入力しているはずである。警告し更新なしとする。
        logger.warning(f"needless update ({obj1=}, {obj2=})")
        return update

    # 交点位置
    status = iSP(obj1.center, cross_point, obj2.center)
    if status == 1:             # 半時計回りの配置なので角度変化は時計回り
        delta_theta1 = -1
        delta_theta2 = +1       # 必ず逆方向に回転する
    elif status == -1:
        delta_theta1 = +1
        delta_theta2 = -1
    else:                       # 直線上に並ぶ場合は角度変化無しとする
        delta_theta1 = 0
        delta_theta2 = 0

    # 位置
    delta_pos1 = obj1.center-obj2.center
    delta_pos2 = obj2.center-obj1.center
    # 位置が完全に一致した場合はどうにかすべきだがめったにない

    logger.debug(f"{delta_theta1=}, {delta_theta2=}")
    update[obj1] = Spine(delta_pos1, delta_theta1, l=0)
    update[obj2] = Spine(delta_pos2, delta_theta2, l=0)
    return update

def apply_update(update: dict, pos_epsilon, angle_epsilon):
    """
    updateはSpineオブジェクトをキーとして、更新量・方向をSpine型で記述したものを値としているdict
    """
    for obj, delta in update.items():
        # 位置の更新
        # deltaから方向だけ取り出して、pos_epsilonにしたがって更新する
        # 領域外に飛び出すことは気にしない
        obj.update(
            center=obj.center + (delta.center / abs(delta.center))*pos_epsilon,
            theta=obj.theta + sign(delta.theta)*angle_epsilon
        )
    return
