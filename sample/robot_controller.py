import numpy
from sample.robots import Artemis, Holly, Koboi, Butler



class RobotController:

    def __init__(self, maze):
        self.maze = maze
        self.q_matrix_size = numpy.shape(maze)

        self.maze_shape = numpy.shape(maze)
        """ all """
        self.traveled_map = numpy.zeros(self.maze_shape,dtype=numpy.uint8)
        self.robot_list = []

        """ Butler """
        self.shared_q_m = numpy.zeros((self.q_matrix_size[0]*self.q_matrix_size[1],4),dtype=numpy.float)

    def init_robots(self,robot,start_positions,goal_positions):
        number = len(start_positions)
        if robot == 'Artemis':
            for _ in xrange(number):
                new_robot = Artemis.Artemis(_,self.maze,robot)
                new_robot.c_p = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        if robot == 'Butler':
            for _ in xrange(number):
                new_robot = Butler.Butler(_,self.maze,robot)
                new_robot.c_p = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                new_robot.set_q_shared(self.shared_q_m)
                new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        if robot == 'Holly':
            for _ in xrange(number):
                new_robot = Holly.Holly(_,self.maze,robot)
                new_robot.c_p = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        if robot == 'Koboi':
            for _ in xrange(number):
                new_robot = Koboi.Koboi(_, self.maze, robot)
                new_robot.c_p = start_positions[_]
                new_robot.goal_position = goal_positions[_]
                new_robot.traveled_map = self.traveled_map
                self.robot_list.append(new_robot)
        for robot in self.robot_list:
            robot.robot_list = self.robot_list

    def reset_robots(self,start_positions,goal_positions):
        i = 0
        self.traveled_map = numpy.zeros(numpy.shape(self.traveled_map),dtype=numpy.uint8)
        for robot in self.robot_list:
            robot.traveled_map = self.traveled_map
            robot.reset(start_positions[i],goal_positions[i])
            i += 1

    def set_exploration_mode(self,mode):
        for _ in self.robot_list:
            _.exploration_mode = mode

    def set_exploration_rate(self,rate):
        for _ in self.robot_list:
            _.exploration_rate = rate

    def q_settings(self, learn_rate, discount, reward_goal, reward_wall, reward_robot, reward_step, cooperation_time = 0):
        for robot in self.robot_list:
            robot.learn_rate = learn_rate
            robot.discount = discount
            robot.reward_wall = reward_wall
            robot.reward_step = reward_step
            robot.reward_robot = reward_robot
            robot.reward_goal = reward_goal
            if robot.name == "Koboi":
                robot.cooperation_time = cooperation_time
            if robot.name == "Holly":
                robot.cooperation_time = cooperation_time
