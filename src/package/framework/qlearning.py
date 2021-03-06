from abc import ABCMeta
from package.framework.agentmodul import AgentModul
import numpy, math
from bisect import bisect
from random import random


class QLearning(AgentModul):
    __metaclass__ = ABCMeta

    expertness_modul = None
    weighting_modul = None

    def __init__(self, config, expertness_modul, weighting_modul):
        self.expertness_modul = expertness_modul
        self.weighting_modul = weighting_modul

        self.learn_rate =  config.get('learn_rate', 1)
        self.discount =  config.get('discount', 0.9)

        self.Q_mat = None
        self.Q_mat_new = None
        self.Q_mat_new_2 = None

        ''' Rewards '''
        self.reward_wall = config.get('reward_wall', -10)
        self.reward_step = config.get('reward_step', -0.01)
        self.reward_goal = config.get('reward_goal', 100)
        self.reward_mat = None

        # expertness
        self.expertness = 0
        # self.reward_robot = -0.01

        self.last_reward = None
        self.weights = []

    def update_Q_mat(self, action, state, next_state, reward):
        self.last_reward = reward
        estimate = max(self.Q_mat[next_state, :])
        self.Q_mat[state, action] += self.learn_rate*(reward+self.discount*estimate-self.Q_mat[state, action])

    def get_action_list(self, state, tau, action_selection):
        # init Q_mat
        if self.Q_mat is None:
            self.Q_mat = numpy.zeros((self.mov.n_states, self.mov.n_actions), dtype=numpy.float)

        action_values = list(self.Q_mat[state, :])

        if action_selection == 'Probabilistic':
            denominator = float()
            P = []

            for value in action_values:
                denominator += math.exp(value/tau)

            for value in action_values:
                P.append(math.exp(value/tau)/denominator)

            cdf = [P[0]]
            for i in xrange(1, len(P)):
                cdf.append(cdf[-1] + P[i])

            random_ind = bisect(cdf,random())
            return [random_ind, ]

        elif action_selection == 'Greedy':
            actions_sorted = [i[0] for i in sorted(enumerate(action_values), key=lambda x:x[1], reverse=True)]

            number_same_value = action_values.count(actions_sorted[0])  # choose a random action if they have same q values
            actions_same_value = actions_sorted[0:number_same_value]
            numpy.random.shuffle(actions_same_value)
            actions_sorted[0:number_same_value] = actions_same_value
            return actions_sorted

    # learns from each agent in agent list the weighted q matrix
    def create_Q_mat_new(self, agent_list):

        # reset Q_mat_new
        self.Q_mat_new = numpy.zeros_like(self.Q_mat)
        self.Q_mat_new_2 = numpy.empty_like(self.Q_mat)
        numpy.copyto(self.Q_mat_new_2, self.Q_mat)
        self.weights = list()

        # create Q_mat_new
        for agent in agent_list:
            w = self.weighting_modul.get_weighting(self.agt, agent, agent_list)
            self.weights.append(w)
            self.Q_mat_new += w*agent.qrl.Q_mat
            self.Q_mat_new_2 += w*(agent.qrl.Q_mat - self.Q_mat)

        # self.Q_mat_new = self.Q_mat_new / self.Q_mat_new.max()

    # set Q_mat to Q_mat_new
    def learn_Q_mat_new(self):

        # print self.Q_mat, self.Q_mat_new
        # copy Q_mat_new to Q_mat
        # self.Q_mat[:, :] = self.Q_mat_new[:, :]
        numpy.copyto(self.Q_mat, self.Q_mat_new)
        # self.Q_mat[:, :] = self.Q_mat_new_2[:, :]

    def zero_Q_mat(self):
        return numpy.zeros((self.mov.n_states,self.mov.n_actions), dtype=numpy.float)

    def init_reward_matrix(self, maze_shape):
        self.reward_matrix = numpy.zeros(maze_shape)
        # goal_reward = maze_shape[0] + maze_shape[1] - 1
        goal_reward = self.reward_goal

        for row in range(maze_shape[0]):
            for col in range(maze_shape[1]):
                self.reward_matrix[-row-1, -col-1] = goal_reward + self.reward_step*row + self.reward_step*col
