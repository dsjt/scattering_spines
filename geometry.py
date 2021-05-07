# -*- coding: utf-8 -*-
from __future__ import annotations
import math
import logging

EPS = 1.0e-6
INF = float("infinity")
logger = logging.getLogger(__name__)

class Point(object):
    """
    座標を表すクラス。
    加算、減算、乗算、絶対値、内積、外積、行列式を扱える。
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

    def __repr__(self):
        return "<Point x={}, y={}>".format(self.x, self.y)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return tuple(self) < tuple(other)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y+other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if type(other) is Point:
            return Point(self.x * other.x, self.y*other.y)
        else:
            return Point(self.x * other, self.y*other)

    def __truediv__(self, other):
        if type(other) is Point:
            return Point(self.x/other.x, self.y/other.y)
        else:
            return Point(self.x/other, self.y/other)

    def __floordiv__(self, other):
        return Point(self.x//other.x, self.y//other.y)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

    def __iter__(self):
        yield self.x
        yield self.y

    def dot(self, other):
        p = self*other
        return p.x+p.y

    def inner(self, other):
        return self.dot(other)

    def rotate(self, degree):
        x = self.x*math.cos(degree)-self.y*math.sin(degree)
        y = self.x*math.sin(degree)+self.y*math.cos(degree)
        return Point(x, y)

    def rotate90(self):
        return Point(-self.y, self.x)

    def det(self, other):
        return self.inner(-other.rotate90())

    def outer(self, other):
        return self.det(other)

    def degree(self):
        return math.degrees(math.atan2(self.y, self.x))

class Line(object):
    """直線を表すクラス
    """
    _CROSS = 1
    _PARALLEL = -1
    _SAME = 0

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        pass

    def relation(self, other: Line):
        """
        ニ直線の関係性を求める。
        """
        status = (self.p1-self.p2).det(other.p1-other.p2)
        if not (-EPS < status < EPS):
            return self._CROSS        # 交差する
        status = (self.p1-self.p2).det(other.p1-self.p2)
        if not (-EPS < status < EPS):
            return self._PARALLEL       # 平行である
        return self._SAME            # 同一直線である

    def cross(self, other: Line):
        """
        二直線の交点を求める
        """
        status = self.relation(other)
        if status == self._CROSS:
            # 交差点を求める
            numer = (other.p1-self.p1).det(other.p2-other.p1)
            denom = (self.p2-self.p1).det(other.p2-other.p1)
            return self.p1 + (self.p2-self.p1)*(numer/denom)
        elif status == self._PARALLEL:
            return None
        else:
            return INF

    def dist(self, point: Point):
        """
        点と直線の距離を求める。
        """
        return abs((point-self.p1).det(self.p2-self.p1) / abs(self.p2-self.p1))

    def __repr__(self):
        return f"<Line defined by ({self.p1}, {self.p2})>"


class Segment(Line):
    """線分を表すクラス
    """
    _NOTCROSS = -2
    def relation(self, other):
        status1 = iSP(self.p1, self.p2, other.p1) * \
            iSP(self.p1, self.p2, other.p2) <= 0
        status2 = iSP(other.p1, other.p2, self.p1) * \
            iSP(other.p1, other.p2, self.p2) <= 0
        if status1 and status2:
            # 節点を持つ
            return super().relation(other)
        else:
            return self._NOTCROSS

    def dist(self, point):
        if (self.p2-self.p1).dot(point-self.p1) < -EPS:
            return abs(point-self.p1)
        elif (self.p1-self.p2).dot(point-self.p2) < -EPS:
            return abs(point-self.p2)
        else:
            return super().dist(point)

def iSP(a, b, c):
    """
    反時計回りに曲がる: +1
    時計回りに曲がる: -1
    直線に並び、c-a-bの順 -2
    直線に並び、a-b-cの順 +2
    直線に並び、a-c-bの順 0
    """
    status = (b-a).det(c-a)
    if status < -EPS:
        return -1
    elif status < EPS:
        if (b-a).dot(c-a) < 0:
            return -2
        elif (a-b).dot(c-b) < 0:
            return 2
        else:
            return 0
    else:
        return 1
