import numpy
from basicSensors import BasicSensors
from basicExploration import BasicExploration
from basicQlearning import BasicQlearning
from operator import add


""" Simple Q-learning agent
    States: position (y,x) | Actions: North = 0 , East = 1, South = 2, Right = 3
    Robot actions: North = 0 , East = 1, South = 2, Right = 3
"""


class BasicRobot(BasicSensors, BasicExploration, BasicQlearning):
    def __init__(self, id, maze, name = 'StepRobot'):
        BasicSensors.__init__(self)
        BasicExploration.__init__(self)
        BasicQlearning.__init__(self, maze)
        self.id = id
        self.name = name

        """ robot specs """
        self.c_p = [1,1,2]  # current_position, y-axis, x-axis, orientation [cm]
        self.o_p = []  # old position
        self.n_p = self.c_p  # next position
        self.goal_position = [10,10,2]
        self.history = []
        self.robot_list = []    # list ofother created robots
        self.traveled_map = numpy.zeros(numpy.shape(maze))


    """ main function for robot, makes one step each call """
    def make_step(self):
        self.o_p = self.c_p  # set old_position
        if self.reached_goal():  # check if we reached the goal
            self.o_p = self.c_p
            return True

        self.history.append([self.o_p[0],self.o_p[1]])  # add position to history

        actions = self.get_action_list()
        if numpy.random.random_sample(1) < self.exploration_rate:
            actions = self.explore

        # check actions and get next position and reward
        for action in actions:
            self.n_p = self.get_next_pos(action)
            if self.check_action(self.c_p, action):  # check action if no obstacle is in the way
                if self.n_p[0] == self.goal_position[0] and self.n_p[1] == self.goal_position[1]:
                    self.update_q(action, self.c_p, self.n_p, self.reward_goal)
                else:
                    self.update_q(action, self.c_p, self.n_p, self.reward_step)
                break
            else:
                is_robot = False
                for robot in self.robot_list:  # check if robot
                    if self.n_p[0] == robot.c_p[0] and self.n_p[1] == robot.c_p[1]:
                        is_robot = True
                        break
                if is_robot:
                    self.update_q(action, self.c_p, self.n_p, self.reward_robot)
                else:
                    self.update_q(action, self.c_p,self.n_p, self.reward_wall)
                self.expertness = self.compute_expertness()
                self.n_p = self.c_p # reset next position to current position

        self.expertness = self.compute_expertness()
        self.c_p = self.n_p
        return False

    def get_action_list(self):  # returns list of q_actions, sorted by q matrix values
        index = self.c_p[1]*self.rows+self.c_p[0]
        actions_unsorted = list(self.q_m[index,:])
        actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1],reverse=True)]

        number_same_value = actions_unsorted.count(actions_sorted[0]) # choose a random action if they have same q values
        copy = actions_sorted[0:number_same_value]
        numpy.random.shuffle(copy)
        actions_sorted[0:number_same_value] = copy
        return actions_sorted

    def get_next_pos(self, q_action): # get next position for q action
        if q_action == 0:
            target_pos = map(add,self.c_p,[-1,0,0])
            target_pos[2] = 0
        elif q_action == 1:
            target_pos = map(add,self.c_p,[0,+1,0])
            target_pos[2] = 1
        elif q_action == 2:
            target_pos = map(add,self.c_p,[+1,0,0])
            target_pos[2] = 2
        elif q_action == 3:
            target_pos = map(add,self.c_p,[0,-1,0])
            target_pos[2] = 3
        else:
            target_pos = self.c_p
        return target_pos

    def reached_goal(self): # function to determine if goal is reached
        if self.c_p[0] == self.goal_position[0] and self.c_p[1] == self.goal_position[1]:
            return True
        return False

    def reset(self, start, goal):
        self.c_p = start
        self.n_p = start
        self.o_p = start
        self.goal_position = goal