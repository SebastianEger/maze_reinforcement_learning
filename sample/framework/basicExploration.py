from sample.framework.baseExploration import BaseExploration
import numpy


class BasicExploration(BaseExploration):
    def __init__(self, basis):
        BaseExploration.__init__(self, basis)

    def explore(self, actionList):
        if numpy.random.random_sample(1) < self.getExplorationRate():
            actionList = []
            for action in range(self.basis.ms.nActions):
                actionList.append(action)
            numpy.random.shuffle(actionList)
            return actionList
        else:
            return actionList

    def getExplorationRate(self):
        return self.exploration_rate