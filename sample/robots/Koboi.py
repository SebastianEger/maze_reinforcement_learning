import time
import math
import numpy
from step_robot import StepRobot
from operator import add


class Koboi(StepRobot):
    def __init__(self,id,maze,name):
        StepRobot.__init__(self,id,maze,name)
        self.q_new = numpy.zeros((self.rows*self.columns,4),dtype=numpy.float)
        self.cooperation_time = 20
        self.cooperation_counter = 0
        self.expertness = 0

    def make_step(self):
        if self.c_p[0] != self.goal_position[0] or self.c_p[1] != self.goal_position[1]:  # check if we reached the goal
            self.o_p = self.c_p  # set old_position
            self.history.append([self.o_p[0],self.o_p[1]])  # add position to history

            # get actions
            actions = self.get_action_list()  # get next action

            if self.cooperation_counter >= self.cooperation_time:
                self.q_new = numpy.zeros((self.rows*self.columns,4),dtype=numpy.float)
                expertness_sum = 0
                for robot in self.robot_list:
                    expertness_sum += robot.expertness

                for robot in self.robot_list:
                    if robot != self:
                        self.q_new += robot.q_m*robot.expertness/expertness_sum
                self.cooperation_counter = 0
                self.n_p = self.c_p # wait one step
            else:
                if self.cooperation_counter == 0:
                    self.q_m = self.q_new
                for action in actions:
                    self.n_p = self.get_next_pos(action)
                    if self.check_action(action):  # check action if no obstacle is in the way
                        if self.n_p[0] == self.goal_position[0] and self.n_p[1] == self.goal_position[1]:
                            self.update_q(action,self.n_p,self.reward_goal)
                            self.expertness += self.reward_goal
                        else:
                            self.update_q(action,self.n_p,self.reward_step)
                            self.expertness += self.reward_step
                        break
                    else:
                        is_robot = False
                        for robot in self.robot_list:  # check if robot
                            if self.n_p[0] == robot.c_p[0] and self.n_p[1] == robot.c_p[1]:
                                is_robot = True
                                break
                        if is_robot:
                            self.update_q(action,self.n_p,self.reward_robot)
                        else:
                            self.update_q(action,self.n_p,self.reward_wall)
                        self.n_p = self.c_p # reset next position to current position

            self.cooperation_counter += 1
            self.c_p = self.n_p
            return False
        else:
            self.old_position = self.c_p
            return True

    def reset(self,start,goal):
        StepRobot.reset(self, start, goal)
        self.cooperative_counter = 0