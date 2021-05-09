# -*- coding: utf-8 -*-
import itertools
import logging
from spine import Spine
from collections import defaultdict

logger = logging.getLogger(__name__)

class ContactManager(object):
    """
    オブジェクトを登録し、オブジェクト間の接触判定を管理する。
    全オブジェクトを操作する実装。必要なら四分木
    """
    def __init__(self):
        self.objects = []       # オブジェクトのリスト
        self.mapping = {}       # オブジェクトから配列の添字を得るマッピング
        self.E = []
        pass

    def register(self, x: Spine):
        """オブジェクトの登録
        """
        self.objects.append(x)
        self.E.append([])
        N = len(self.objects)
        self.mapping[x] = N-1

        # これまでのオブジェクトとの接触を反映する
        # O(N)
        for other in self.overlapped_objects_with_new(x):
            i = self.mapping[other]
            self.E[i].append(N-1)
            self.E[N-1].append(i)
        return

    def overlapped_objects_with_new(self, x):
        """
        未登録のオブジェクトxと重なっているオブジェクトを返す。O(N)。
        """
        ret = []
        for other in self.objects:
            if x.is_overlapped_with_spine(other):
                ret.append(other)
        return ret

    def overlapped_objects_with_known(self, x):
        """登録済みのオブジェクトxと重なっているオブジェクトを返す。O(N)
        """
        ret = self.overlapped_objects_with_new(x)
        return [r for r in ret if r != x]

    def update(self, x):
        """
        登録したオブジェクトの接触情報を更新する。
        """
        i = self.mapping[x]
        # 既存の情報を削除する
        for j in self.E[i]:
            self.E[j].remove(i)
        self.E[i] = []

        # 新しい情報を反映する
        for other in self.overlapped_objects_with_known(x):
            j = self.mapping[other]
            self.E[i].append(j)
            self.E[j].append(i)
        return

    def contact_pairs(self):
        """
        接触しているオブジェクトのペアを返すジェネレータ
        """
        N = len(self.objects)
        for i in range(N):
            for j in self.E[i]:
                if i < j:
                    yield (self.objects[i], self.objects[j])
        return
