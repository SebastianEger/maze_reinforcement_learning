import time
import math
import numpy
from basicRobot import BasicRobot
from operator import add

""" Simple Q-learning agent
    States: (y,x,o) | Actions: Forward = 0 , Right = 1, Backwards = 2, Left = 3
"""


class Diggums(BasicRobot):
    def __init__(self,id,maze,name):
        BasicRobot.__init__(self,id,maze,name)
        self.q_m = numpy.zeros((4*self.rows*self.columns,4),dtype=numpy.float)

    def update_q(self, action, c_p, next_pos, reward):
        self.last_reward = reward
        estimate = max(self.q_m[next_pos[2]*self.rows*self.columns + next_pos[1]*self.rows + next_pos[0],:])
        ind = self.c_p[2]*self.rows*self.columns + self.c_p[1]*self.rows+self.c_p[0]
        self.q_m[ind,action] += self.learn_rate*(reward+self.discount*estimate-self.q_m[ind,action])

    def get_action_list(self):  # returns list of actions, sorted by q matrix values
        index = self.c_p[2]*self.rows*self.columns + self.c_p[1]*self.rows+self.c_p[0]
        actions_unsorted = list(self.q_m[index,:])
        actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1],reverse=True)]
        # choose a random action if they have same q values
        number_same_value = actions_unsorted.count(actions_sorted[0])
        copy = actions_sorted[0:number_same_value]
        copy.sort()
        actions_sorted[0:number_same_value] = copy
        return actions_sorted

    def check_action(self, c_p, r_action): # checks q action
        # check all sensor if there is a wall
        if r_action == 0:
            if self.sim_sensor_front == 1:
                return False
        if r_action == 1:
            if self.sim_sensor_right == 1:
                return False
        if r_action == 2:
            if self.sim_sensor_back == 1:
                return False
        if r_action == 3:
            if self.sim_sensor_left == 1:
                return False
        # if all sensor are false return true
        return True
    
    def get_next_pos(self, r_action): # get next position for q action
        target_pos = []
        if self.c_p[2] == 0:
            y = -1
            x = +1
            if r_action == 0:
                target_pos = map(add,self.c_p,[y,0,0])
                target_pos[2] = 0
            elif r_action == 1:
                target_pos = map(add,self.c_p,[0,x,0])
                target_pos[2] = 1
            elif r_action == 2:
                target_pos = map(add,self.c_p,[-1*y,0,0])
                target_pos[2] = 2
            elif r_action == 3:
                target_pos = map(add,self.c_p,[0,-1*x,0])
                target_pos[2] = 3
            else:
                target_pos = self.c_p
        elif self.c_p[2] == 2:
            y = +1
            x = -1
            if r_action == 0:
                target_pos = map(add,self.c_p,[y,0,0])
                target_pos[2] = 2
            elif r_action == 1:
                target_pos = map(add,self.c_p,[0,x,0])
                target_pos[2] = 3
            elif r_action == 2:
                target_pos = map(add,self.c_p,[-1*y,0,0])
                target_pos[2] = 0
            elif r_action == 3:
                target_pos = map(add,self.c_p,[0,-1*x,0])
                target_pos[2] = 1
            else:
                target_pos = self.c_p
        elif self.c_p[2] == 1:
            y = +1
            x = +1
            if r_action == 0:
                target_pos = map(add,self.c_p,[0,x,0])
                target_pos[2] = 1
            elif r_action == 1:
                target_pos = map(add,self.c_p,[y,0,0])
                target_pos[2] = 2
            elif r_action == 2:
                target_pos = map(add,self.c_p,[0,-1*x,0])
                target_pos[2] = 3
            elif r_action == 3:
                target_pos = map(add,self.c_p,[-1*y,0,0])
                target_pos[2] = 0
            else:
                target_pos = self.c_p
        elif self.c_p[2] == 3:
            y = -1
            x = -1
            if r_action == 0:
                target_pos = map(add,self.c_p,[0,x,0])
                target_pos[2] = 3
            elif r_action == 1:
                target_pos = map(add,self.c_p,[y,0,0])
                target_pos[2] = 0
            elif r_action == 2:
                target_pos = map(add,self.c_p,[0,-1*x,0])
                target_pos[2] = 1
            elif r_action == 3:
                target_pos = map(add,self.c_p,[-1*y,0,0])
                target_pos[2] = 2
            else:
                target_pos = self.c_p
        return target_pos

    def set_q_shared(self,q):
        self.q_m = q