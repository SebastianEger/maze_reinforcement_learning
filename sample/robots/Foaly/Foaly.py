import math

from sample.framework.basicRobot import BasicRobot
from sample.framework.advMovementAndSensors import AdvMovementAndSensors
from folQLearning import FolQLearning
from sample.framework.advExploration import AdvExploration


# Expertness: Inverse Distance to Goal (IDG)
# Weight Calculation: Learning From All
class Foaly(BasicRobot):
    def __init__(self, id, maze, name):
        ms = AdvMovementAndSensors(maze)
        e = AdvExploration(ms, maze)
        q = FolQLearning(ms, maze)
        BasicRobot.__init__(self, id, maze, name, ms, e, q)

    def set_q_shared(self, qshared):
        self.Q = qshared
