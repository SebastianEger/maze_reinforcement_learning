from sample.framework.basicExploration import BasicExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors


class Butler(BasicRobot, BasicExploration, BasicMovementAndSensors, BasicQlearning):
    def __init__(self, id, maze, name):
        BasicMovementAndSensors.__init__(self, self, maze)
        BasicExploration.__init__(self, self)
        BasicQlearning.__init__(self, self, maze)
        BasicRobot.__init__(self, self, id, name, maze)

    def set_q_shared(self, qmatrix):
        self.Q = qmatrix