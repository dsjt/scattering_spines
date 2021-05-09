# -*- coding: utf-8 -*-
# リポジトリ固有な、ある程度汎用な関数
import logging
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from spine import Spine
from geometry import Point
from utils import AutoSaveFigure

logger = logging.getLogger(__name__)
random.seed(0)

def random_spines(H, W, L, N) -> list[Spine]:
    """
    交差を許してランダムに針の位置を決める。
    """
    return [random_spine(H, W, L, identifier=f"{i}") for i in range(N)]

def random_spine(H, W, L, identifier=None) -> Spine:
    """
    ランダムに針の位置を決める
    """
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    center = Point(x, y)
    theta = random.uniform(0, math.pi)
    logger.debug(f"random_spines {identifier=} {x=:.3f}, {y=:.3f}, {theta=:.3f}")
    return Spine(center, theta, L, identifier=identifier)


def display(h, w, spines: list[Spine], fn="tmp.png"):
    """
    針の状態を一枚の画像で保存する
    """
    with AutoSaveFigure(fn=fn) as fig:
        ax = fig.add_subplot(1, 1, 1, aspect="equal")
        spines_plot(h, w, spines, ax)
    return

def spines_plot(h, w, spines: list[Spine], ax):
    """
    針をプロットする
    """
    for spine in spines:
        spine.plot(ax, color="black")

    # 外枠
    r = matplotlib.patches.Rectangle(xy=(0, 0), width=w, height=h,
                                     ec='#000000', linestyle=":", fill=False)
    ax.add_patch(r)

    # 表示範囲
    rep_spine = spines[0]
    ax.set_xlim(-rep_spine.l/2, w+rep_spine.l/2)
    ax.set_ylim(-rep_spine.l/2, h+rep_spine.l/2)
    return ax
