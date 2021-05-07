# -*- coding: utf-8 -*-
import numpy as np
import math
import logging
import matplotlib
from geometry import *

logger = logging.getLogger(__name__)

class Spine(Segment):
    """
    針を表すクラス。
    """
    def __init__(self, center: Point, theta, l, identifier=None):
        # 中心座標
        self.center = center
        # 横軸となす角度 0からπ
        self.theta = theta
        # 針の長さ
        self.l = l
        # 識別
        self.identifier = identifier

        # 上位クラスへ
        dp = Point(math.cos(theta)*l/2, math.sin(theta)*l/2)
        super().__init__(self.center+dp, self.center-dp)
        pass

    def update(self, center: Point = None, theta=None, l=None):
        """
        針の位置、角度、長さを更新する。
        """
        if center is not None:
            self.center = center
        if theta is not None:
            self.theta = theta
        if l is not None:
            self.l = l

        dp = Point(math.cos(self.theta)*self.l/2,
                   math.sin(self.theta)*self.l/2)
        self.p1 = self.center+dp
        self.p2 = self.center-dp
        return

    def plot(self, ax, **kwargs):
        ax.plot(self.center.x, self.center.y, marker=".", **kwargs)
        if self.identifier is not None:
            ax.annotate(self.identifier, xy=(self.center.x, self.center.y))
        x = [self.p1.x, self.p2.x]
        y = [self.p1.y, self.p2.y]
        ax.plot(x, y, **kwargs)
        return

    def is_overlapped_with_spine(self, other: Segment) -> bool:
        if self.relation(other) == Segment._NOTCROSS:
            return False
        else:
            return True

    def __repr__(self):
        return f"<Spine {self.identifier=}, ({self.center}, {self.theta=:.3f}, {self.l=:.3f})>"

    def __iadd__(self, other):
        self.update(self.center+other.center,
                    self.theta+other.theta,
                    self.l + other.l)
        return self
