from abc import ABCMeta, abstractmethod


class BaseMovementAndSensors(object):
    __metaclass__ = ABCMeta

    def __init__(self, basis):
        self.basis = basis
        self.nActions = None
        self.nStates = None

    @abstractmethod
    def getNextPos(self, current_position, action):
        pass

    @abstractmethod
    def checkAction(self, current_position, action):
        pass

    @abstractmethod
    def getState(self, current_position):
        pass

    @abstractmethod
    def simSensors(self, current_position, maze):
        pass