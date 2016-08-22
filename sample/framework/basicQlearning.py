import numpy
from sample.framework.baseQLearning import BaseQLearning


class BasicQlearning(BaseQLearning):
    def __init__(self, basis, maze):
        BaseQLearning.__init__(self, basis)
        rows, columns, dims = numpy.shape(maze)
        self.Q = numpy.zeros((basis.nStates, basis.nActions), dtype=numpy.float)  # orientation x row x col

        ''' Other '''
        self.lastReward = 0
        self.expertness = 0

    def updateQ(self, action, state, next_state, reward): # Main update function
        self.lastReward = reward
        estimate = max(self.Q[next_state,:])
        # main update function
        self.Q[state, action] += self.learn_rate*(reward+self.discount*estimate-self.Q[state, action])*self.computeWeight()

    # returns list of q_actions, sorted by q matrix values [descending]
    # array is sorted by descending q matrix values
    def getActionList(self, state):
        actions_unsorted = list(self.Q[state,:])
        actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1],reverse=True)]

        number_same_value = actions_unsorted.count(actions_sorted[0]) # choose a random action if they have same q values
        copy = actions_sorted[0:number_same_value]
        numpy.random.shuffle(copy)
        actions_sorted[0:number_same_value] = copy
        return actions_sorted

    def computeWeight(self):
        return 1

    def computeExpertness(self): # gets called when Q is updated
        # important variables: last_reward, expertness
        return 0

    def learnedFromRobots(self):
        return False
