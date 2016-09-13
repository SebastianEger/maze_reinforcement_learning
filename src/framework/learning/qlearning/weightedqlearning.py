import numpy

from src.framework.learning.qlearning.basicQlearning import BasicQlearning


class WeightedQlearning(BasicQlearning):
    def __init__(self, basis):
        BasicQlearning.__init__(self, basis)
        self.Qnew = numpy.zeros(numpy.shape(self.Q))
        self.cooperation_time = 50
        self.cooperation_counter = 0

    def computeWeight(self, basis):
        return 0.5
