import numpy

from sample.robots.Artemis import Artemis
from sample.robots.Butler import Butler
from sample.robots.Diggums import Diggums
from sample.robots.Foaly import Foaly
from sample.robots.Holly import Holly


class RobotController:

    def __init__(self, maze):
        self.maze = maze
        self.q_matrix_size = numpy.shape(maze)

        self.maze_shape = numpy.shape(maze)
        """ all """
        self.traveled_map = numpy.zeros(self.maze_shape, dtype=numpy.uint8)
        self.robot_list = []
        self.startPositions = None
        self.goalPositions = None

        """ Butler """
        self.butler_sq = numpy.zeros((self.q_matrix_size[0]*self.q_matrix_size[1], 4), dtype=numpy.float)

        """ Diggums """
        self.diggums_sq = numpy.zeros((self.q_matrix_size[0]*self.q_matrix_size[1], 4), dtype=numpy.float)

        """ Foaly """
        self.foaly_sq = numpy.zeros((self.q_matrix_size[0]*self.q_matrix_size[1], 4), dtype=numpy.float)

    def init_robots(self, robotName, start_positions, goal_positions):
        self.startPositions = start_positions
        self.goalPositions = goal_positions
        number = len(start_positions)
        if robotName == 'Artemis':
            for _ in xrange(number):
                newRobot = Artemis.Artemis(_, self.maze, robotName)
                newRobot.current_position = start_positions[_]
                newRobot.goal_position = goal_positions[_]
                # newRobot.traveled_map = self.traveled_map
                self.robot_list.append(newRobot)
        if robotName == 'Butler':
            for _ in xrange(number):
                newRobot = Butler.Butler(_, self.maze, robotName, self.butler_sq)
                newRobot.current_position = start_positions[_]
                newRobot.goal_position = goal_positions[_]
                # newRobot.traveled_map = self.traveled_map
                self.robot_list.append(newRobot)
        if robotName == 'Diggums':
            for _ in xrange(number):
                newRobot = Diggums.Diggums(_, self.maze, robotName, self.diggums_sq)
                newRobot.current_position = start_positions[_]
                newRobot.goal_position = goal_positions[_]
                self.robot_list.append(newRobot)
        if robotName == 'Foaly':
            for _ in xrange(number):
                newRobot = Foaly.Foaly(_, self.maze, robotName, self.foaly_sq)
                newRobot.current_position = start_positions[_]
                newRobot.goal_position = goal_positions[_]
                self.robot_list.append(newRobot)
        if robotName == 'Holly':
            for _ in xrange(number):
                newRobot = Holly.Holly(_, self.maze, robotName)
                newRobot.current_position = start_positions[_]
                newRobot.goal_position = goal_positions[_]
                self.robot_list.append(newRobot)
        for robot in self.robot_list:
            robot.robot_list = self.robot_list

    def reset_robots(self):
        i = 0
        for robot in self.robot_list:
            robot.reset(self.startPositions[i], self.goalPositions[i])
            i += 1

    def cmd(self, cmd, value=None):
        if cmd == "reset_robots":
            self.reset_robots()
        if cmd == "set_exploration_rate":
            self.set_exploration_rate(value)
        if cmd == "set_exploration_mode":
            self.set_exploration_mode(value)
        if cmd == "do_coop_learning":
            for robot in self.robot_list:
                robot.learnFromRobots()
            for robot in self.robot_list:
                robot.learnNewQ()

    def set_exploration_mode(self, mode):
        for _ in self.robot_list:
            _.exploration_mode = mode

    def set_exploration_rate(self,rate):
        for _ in self.robot_list:
            _.exploration_rate = rate

    def q_settings(self, learn_rate, discount, reward_goal, reward_wall, reward_robot, reward_step, exploration_rate=0):
        for robot in self.robot_list:
            robot.learn_rate = learn_rate
            robot.discount = discount
            robot.reward_wall = reward_wall
            robot.reward_step = reward_step
            robot.reward_robot = reward_robot
            robot.reward_goal = reward_goal
            robot.exploration_rate = exploration_rate
