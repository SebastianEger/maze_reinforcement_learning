from sample.framework.advExploration import AdvExploration


class DigExploration(AdvExploration):
    def __init__(self, ms, maze):
        AdvExploration.__init__(self, ms, maze)

    def getExplorationRate(self):
        return 1/(self.basis.learningTrial/2 + 1)