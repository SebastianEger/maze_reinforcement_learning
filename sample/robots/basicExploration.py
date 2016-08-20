import numpy
from basicMovementAndSensors import BasicMovementAndSensors


class BasicExploration:
    def __init__(self):
        self.exploration_rate = 0

    def explore(self, numberOfActions, actionList):
        if numpy.random.random_sample(1) < self.getExplorationRate():
            actionList = []
            for action in range(numberOfActions):
                actionList.append(action)
            numpy.random.shuffle(actionList)
            return actionList
        else:
            return actionList

    def getExplorationRate(self):
        return self.exploration_rate