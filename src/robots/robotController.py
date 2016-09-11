import numpy

# import RobotBuilder.RobotBuilder as RB
from src.framework.agent.mazerobot.mazerobot import MazeRobot
from src.framework.exploration.random import randomexploration, smartrandomexploration
from src.framework.learning.qlearning import basicQlearning, weightedqlearning
from src.framework.movement.discrete import northeastsouthwest, forwardbackwardturn
# from src.robots.Artemis import Artemis
# from src.robots.Butler import Butler
# from src.robots.Diggums import Diggums
# from src.robots.Foaly import Foaly
# from src.robots.Holly import Holly
# from src.robots.TestRobot import TestRobot


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
        self.sharedQmatrix = None

    def init_robots(self, configuration, start_positions, goal_positions):
        self.startPositions = start_positions
        self.goalPositions = goal_positions
        number = len(start_positions)
        print configuration
        for robotID in xrange(number):
            mas = None
            if configuration[0] == 'North East South West':
                mas = northeastsouthwest.NorthEastSouthWest(self.maze)
            if configuration[0] == 'Forward Backward Turn':
                mas = forwardbackwardturn.ForwardBackwardTurn(self.maze)

            qrl = None
            if configuration[1] == 'Basic Q learning':
                qrl = basicQlearning.BasicQlearning(mas)
            if configuration[1] == 'Weighted Q learning':
                qrl = weightedqlearning.WeightedQlearning(mas, self.maze)

            exp = None
            if configuration[2] == 'Random':
                exp = randomexploration.RandomExploration()
            if configuration[2] == 'Smart Random':
                exp = smartrandomexploration.SmartRandomExploration()

            modules = [mas, qrl, exp]

            newRobot = MazeRobot(robotID, modules, self.maze)
            newRobot.current_position = start_positions[robotID]
            newRobot.goal_position = goal_positions[robotID]

            if configuration[3]:
                if self.sharedQmatrix is None:
                    # create shared Q matrix
                    self.sharedQmatrix = newRobot.qrl.genQmatrix()
                newRobot.qrl.Q = self.sharedQmatrix

            self.robot_list.append(newRobot)

        for robot in self.robot_list:
            robot.robot_list = self.robot_list

    def reset_robots(self):
        i = 0
        for robot in self.robot_list:
            robot.reset(self.startPositions[i], self.goalPositions[i])
            i += 1

    def cmd(self, cmd, value=None):
        def set_exploration_mode(mode):
            for _ in self.robot_list:
                _.exploration_mode = mode

        def set_exploration_rate(rate):
            for _ in self.robot_list:
                _.exploration_rate = rate

        def set_doOneActionPerStep(a):
            for _ in self.robot_list:
                _.doOnlyOneActionPerStep = a
                print _.doOnlyOneActionPerStep

        if cmd == "reset_robots":
            self.reset_robots()
        if cmd == "set_exploration_rate":
            set_exploration_rate(value)
        if cmd == "set_exploration_mode":
            set_exploration_mode(value)
        if cmd == "set_doOnlyOneActionPerStep":
            set_doOneActionPerStep(value)
        if cmd == "do_coop_learning":
            for robot in self.robot_list:
                robot.learnFromRobots()
            for robot in self.robot_list:
                robot.learnNewQ()

    def q_settings(self, learn_rate, discount, reward_goal, reward_wall, reward_robot, reward_step, exploration_rate=0):
        for robot in self.robot_list:
            robot.qrl.learn_rate = learn_rate
            robot.qrl.discount = discount
            robot.qrl.reward_wall = reward_wall
            robot.qrl.reward_step = reward_step
            robot.qrl.reward_robot = reward_robot
            robot.qrl.reward_goal = reward_goal
            robot.exp.explorationRate = exploration_rate
