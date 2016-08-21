from abc import ABCMeta, abstractmethod


class BaseRobot(object):
    __metaclass__ = ABCMeta

    def __init__(self, basis, id, name):
        self.basis = basis

        self.id = id
        self.name = name
        self.info = 'No information yet'

        self.current_position = None  # current_position, y-axis, x-axis, orientation [cm]
        self.goal_position = None

    @abstractmethod
    def makeStep(self):
        pass

    @abstractmethod
    def reset(self, start, goal):
        pass
