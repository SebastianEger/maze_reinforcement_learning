import math

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors
from sample.framework.advExploration import AdvExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot


# Expertness: Inverse Distance to Goal (IDG)
# Weight Calculation: Learning From All
class Foaly(BasicRobot, BasicMovementAndSensors, AdvExploration, BasicQlearning):

    def __init__(self, id, maze, name):
        BasicMovementAndSensors.__init__(self, self, maze)
        AdvExploration.__init__(self, self, maze)
        BasicQlearning.__init__(self, self, maze)
        BasicRobot.__init__(self,self, id, name, maze)

    def set_q_shared(self, qshared):
        self.Q = qshared

    def computeExpertness(self):
        return self.expertness+self.lastReward

    def computeWeight(self):
        expertness_sum = 0
        for robot in self.robot_list:
            expertness_sum += robot.expertness

        if expertness_sum == 0:
            return 1

        return self.expertness/expertness_sum
