from sample.framework.basicExploration import BasicExploration
from sample.framework.basicQlearning import BasicQlearning
from sample.framework.basicRobot import BasicRobot

from sample.framework.basicMovementAndSensors import BasicMovementAndSensors


class Butler(BasicRobot):
    def __init__(self,id,maze,name):
        self.ms = BasicMovementAndSensors(self,maze)
        self.e = BasicExploration(self)
        self.q = BasicQlearning(self, maze)

        BasicRobot.__init__(self, self, id, name, maze)

    def set_q_shared(self, qmatrix):
        self.q.Q = qmatrix