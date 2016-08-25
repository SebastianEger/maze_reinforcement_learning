from basicQlearning import BasicQlearning
import numpy


class AdvQLearning(BasicQlearning):
    def __init__(self, basis, maze):
        BasicQlearning.__init__(self, basis, maze)
        self.Qnew = numpy.zeros(numpy.shape(self.Q))
        self.cooperation_time = 50
        self.cooperation_counter = 0
        self.learnQnew = False

    def updateQ(self, action, state, next_state, reward): # Main update function
        self.lastReward = reward
        estimate = max(self.Q[next_state, :])
        self.Q[state, action] += self.learn_rate*(reward + self.discount*estimate - self.Q[state, action])

    def computeWeight(self):
        return 0.5

    def learnedFromRobots(self):
        self.cooperation_counter += 1
        if self.learnQnew:
            self.Q[:,:] = self.Qnew[:, :]
            self.Qnew = numpy.zeros(numpy.shape(self.Q))
            self.learnQnew = False
            return False

        if self.cooperation_counter == self.cooperation_time:
            self.learnQnew = True
            for robot in self.basis.robot_list:
                Qtmp = numpy.zeros_like(robot.Q)
                numpy.copyto(Qtmp, robot.Q)
                self.Qnew[:, :] += Qtmp*self.computeWeight()
            self.cooperation_counter = 0
            return True
