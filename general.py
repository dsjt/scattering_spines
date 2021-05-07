# -*- coding: utf-8 -*-
# リポジトリ固有な、ある程度汎用な関数
import logging
import math
import random
from spine import Spine
from geometry import Point

logger = logging.getLogger(__name__)
random.seed(0)

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
