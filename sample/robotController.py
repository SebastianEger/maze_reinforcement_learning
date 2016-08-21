import numpy

from robots import Holly, Koboi
from sample.robots.Artemis import Artemis
from sample.robots.Butler import Butler
from sample.robots.Diggums import Diggums
from sample.robots.Foaly import Foaly


class RobotController:

    def __init__(self, maze):
        self.maze = maze
        self.q_matrix_size = numpy.shape(maze)

        self.maze_shape = numpy.shape(maze)
        """ all """
        self.traveled_map = numpy.zeros(self.maze_shape, dtype=numpy.uint8)
        self.robot_list = []

        """ Butler """
        self.butler_sq = numpy.zeros((self.q_matrix_size[0]*self.q_matrix_size[1],4), dtype=numpy.float)

        """ Diggums """
        self.diggums_sq = numpy.zeros((4*self.q_matrix_size[0]*self.q_matrix_size[1],4),dtype=numpy.float)

    def init_robots(self, robot, start_positions, goal_positions):
        number = len(start_positions)
        if robot == 'Artemis':
            for _ in xrange(number):
                new_robot = Artemis.Artemis(_, self.maze, robot)
                new_robot.current_position = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                # new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        if robot == 'Butler':
            for _ in xrange(number):
                new_robot = Butler.Butler(_, self.maze, robot)
                new_robot.current_position = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                new_robot.set_q_shared(self.butler_sq)
                # new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        if robot == 'Holly':
            for _ in xrange(number):
                new_robot = Holly.Holly(_,self.maze,robot)
                new_robot.current_position = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                self.robot_list.append(new_robot)
        if robot == 'Koboi':
            for _ in xrange(number):
                new_robot = Koboi.Koboi(_, self.maze, robot)
                new_robot.current_position = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                # new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        if robot == 'Diggums':
            for _ in xrange(number):
                new_robot = Diggums.Diggums(_, self.maze, robot)
                new_robot.current_position = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                # new_robot.traveled_map = self.traveled_map
                new_robot.set_q_shared(self.diggums_sq)
                self.robot_list.append(new_robot)
        if robot == 'Foaly':
            for _ in xrange(number):
                new_robot = Foaly.Foaly(_, self.maze, robot)
                new_robot.current_position = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                # new_robot.traveled_map = self.traveled_map
                new_robot.set_q_shared(self.diggums_sq)
                self.robot_list.append(new_robot)
        for robot in self.robot_list:
            robot.robot_list = self.robot_list

    def reset_robots(self, start_positions, goal_positions):
        i = 0
        for robot in self.robot_list:
            robot.reset(start_positions[i], goal_positions[i])
            i += 1

    def set_exploration_mode(self,mode):
        for _ in self.robot_list:
            _.exploration_mode = mode

    def set_exploration_rate(self,rate):
        for _ in self.robot_list:
            _.exploration_rate = rate

    def q_settings(self, learn_rate, discount, reward_goal, reward_wall, reward_robot, reward_step, exploration_rate=0, cooperation_time = 0):
        for robot in self.robot_list:
            robot.q.learn_rate = learn_rate
            robot.q.discount = discount
            robot.q.reward_wall = reward_wall
            robot.q.reward_step = reward_step
            robot.q.reward_robot = reward_robot
            robot.q.reward_goal = reward_goal
            robot.e.exploration_rate = exploration_rate

            if robot.name == "Koboi":
                robot.cooperation_time = cooperation_time
            if robot.name == "Holly":
                robot.cooperation_time = cooperation_time
