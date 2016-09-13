import numpy

from src.framework.exploration.baseExploration import BaseExploration


class RandomExploration(BaseExploration):
    def __init__(self):
        pass

    def getActionList(self, basis, actionList):
        actionList = []
        for action in range(basis.mov.nActions):
            actionList.append(action)
        numpy.random.shuffle(actionList)
        return actionList

    def getExplorationRate(self):
        return self.explorationRate
