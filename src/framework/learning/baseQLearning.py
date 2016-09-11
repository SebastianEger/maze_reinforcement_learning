from abc import ABCMeta, abstractmethod


class BaseQLearning(object):
    __metaclass__ = ABCMeta

    mas = None
    expertness = 0

    def __init__(self, mas):
        self.mas = mas
        self.learn_rate = 0.2
        self.discount = 0.9

        ''' Rewards '''
        self.reward_wall = -10
        self.reward_step = -0.01
        self.reward_goal = 100
        self.reward_robot = -0.01

    @abstractmethod
    def updateQ(self, action, state, next_state, reward):
        pass

    @abstractmethod
    def getActionList(self, state):
        pass

    @abstractmethod
    def computeWeight(self, basis):
        pass

    @abstractmethod
    def computeExpertness(self):
        pass

    @abstractmethod
    def learnFromRobots(self, basis):
        pass
