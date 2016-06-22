import numpy


class BasicQlearning:
    def __init__(self, maze):
        self.rows, self.columns, self.dims = numpy.shape(maze)
        self.q_m = numpy.zeros((self.rows*self.columns,4),dtype=numpy.float)  # orientation x row x col
        self.learn_rate = 0.2
        self.discount = 0.9
        self.reward_wall = -10
        self.reward_step = -0.01
        self.reward_goal = 100
        self.reward_robot = -0.01
        self.exploration_rate = 0
        self.last_reward = 0
        self.expertness = 0

    def update_q(self, action, c_p, next_pos, reward):
        self.last_reward = reward
        estimate = max(self.q_m[next_pos[1]*self.rows+next_pos[0],:])
        ind = c_p[1]*self.rows + c_p[0]
        self.q_m[ind,action] += self.learn_rate*(reward+self.discount*estimate-self.q_m[ind,action])*self.compute_weight()

    def compute_weight(self):
        return 1

    def compute_expertness(self): # gets called when Q is updated
        # important variables: last_reward, expertness
        return 0