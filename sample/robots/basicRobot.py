import numpy
from basicMovementAndSensors import BasicMovementAndSensors
from basicExploration import BasicExploration
from basicQlearning import BasicQlearning


""" Simple Q-learning agent
    States: position (y,x) | Actions: North = 0 , East = 1, South = 2, Right = 3
    Robot actions: North = 0 , East = 1, South = 2, Right = 3
"""


class BasicRobot(BasicMovementAndSensors, BasicExploration, BasicQlearning):
    def __init__(self, id, maze, name='StepRobot'):
        BasicMovementAndSensors.__init__(self, maze)
        BasicExploration.__init__(self)
        BasicQlearning.__init__(self, maze, self.nActions, self.nStates)

        ''' Some information about the robot'''
        self.id = id
        self.name = name

        self.exploration_rate = 0

        """ Robot coordinates """
        self.current_position = [1,1,2]  # current_position, y-axis, x-axis, orientation [cm]
        self.goal_position = [10,10,2] # default goal position
        self.history = []
        self.robot_list = []    # list of all robots
        self.traveled_map = numpy.zeros(numpy.shape(maze)) # map to store already visited locations

    """ main function for robot, makes one step each call """
    def makeStep(self):
        if self.goalIsReached():  # check if we reached the goal
            return True, self.current_position # return True because current position is goal position

        self.addPosToHistory()

        actions = self.getActionList(self.getState(self.current_position)) # get action list from Q matrix
        actions = self.explore(self.nActions, actions)

        # check actions and get next position and reward
        for action in actions:
            next_position = self.getNextPos(action, self.current_position) # get target position
            if self.checkAction(self.current_position, action):  # check action if no obstacle is in the way
                self.move(action, next_position)  # move to new location and get reward
                break  # do not check any further actions in actionslist
            else:
                self.stay(action, next_position)  # stay and get reward

        return False, self.current_position

    def move(self, action, next_position):
        if next_position[0] == self.goal_position[0] and next_position[1] == self.goal_position[1]:  # check if target is goal
            self.updateQ(action, self.getState(self.current_position), self.getState(next_position), self.reward_goal)  # update q with reward goal
        else:
            self.updateQ(action, self.getState(self.current_position), self.getState(next_position), self.reward_step)  # update q with reward step
        self.expertness = self.computeExpertness()
        self.current_position = next_position

    def stay(self, action, next_position):
        is_robot = False
        for robot in self.robot_list:  # check if robot
            if next_position[0] == robot.current_position[0] and next_position[1] == robot.current_position[1]:
                is_robot = True
                break

        if is_robot:
            self.updateQ(action, self.getState(self.current_position), self.getState(next_position), self.reward_robot) # update q with reward robot
        else:
            self.updateQ(action, self.getState(self.current_position), self.getState(next_position), self.reward_wall) # update q with reward wall
        self.expertness = self.computeExpertness() # calcualte expertness

    def goalIsReached(self): # function to determine if goal is reached
        if self.current_position[0] == self.goal_position[0] and self.current_position[1] == self.goal_position[1]:
            return True
        return False

    def addPosToHistory(self):
        self.traveled_map[self.current_position[0],self.current_position[1], 0] = 1
        self.history.append([self.current_position[0],self.current_position[1]])  # add old position to history

    def reset(self, start, goal): # reset robot start and goal coordinates
        self.current_position = start
        self.goal_position = goal