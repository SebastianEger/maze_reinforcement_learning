from sample.framework.basicExploration import BasicExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors


# Shared Q matrix: No
# Expertness: None
# Weighting: None


class Artemis(BasicRobot, BasicMovementAndSensors, BasicExploration, BasicQlearning):
    def __init__(self, id, maze, name):
        BasicMovementAndSensors.__init__(self, self, maze)
        BasicExploration.__init__(self, self)
        BasicQlearning.__init__(self, self)
        BasicRobot.__init__(self, self, id, name, maze)

    def computeWeight(self, robot):
        a = 1/float(len(self.robot_list))
        return a
