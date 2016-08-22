from sample.framework.basicRobot import BasicRobot
from sample.framework.basicMovementAndSensors import BasicMovementAndSensors
from sample.framework.advExploration import AdvExploration
from sample.framework.advQLearning import AdvQLearning


class Holly(BasicRobot, BasicMovementAndSensors, AdvExploration, AdvQLearning):
    def __init__(self, id, maze, name):
        BasicMovementAndSensors.__init__(self, self, maze)
        AdvExploration.__init__(self, self, maze)
        AdvQLearning.__init__(self, self, maze)
        BasicRobot.__init__(self, self, id, name, maze)
