from sample.framework.basicExploration import BasicExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors


# Shared Q matrix: No
# Expertness: None
# Weighting: None


class Artemis(BasicRobot):
    def __init__(self, id, maze, name):
        self.ms = BasicMovementAndSensors(self, maze)
        self.e = BasicExploration(self)
        self.q = BasicQlearning(self, maze)

        BasicRobot.__init__(self, self, id, name, maze)