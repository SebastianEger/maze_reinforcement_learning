import numpy
from sample.framework.baseRobot import BaseRobot

""" Simple Q-learning agent
    States: position (y,x) | Actions: North = 0 , East = 1, South = 2, Right = 3
    Robot actions: North = 0 , East = 1, South = 2, Right = 3
"""


class BasicRobot(BaseRobot):
    def __init__(self, basis, idnr, name, maze):
        BaseRobot.__init__(self, basis, idnr, name)
        self.madeSteps = 0
        self.learningTrial = 0

        self.history = []
        self.robot_list = []    # list of all robots

        self.traveled_map = numpy.zeros(numpy.shape(maze), dtype=numpy.float) # map to store already visited locations
        self.traveled_map[:, 0, 0] = 1
        self.traveled_map[:,-1,0] = 1
        self.traveled_map[0,:,0] = 1
        self.traveled_map[-1,:,0] = 1


    """ main function for robot, makes one step each call """
    def makeStep(self):
        self.madeSteps += 1
        if self.goalIsReached():  # check if we reached the goal
            return True, self.current_position # return True because current position is goal position

        self.addPosToHistory()

        actions = self.basis.getActionList(self.basis.getState(self.current_position)) # get action list from Q matrix
        actions = self.basis.explore(actions)

        # check actions and get next position and reward
        if not self.basis.learnedFromRobots():
            for action in actions:
                next_position = self.basis.getNextPos(self.current_position, action) # get target position
                if self.basis.checkAction(self.current_position, action):  # check action if no obstacle is in the way
                    self.move(action, next_position)  # move to new location and get reward
                    break  # do not check any further actions in actionslist
                else:
                    self.stay(action, next_position)  # stay and get reward
                    break

        return False, self.current_position

    def move(self, action, next_position):
        reward = self.basis.reward_step
        if next_position[0] == self.goal_position[0] and next_position[1] == self.goal_position[1]:  # check if target is goal
            reward = self.basis.reward_goal
        self.basis.updateQ(action,
                           self.basis.getState(self.current_position),
                           self.basis.getState(next_position),
                           reward)  # update q with reward step
        self.basis.expertness = self.basis.computeExpertness()
        self.current_position = next_position

    def stay(self, action, next_position):
        reward = self.basis.reward_wall
        for robot in self.robot_list:  # check if robot
            if next_position[0] == robot.current_position[0] and next_position[1] == robot.current_position[1]:
                reward = self.basis.reward_robot
                break
        self.basis.updateQ(action,
                           self.basis.getState(self.current_position),
                           self.basis.getState(next_position),
                           reward)  # update q with reward wall
        self.basis.expertness = self.basis.computeExpertness()  # calculate expertness

    def goalIsReached(self):  # function to determine if goal is reached
        if self.current_position[0] == self.goal_position[0] and self.current_position[1] == self.goal_position[1]:
            return True
        return False

    def addPosToHistory(self):
        self.traveled_map[self.current_position[0], self.current_position[1], 0] = 1
        self.history.append([self.current_position[0], self.current_position[1]])  # add old position to history

    def reset(self, start, goal): # reset robot start and goal coordinates
        self.current_position = start
        self.goal_position = goal
        self.learningTrial += 1
        self.traveled_map = numpy.zeros(numpy.shape(self.traveled_map), dtype=numpy.float) # map to store already visited locations
        self.traveled_map[:, 0, 0] = 1
        self.traveled_map[:, -1, 0] = 1
        self.traveled_map[0, :, 0] = 1
        self.traveled_map[-1, :, 0] = 1
