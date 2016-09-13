import numpy

from src.framework.learning.baseQLearning import BaseQLearning


class BasicQlearning(BaseQLearning):
    def __init__(self, mas):
        BaseQLearning.__init__(self, mas)
        self.Q = numpy.zeros((mas.nStates, mas.nActions), dtype=numpy.float)  # orientation x row x col
        self.Qnew = numpy.zeros_like(self.Q)

        self.lastReward = 0
        self.expertness = 0

    def updateQ(self, action, state, next_state, reward):  # Main update function
        self.lastReward = reward
        estimate = max(self.Q[next_state, :])
        # main update function
        self.Q[state, action] += self.learn_rate*(reward+self.discount*estimate-self.Q[state, action])

    # returns list of actions, sorted by q matrix values [descending]
    # if there are multiple 'best' actions, these actions get randomly shuffled
    def getActionList(self, state):
        actions_unsorted = list(self.Q[state, :])
        actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1], reverse=True)]

        number_same_value = actions_unsorted.count(actions_sorted[0])  # choose a random action if they have same q values
        actions_same_value = actions_sorted[0:number_same_value]
        numpy.random.shuffle(actions_same_value)
        actions_sorted[0:number_same_value] = actions_same_value
        return actions_sorted

    def computeWeight(self, robot):
        return 1

    def computeExpertness(self): # gets called when Q is updated
        # important variables: last_reward, expertness
        return 0

    def learnedFromRobots(self, basis):
        return False

    def genQmatrix(self):
        return numpy.zeros_like(self.Q)
