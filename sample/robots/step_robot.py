import numpy
from operator import add


""" Simple Q-learning agent
    States: position (y,x) | Actions: North = 0 , East = 1, South = 2, Right = 3
    Robot actions: Forward = 0, Right = 1, Backwards = 2, Left = 3
"""


class StepRobot:
    def __init__(self,id,maze,name = 'StepRobot'):
        self.id = id
        self.name = name

        """ robot specs """
        self.c_p = [1,1,2]  # current_position, y-axis, x-axis, orientation [cm]
        self.o_p = []  # old position
        self.n_p = self.c_p  # next position
        self.goal_position = [10,10,2]
        self.history = []
        self.robot_list = []    # list ofother created robots

        """ Q learning """
        self.rows, self.columns, self.dims = numpy.shape(maze)
        self.q_m = numpy.zeros((self.rows*self.columns,4),dtype=numpy.float)  # orientation x row x col
        self.learn_rate = 0.2
        self.discount = 0.9
        self.reward_wall = -10
        self.reward_step = -0.01
        self.reward_goal = 100
        self.reward_robot = -0.01
        self.last_reward = 0

        """ simulated sensors for wall detection """
        self.sim_sensor_front = 0  # if there is a wall in front, sensor = 1, robot = 2, nothing = 0
        self.sim_sensor_back = 0
        self.sim_sensor_left = 0
        self.sim_sensor_right = 0
        self.sim_sensor_goal = 0  # goal = 1, no goal insight = 0


    """ main function for robot, makes one step each call """
    def make_step(self):
        if self.c_p[0] != self.goal_position[0] or self.c_p[1] != self.goal_position[1]:  # check if we reached the goal
            self.o_p = self.c_p  # set old_position
            self.history.append([self.o_p[0],self.o_p[1]])  # add position to history

            # get actions
            actions = self.get_action_list()  # get next action
            # check actions and get next position and reward
            for action in actions:
                self.n_p = self.get_next_pos(action)
                if self.check_action(action):  # check action if no obstacle is in the way
                    if self.n_p[0] == self.goal_position[0] and self.n_p[1] == self.goal_position[1]:
                        self.update_q(action,self.n_p,self.reward_goal)
                    else:
                        self.update_q(action,self.n_p,self.reward_step)
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

            self.c_p = self.n_p
            return False
        else:
            self.old_position = self.c_p
            return True

    def get_action_list(self):  # returns list of actions, sorted by q matrix values
        index = self.c_p[1]*self.rows+self.c_p[0]
        actions_unsorted = list(self.q_m[index,:])
        actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1],reverse=True)]
        # choose a random action if they have same q values
        number_same_value = actions_unsorted.count(actions_sorted[0])
        copy = actions_sorted[0:number_same_value]
        numpy.random.shuffle(copy)
        actions_sorted[0:number_same_value] = copy

        return actions_sorted

    def update_q(self, action, next_pos, reward):
        self.last_reward = reward
        estimate = max(self.q_m[next_pos[1]*self.rows+next_pos[0],:])
        ind = self.c_p[1]*self.rows+self.c_p[0]
        self.q_m[ind,action] += self.learn_rate*(reward+self.discount*estimate-self.q_m[ind,action])

    """ some basic functions for robot functions """

    def check_action(self, q_action): # checks q action
        # transform q action to robot action
        def transform_q_action(q_action):
            if self.c_p[2] == 0:
                if q_action == 0:
                    return 0
                elif q_action == 2:
                    return 2
                if q_action == 3:
                    return 3
                elif q_action == 1:
                    return 1
            elif self.c_p[2] == 2:
                if q_action == 0:
                    return 2
                elif q_action == 2:
                    return 0
                if q_action == 3:
                    return 1
                elif q_action == 1:
                    return 3
            elif self.c_p[2] == 1:
                if q_action == 0:
                    return 3
                elif q_action == 2:
                    return 1
                if q_action == 3:
                    return 2
                elif q_action == 1:
                    return 0
            elif self.c_p[2] == 3:
                if q_action == 0:
                    return 1
                elif q_action == 2:
                    return 3
                if q_action == 3:
                    return 0
                elif q_action == 1:
                    return 2
            return 4  # wait
        r_action = transform_q_action(q_action)
        # check all sensor if there is a wall
        if r_action == 0:
            if self.sim_sensor_front == 1:
                return False
        if r_action == 1:
            if self.sim_sensor_right == 1:
                return False
        if r_action == 2:
            if self.sim_sensor_back == 1:
                return False
        if r_action == 3:
            if self.sim_sensor_left == 1:
                return False
        # if all sensor are false return true
        return True

    def get_next_pos(self,q_action): # get next position for q action
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

    def reset(self,start,goal):
        self.c_p = start
        self.n_p = start
        self.o_p = start
        self.goal_position = goal