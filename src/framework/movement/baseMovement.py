from abc import ABCMeta, abstractmethod


class BaseMovementAndSensors(object):
    __metaclass__ = ABCMeta

    nStates = None
    nActions = None

    @abstractmethod
    def getNextPos(self, current_position, action):
        pass

    @abstractmethod
    def checkAction(self, current_position, action, next_position, sensors):
        pass

    @abstractmethod
    def getState(self, position):
        pass


