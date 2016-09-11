from abc import ABCMeta, abstractmethod


class BaseExploration(object):
    __metaclass__ = ABCMeta

    explorationRate = 0

    @abstractmethod
    def getActionList(self, basis, actionList):
        pass
