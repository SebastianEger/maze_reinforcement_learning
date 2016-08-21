from digExploration import DigExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors

""" Simple Q-learning agent
    States: (y,x,o) | Actions: Forward = 0 , Right = 1, Backwards = 2, Left = 3
"""


class Diggums(BasicRobot):
    def __init__(self, id, maze, name):
        self.ms = BasicMovementAndSensors(self, maze)
        self.e = DigExploration(self, maze)
        self.q = BasicQlearning(self, maze)

        BasicRobot.__init__(self, self, id, name, maze)

    def set_q_shared(self, qmatrix):
        self.q.Q = qmatrix
