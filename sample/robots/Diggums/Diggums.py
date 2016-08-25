from sample.framework.advExploration import AdvExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors

""" Simple Q-learning agent
    States: (y,x,o) | Actions: Forward = 0 , Right = 1, Backwards = 2, Left = 3
"""


class Diggums(BasicRobot, BasicMovementAndSensors, BasicQlearning, AdvExploration):
    def __init__(self, id, maze, name, sharedQmatrix):
        BasicMovementAndSensors.__init__(self, self, maze)
        AdvExploration.__init__(self, self)
        BasicQlearning.__init__(self, self)
        BasicRobot.__init__(self, self, id, name, maze)
        self.Q = sharedQmatrix

    def getExplorationRate(self):
        return 1/(self.learningTrial/2 + 1)
