import matplotlib.pyplot as plt
import numpy

import robot
import robot_2
import simulation


class RobotController:

    def __init__(self, number, maze, r_type):
        self.number_robots = number
        self.maze = maze
        self.maze_shape = numpy.shape(maze)
        self.run_mode = 0   # 0 = stepwise
        self.robot_list = []
        self.traveled_map = numpy.zeros(self.maze_shape,dtype=numpy.uint8)
        if r_type == 1:
            for _ in xrange(number):
                new_robot = robot.Robot(_)
                new_robot.c_p = [1,1,2]
                new_robot.goal_position = [self.maze_shape[0]-2,self.maze_shape[1]-2]
                new_robot.init_q_matrix(maze)
                new_robot.traveled_map = self.traveled_map
                maze[new_robot.c_p[0],new_robot.c_p[1],0] = 1
                self.robot_list.append(new_robot)
        else:
            for _ in xrange(number):
                new_robot = robot_2.Robot(_)
                new_robot.c_p = [1,1,2]
                new_robot.goal_position = [self.maze_shape[0]-2,self.maze_shape[1]-2]
                new_robot.init_q_matrix(maze)
                new_robot.traveled_map = self.traveled_map
                maze[new_robot.c_p[0],new_robot.c_p[1],0] = 1
                self.robot_list.append(new_robot)
        for _ in self.robot_list:
            _.robot_list = self.robot_list

    def add_robot(self):
        new_robot = robot.Robot(self.number_robots+1)
        self.number_robots += 1
        self.robot_list.append(new_robot)

    def reset_robots(self):
        i = 0
        self.traveled_map = numpy.zeros(numpy.shape(self.traveled_map),dtype=numpy.uint8)
        for _ in self.robot_list:
            _.traveled_map = self.traveled_map
            self.maze[_.c_p[0],_.c_p[1],0] = 0
            _.c_p = [1,1,2]
            _.goal_position = [self.maze_shape[0]-2,self.maze_shape[1]-2]
            self.maze[_.c_p[0],_.c_p[1],0] = 1
            i += 1

    def set_exploration_mode(self,mode):
        for _ in self.robot_list:
            _.exploration_mode = mode

    def set_exploration_rate(self,rate):
        for _ in self.robot_list:
            _.exploration_rate = rate

    def set_q_matrix(self, m):
        for _ in self.robot_list:
            _.use_q_matrix = m