# -*- coding: utf-8 -*-
import itertools
import logging
from spine import Spine
logger = logging.getLogger(__name__)

class ContactManager(object):
    """
    オブジェクトを登録し、オブジェクト間の接触判定を管理する。
    全オブジェクトを操作する実装。必要なら四分木
    """
    def __init__(self):
        self.objects = []
        pass

    def register(self, x: Spine):
        """オブジェクトの登録
        """
        self.objects.append(x)
        return

    def contact_pairs(self):
        """
        接触しているオブジェクトのペアを返すジェネレータ
        """
        N = len(self.objects)
        for obj1, obj2 in itertools.combinations(self.objects, 2):
            if obj1.is_overlapped_with_spine(obj2):
                yield (obj1, obj2)
        return
