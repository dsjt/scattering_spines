# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
import random
import copy
from collections import defaultdict
import math

import geometry
from spine import Spine
from utils import sign, AutoSaveAnimation
from general import random_spines, random_spine, display, spines_plot
from geometry import Point, iSP
from contact_manager import ContactManager

logger = logging.getLogger(__name__)

INF = float("infinity")
ALPHA = 0.1
EPS = 1.0e-6

def anealing(H, W, L, N) -> list[Spine]:
    """
    アニーリングによってエネルギー０を目指すアプローチで針の位置・向きを求める。
    """
    # 最大反復回数を制御するグローバルパラメータ
    max_iteration = 3000

    # ランダムな生成
    spines = random_spines(H, W, L, N)
    cm = ContactManager()
    for spine in spines:
        cm.register(spine)

    with AutoSaveAnimation("anealing.gif", figsize=(8, 6)) as ani:
        ax = ani.add_subplot(1, 1, 1, aspect="equal")
        ani.frames.append(spines_plot(H, W, spines, ax).get_children())

        e = eval(H, W, spines, cm)

        best_e = e
        best_state = copy.deepcopy(spines)

        for epoch in range(max_iteration):
            logger.debug(f"{epoch=}/{max_iteration}")

            cp = list(cm.contact_pairs())
            if len(cp) == 0:
                logger.debug("iteration end")
                break

            # ランダムに一つのspineを選択し、新しい位置を決める。
            i = random.randint(0, N-1)
            spine = random_spine(H, W, L, identifier=f"{i}")
            orig_spine = cm.objects[i]  # FIX

            # 置き換わった場合の評価値
            next_e = e - \
                len([s for s in cm.overlapped_objects_with_known(orig_spine)]) \
                + len([s for s in cm.overlapped_objects_with_new(spine)
                       if s != orig_spine])

            if next_e < best_e:
                best_e = next_e
                # ここ、next_stateを使うべきだができないため
                best_state = copy.deepcopy(spines)

            prob = probability(e, next_e, temperature(epoch/max_iteration))
            if random.uniform(0, 1) <= prob:
                # 置き換える
                orig_spine.update(spine.center, spine.theta, spine.l)
                e = next_e
                cm.update(orig_spine)
                if e < EPS:
                    break

            if logger.level == logging.DEBUG:
                logger.debug(f"{e=:.3f}")

            # 描画
            if epoch % (max_iteration//20) == 0:
                ax = ani.add_subplot(1, 1, 1, aspect="equal")
                ani.frames.append(spines_plot(H, W, spines, ax).get_children())

            # 接触情報を更新
            cp = list(cm.contact_pairs())

    return spines

def eval(H, W, state: list[Spine], cm):
    """
    針の状態に対する評価値
    """
    return len(list(cm.contact_pairs()))

def temperature(r):
    """
    使用する温度。
    """
    return pow(ALPHA, r)

def probability(e1, e2, t):
    if e1 >= e2:
        return 1
    else:
        return pow(math.e, (e1-e2)/t)
