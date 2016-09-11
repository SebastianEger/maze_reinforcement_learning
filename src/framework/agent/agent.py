from src.framework.sensor.baseSensor import BaseSensor
from abc import ABCMeta, abstractmethod


class Agent(object):
    __metaclass__ = ABCMeta
    ''' Modules '''
    mov = None  # Movement module
    qrl = None  # Q Reinforcement Learning module
    exp = None  # Exploration module
    sen = None  # Sensor module

    def __init__(self, info, modules):
        self.info = info

        self.sen = BaseSensor()
        self.mov = modules[0]
        self.qrl = modules[1]
        self.exp = modules[2]

        self.current_position = None  # current_position, y-axis, x-axis, orientation [cm]
        self.goal_position = None

    @abstractmethod
    def makeStep(self):
        pass

    @abstractmethod
    def reset(self, start, goal):
        pass
