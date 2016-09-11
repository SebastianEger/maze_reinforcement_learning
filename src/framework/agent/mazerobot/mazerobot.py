import numpy

from src.framework.agent.agent import Agent

""" Simple Q-learning agent
    States: position (y,x) | Actions: North = 0 , East = 1, South = 2, Right = 3
    Robot actions: North = 0 , East = 1, South = 2, Right = 3
"""


class MazeRobot(Agent):
    def __init__(self, info, modules, maze):
        Agent.__init__(self, info, modules)
        self.madeSteps = 0
        self.learningTrial = 0
        self.maze = maze

        self.history = []
        self.robot_list = []    # list of all robots

        self.traveled_map = numpy.zeros(numpy.shape(maze), dtype=numpy.float) # map to store already visited locations
        self.traveled_map[:, 0, 0] = 1
        self.traveled_map[:,-1,0] = 1
        self.traveled_map[0,:,0] = 1
        self.traveled_map[-1,:,0] = 1

        self.stepCounter = 0

        self.doOnlyOneActionPerStep = False


    """ main function for robot, makes one step each call """
    def makeStep(self):
        self.madeSteps += 1
        if self.goalIsReached():  # check if we reached the goal
            return True, self.current_position  # return True because current position is goal position

        self.addPosToHistory()

        actions = self.qrl.getActionList(self.mov.getState(self.current_position))  # get action list from Q matrix
        if self.doExploration():
            actions = self.exp.getActionList(self, actions)

        # check actions and get next position and reward
        for action in actions:
            next_position = self.mov.getNextPos(self.current_position, action)  #  get target position
            if self.mov.checkAction(self.current_position, action, next_position, self.sen):  # check action if no obstacle is in the way
                self.move(action, next_position)  # move to new location and get reward
                self.stepCounter += 1
                break  # do not check any further actions in actionslist
            else:
                self.stay(action, next_position)  # stay and get reward
                if self.doOnlyOneActionPerStep:
                    self.stepCounter += 1
                    break

        return False, self.current_position

    def move(self, action, nextPosition):
        reward = self.qrl.reward_step
        if nextPosition[0] == self.goal_position[0] and nextPosition[1] == self.goal_position[1]:  # check if target is goal
            reward = self.qrl.reward_goal
        self.qrl.updateQ(action,
                           self.mov.getState(self.current_position),
                           self.mov.getState(nextPosition),
                           reward)  # update q with reward step
        self.qrl.expertness = self.qrl.computeExpertness()
        self.current_position = nextPosition

    def stay(self, action, nextPosition):
        reward = self.qrl.reward_wall
        if self.robotAtPosition(nextPosition):
            reward = self.qrl.reward_robot
        self.qrl.updateQ(action,
                           self.mov.getState(self.current_position),
                           self.mov.getState(nextPosition),
                           reward)  # update q with reward wall
        self.qrl.expertness = self.qrl.computeExpertness()  # calculate expertness

    def goalIsReached(self):  # function to determine if goal is reached
        if self.current_position[0] == self.goal_position[0] and self.current_position[1] == self.goal_position[1]:
            return True
        return False

    def addPosToHistory(self):
        self.traveled_map[self.current_position[0], self.current_position[1], 0] = 1
        self.history.append([self.current_position[0], self.current_position[1]])  # add old position to history

    def doExploration(self):
        if numpy.random.random_sample(1) < self.exp.getExplorationRate():
            return True
        else:
            return False

    def robotAtPosition(self, position):
        isRobot = False
        for robot in self.robot_list:  # check if robot
            if position[0] == robot.current_position[0] and position[1] == robot.current_position[1]:
                isRobot = True
                break
        return isRobot

    def reset(self, start, goal): # reset robot start and goal coordinates
        self.current_position = start
        self.goal_position = goal
        self.stepCounter = 0
        self.learningTrial += 1
        self.traveled_map = numpy.zeros(numpy.shape(self.traveled_map), dtype=numpy.float) # map to store already visited locations
        self.traveled_map[:, 0, 0] = 1
        self.traveled_map[:, -1, 0] = 1
        self.traveled_map[0, :, 0] = 1
        self.traveled_map[-1, :, 0] = 1
