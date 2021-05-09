# -*- coding: utf-8 -*-
# 平面上に針を配置する。針は互いに重ならないようにする。
# できるだけばらばらな方向を向いた針を得たい。
import matplotlib
import matplotlib.pyplot as plt
import logging
import math
from spine import Spine
from general import random_spines, display
from contact_manager import ContactManager
from relaxation import relaxation
from anealing import anealing

logging.basicConfig(level=logging.WARNING)
logger_levels = {
    "main": logging.DEBUG,
    "relaxation": logging.DEBUG,
    "anealing": logging.DEBUG
}
for mn, level in logger_levels.items():
    logging.getLogger(mn).setLevel(level)

logger = logging.getLogger(__name__)

def main():
    # 平面のサイズ
    H, W = 10, 10
    # 針一本の長さ
    L = 3
    # 針の本数
    N = 60

    # spines = relaxation(H, W, L, N)
    spines = anealing(H, W, L, N)
    display(H, W, spines, fn="output.png")
    return


if __name__ == '__main__':
    main()
