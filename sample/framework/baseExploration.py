from abc import ABCMeta, abstractmethod


class BaseExploration(object):
    __metaclass__ = ABCMeta

    def __init__(self, basis):
        self.basis = basis
        self.exploration_rate = None

    @abstractmethod
    def explore(self, actionList):
        pass
