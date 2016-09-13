from abc import ABCMeta, abstractmethod
import numpy

class BaseQLearning(object):
    __metaclass__ = ABCMeta

    mas = None
    Q = None
    Qnew = None
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

    def computeWeight(self, basis):
        return 1

    @abstractmethod
    def computeExpertness(self):
        pass

    def learnFromRobots(self, robotList):
        self.Qnew = numpy.zeros_like(self.Q)
        for robot in robotList:
            self.Qnew += self.computeWeight(robot)*robot.Q

    def learnNewQ(self):
        self.Q[:, :] = self.Qnew[:, :]
