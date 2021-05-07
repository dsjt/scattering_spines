# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class myFigure(matplotlib.figure.Figure):
    def __init__(self, fn, **kwargs):
        self.fn = fn
        super().__init__(**kwargs)
        pass

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        plt.tight_layout()
        self.savefig(self.fn)
        plt.close(self)
        if exception_type is not None:
            print("Error has occurred.")
            print(exception_type, exception_value, traceback)
        return
