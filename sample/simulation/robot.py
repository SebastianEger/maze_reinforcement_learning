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
        self.old_position = [0,0,2]
        self.n_p = [0,0,2]
        self.goal_position = [10,10,2]
        self.history = []
        self.robot_list = []    # contains the other created robots

        self.traveled_map = 0

        """ Q learning settings """
        self.q_matrix_size = []
        self.q_m = numpy.zeros((5,5),dtype=numpy.float)  # orientation x row x col
        self.learn_rate = 0.2
        self.discount = 0.9
        self.exploration_mode = 1
        self.exploration_rate = 0.4
        self.reward_wall = -1
        self.reward_step = -0.01
        self.reward_goal = 10
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
        self.q_m = numpy.zeros((4*self.q_matrix_size[0]*self.q_matrix_size[1],4),dtype=numpy.float)

    def get_reward(self,action):
        next_pos = self.get_next_pos(action)
        if self.check_action(action):
            if action == 4:
                pass
            if next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                self.update_q_matrix(action,next_pos,self.reward_goal)
            else:
                self.update_q_matrix(action,next_pos,self.reward_step)
            return next_pos
        else:
            for _ in self.robot_list:  # check if its a robot
                if next_pos[0] == _.c_p[0] and next_pos[1] == _.c_p[1]:
                    self.update_q_matrix(action,next_pos,self.reward_robot)
                    return next_pos
            self.update_q_matrix(action,next_pos,self.reward_wall)
        return next_pos

    def do_action(self):   # function for getting the next action
        # exploration
        if numpy.random.random_sample(1) <= self.exploration_rate:
            return self.explore(self.exploration_mode)
        # use q learning
        else:
            rows = self.q_matrix_size[0]
            col = self.q_matrix_size[1]

            actions = []
            ind = self.c_p[2]*rows*col+self.c_p[1]*rows+self.c_p[0]
            actions = list(self.q_m[ind,:])
            indices = [i[0] for i in sorted(enumerate(actions), key=lambda x:x[1],reverse=True)]
            for _ in indices:
                if self.check_action(_):
                    return self.get_reward(_)
                else:
                    self.get_reward(_)
            return self.c_p

    def explore(self,mode):
        if mode == 0:
            action_list = []
            for _ in range(4):
                action_list.append(_)
            numpy.random.shuffle(action_list)
            action_list.append(4)
            for action in action_list:
                next_pos = self.get_next_pos(action)
                if self.check_action(action):
                    if action == 4:
                        pass
                    if next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                        self.update_q_matrix(action,next_pos,self.reward_goal)
                    else:
                        self.update_q_matrix(action,next_pos,self.reward_step)
                    return next_pos
                else:
                    next_pos = self.get_next_pos(action)
                    self.update_q_matrix(action,next_pos,self.reward_wall)

        elif mode == 1:
            action_list = []
            # get actions to not visited places
            for action in range(4):
                pos_tmp = self.get_next_pos(action)
                if self.traveled_map[pos_tmp[0],pos_tmp[1],0] == 0:
                    action_list.append(action)
            numpy.random.shuffle(action_list)
            for action in action_list:
                next_pos = self.get_next_pos(action)
                if self.check_action(action):
                    if action == 4:
                        pass
                    elif next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                        self.update_q_matrix(action,next_pos,self.reward_goal)
                    else:
                        self.update_q_matrix(action,next_pos,self.reward_step)
                    return next_pos
                else:
                    self.update_q_matrix(action,next_pos,self.reward_wall)
            action_list_2 = []
            for i in xrange(0,3):
                if i not in action_list:
                    action_list_2.append(i)
            numpy.random.shuffle(action_list_2)
            for action in action_list_2:
                next_pos = self.get_next_pos(action)
                if self.check_action(action):
                    if action == 4:
                        pass
                    elif next_pos[0] == self.goal_position[0] and next_pos[1] == self.goal_position[1]:
                        self.update_q_matrix(action,next_pos,self.reward_goal)
                    else:
                        self.update_q_matrix(action,next_pos,self.reward_step)
                    return next_pos
                else:
                    self.update_q_matrix(action,next_pos,self.reward_wall)
            # stay
            return self.c_p

    def update_q_matrix(self,action,next_pos,reward):
        self.last_reward = reward
        rows = self.q_matrix_size[0]
        col = self.q_matrix_size[1]
        estimate = max(self.q_m[next_pos[2]*col*rows+next_pos[1]*rows+next_pos[0],:])
        ind = self.c_p[2]*rows*col+self.c_p[1]*rows+self.c_p[0]
        self.q_m[ind,action] += self.learn_rate*(reward+self.discount*estimate-self.q_m[ind,action])
        
    def get_next_pos(self, action): # 0: go top, 1: go right, 2: go down, 3: go left
        if self.do_step_wise:
            target_pos = [0,0,0]
            if self.c_p[2] == 0:
                y = -1
                x = +1
                if action == 0:
                    target_pos = map(add,self.c_p,[y,0,0])
                    target_pos[2] = 0
                elif action == 1:
                    target_pos = map(add,self.c_p,[0,x,0])
                    target_pos[2] = 1
                elif action == 2:
                    target_pos = map(add,self.c_p,[-1*y,0,0])
                    target_pos[2] = 2
                elif action == 3:
                    target_pos = map(add,self.c_p,[0,-1*x,0])
                    target_pos[2] = 3
                else:
                    target_pos = self.c_p
            elif self.c_p[2] == 2:
                y = +1
                x = -1
                if action == 0:
                    target_pos = map(add,self.c_p,[y,0,0])
                    target_pos[2] = 2
                elif action == 1:
                    target_pos = map(add,self.c_p,[0,x,0])
                    target_pos[2] = 3
                elif action == 2:
                    target_pos = map(add,self.c_p,[-1*y,0,0])
                    target_pos[2] = 0
                elif action == 3:
                    target_pos = map(add,self.c_p,[0,-1*x,0])
                    target_pos[2] = 1
                else:
                    target_pos = self.c_p
            elif self.c_p[2] == 1:
                y = +1
                x = +1
                if action == 0:
                    target_pos = map(add,self.c_p,[0,x,0])
                    target_pos[2] = 1
                elif action == 1:
                    target_pos = map(add,self.c_p,[y,0,0])
                    target_pos[2] = 2
                elif action == 2:
                    target_pos = map(add,self.c_p,[0,-1*x,0])
                    target_pos[2] = 3
                elif action == 3:
                    target_pos = map(add,self.c_p,[-1*y,0,0])
                    target_pos[2] = 0
                else:
                    target_pos = self.c_p
            elif self.c_p[2] == 3:
                y = -1
                x = -1
                if action == 0:
                    target_pos = map(add,self.c_p,[0,x,0])
                    target_pos[2] = 3
                elif action == 1:
                    target_pos = map(add,self.c_p,[y,0,0])
                    target_pos[2] = 0
                elif action == 2:
                    target_pos = map(add,self.c_p,[0,-1*x,0])
                    target_pos[2] = 1
                elif action == 3:
                    target_pos = map(add,self.c_p,[-1*y,0,0])
                    target_pos[2] = 2
                else:
                    target_pos = self.c_p

            return target_pos
        else:
            if action == 0:
                self.speed = 1
                self.turn_rate = 0

    def check_action(self, action):
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
        return True

    def run(self):
        while True:
            # time_start = time.time()
            print self.c_p
            self.speed = 0.1
            self.turn_rate = math.pi
            time.sleep(self.refresh_rate)
            self.old_position = self.c_p

            self.n_p = self.do_action()

            print 'sensor_back: ' + str(self.sim_sensor_back)
            print 'sensor_front: ' + str(self.sim_sensor_front)
            print 'sensor_left: ' + str(self.sim_sensor_left)
            print 'sensor_right: ' + str(self.sim_sensor_right)
            # self.c_p[0] += self.speed*self.refresh_rate*math.cos(self.turn_rate)
            # self.c_p[1] += self.speed*self.refresh_rate*math.sin(self.turn_rate)
            self.c_p = self.n_p
            #if self.goal_position[0] == self.c_p[0] and self.goal_position[1] == self.c_p[1]:
            #    break
        pass

    def run_step_wise(self):
        # time_start = time.time()
        if self.c_p[0] != self.goal_position[0] or self.c_p[1] != self.goal_position[1]:
            self.old_position = self.c_p
            self.history.append([self.old_position[0],self.old_position[1]])
            self.n_p = self.do_action()
            self.expertness_nrm += self.last_reward
            self.expertness_abs += abs(self.last_reward)
            # self.c_p[0] += self.speed*self.refresh_rate*math.cos(self.turn_rate)
            # self.c_p[1] += self.speed*self.refresh_rate*math.sin(self.turn_rate)
            self.c_p = self.n_p
            return False
        else:
            self.old_position = self.c_p
            return True

if __name__ == '__main__':
    r = Robot()

    r.run()