import time
import math
import numpy
from operator import add


class Robot:
    def __init__(self,id):
        self.id = id

        """ robot specs """
        self.radius = 5  # [cm]
        self.speed = 0  # [m/s]
        self.turn_rate = 0  # [w]
        self.c_p = [1,1,2]  # y-axis, x-axis, orientation [cm]
        self.o_p = [0,0,2]
        self.n_p = [0,0,2]
        self.goal_position = []
        self.history = []
        self.robot_list = []    # contains the other created robots
        self.traveled_map = 0

        """ Q learning settings """
        self.q_matrix_size = []
        self.q_m = numpy.zeros((5,5),dtype=numpy.float)  # orientation x row x col
        self.learn_rate = 0.2
        self.discount = 0.9
        self.reward_wall = -10
        self.reward_step = -0.01
        self.reward_goal = 100
        self.reward_robot = -0.01
        self.last_reward = 0

        """ coop qlearning settings """
        self.expertness_nrm = 0
        self.expertness_abs = 0

        """ simulated sensors for wall detection """
        self.sim_sensor_front = 0  # if there is a wall in front, sensor = 1, robot = 2, nothing = 0
        self.sim_sensor_back = 0
        self.sim_sensor_left = 0
        self.sim_sensor_right = 0
        self.sim_sensor_goal = 0  # goal = 1, no goal insight = 0

        """ simulation settings """
        self.do_step_wise = True
        self.refresh_rate = 0   # [s], time per step execution

    def init_q_matrix(self,maze):
        self.q_matrix_size = numpy.shape(maze)
        self.q_m = numpy.zeros((self.q_matrix_size[0]*self.q_matrix_size[1],4),dtype=numpy.float)

    def get_reward_and_n_p(self,action):
        next_pos = self.get_next_pos(action)
        if self.check_action(action):  # no object at next_pos
            if action == 4:
                pass
            if next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                self.update_q_matrix(action,next_pos,self.reward_goal)
            else:
                self.update_q_matrix(action,next_pos,self.reward_step)
        else:  # object at next_pos, wall or robot?
            for _ in self.robot_list:  # check if robot
                if next_pos[0] == _.c_p[0] and next_pos[1] == _.c_p[1]:
                    self.update_q_matrix(action,next_pos,self.reward_robot)
                    return next_pos
            self.update_q_matrix(action,next_pos,self.reward_wall)
        return next_pos

    def do_action(self):   # function for getting the next action
        rows = self.q_matrix_size[0]
        actions = []

        ind = self.c_p[1]*rows+self.c_p[0]
        actions = list(self.q_m[ind,:])
        indices = [i[0] for i in sorted(enumerate(actions), key=lambda x:x[1],reverse=True)]
        for _ in indices:
            if self.check_action(_):
                return self.get_reward_and_n_p(_)
            else:
                self.get_reward_and_n_p(_)
        return self.c_p  # if no cell is free

    def update_q_matrix(self,action,next_pos,reward):
        self.last_reward = reward
        rows = self.q_matrix_size[0]
        estimate = max(self.q_m[next_pos[1]*rows+next_pos[0],:])
        ind = self.c_p[1]*rows+self.c_p[0]
        self.q_m[ind,action] += self.learn_rate*(reward+self.discount*estimate-self.q_m[ind,action])

    def check_action(self, a):
        # transform q action to robot action
        def get_robot_action(action):
            if self.c_p[2] == 0:
                if action == 0:
                    return 0
                elif action == 2:
                    return 2
                if action == 3:
                    return 3
                elif action == 1:
                    return 1
            elif self.c_p[2] == 2:
                if action == 0:
                    return 2
                elif action == 2:
                    return 0
                if action == 3:
                    return 1
                elif action == 1:
                    return 3
            elif self.c_p[2] == 1:
                if action == 0:
                    return 3
                elif action == 2:
                    return 1
                if action == 3:
                    return 2
                elif action == 1:
                    return 0
            elif self.c_p[2] == 3:
                if action == 0:
                    return 1
                elif action == 2:
                    return 3
                if action == 3:
                    return 0
                elif action == 1:
                    return 2
            return 4  # wait
        action = get_robot_action(a)
        # check all sensor if there is a wall
        if action == 0:
            if self.sim_sensor_front == 1:
                return False
        if action == 1:
            if self.sim_sensor_right == 1:
                return False
        if action == 2:
            if self.sim_sensor_back == 1:
                return False
        if action == 3:
            if self.sim_sensor_left == 1:
                return False
        # if all sensor are false return true
        return True

    def get_next_pos(self,action):
        if action == 0:
            target_pos = map(add,self.c_p,[-1,0,0])
            target_pos[2] = 0
        elif action == 1:
            target_pos = map(add,self.c_p,[0,+1,0])
            target_pos[2] = 1
        elif action == 2:
            target_pos = map(add,self.c_p,[+1,0,0])
            target_pos[2] = 2
        elif action == 3:
            target_pos = map(add,self.c_p,[0,-1,0])
            target_pos[2] = 3
        else:
            target_pos = self.c_p
        return target_pos

    def make_step(self):
        # time_start = time.time()
        if self.c_p[0] != self.goal_position[0] or self.c_p[1] != self.goal_position[1]:
            self.o_p = self.c_p
            self.history.append([self.o_p[0],self.o_p[1]])
            self.n_p = self.do_action()
            #print self.q_m[self.old_position[1]*self.q_matrix_size[0]+self.old_position[0],:]
            self.expertness_nrm += self.last_reward
            self.expertness_abs += abs(self.last_reward)
            self.c_p = self.n_p
            return False
        else:
            self.old_position = self.c_p
            return True

if __name__ == '__main__':
    r = Robot()

    r.run()