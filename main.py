# -*- coding: utf-8 -*-
# 平面上に針を配置する。針は互いに重ならないようにする。
# できるだけばらばらな方向を向いた針を得たい。
import matplotlib
import matplotlib.pyplot as plt
import logging
import math
import random
from spine import Spine
from utils import myFigure
from geometry import Point
from contact_manager import ContactManager

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# random.seed(0)

def main():
    # 平面のサイズ
    H, W = 10, 10
    # 針一本の長さ
    L = 3
    # 針の本数
    N = 10

    spines = random_spines(H, W, L, N)
    cm = ContactManager()
    for spine in spines:
        cm.register(spine)

    for obj1, obj2 in cm.contact_pairs():
        logger.debug(f"overlapping {obj1}, {obj2}")

    display(H, W, spines)
    return

def random_spines(H, W, L, N) -> list[Spine]:
    """
    交差を許してランダムに針の位置を決める。
    """
    ret = []
    for i in range(N):
        x = random.uniform(0, W)
        y = random.uniform(0, H)
        center = Point(x, y)
        theta = random.uniform(0, math.pi)
        logger.debug(f"random_spines {i}th {x=:.3f}, {y=:.3f}, {theta=:.3f}")
        ret.append(Spine(center, theta, L, identifier=f"{i}"))
    return ret


def display(h, w, spines: list[Spine], fn="tmp.png"):
    with myFigure(fn=fn) as fig:
        ax = fig.add_subplot(1, 1, 1, aspect="equal")
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
    return


if __name__ == '__main__':
    main()
