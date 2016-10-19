import numpy
from src.framework.sensor import Sensor

class Agent:
    mov = None  # Movement module
    qrl = None  # Q Reinforcement Learning module
    exp = None  # Exploration module
    sen = None  # Sensor module

    current_position = None
    goal_position = None
    start_position = None

    action_selection = 'Greedy'

    def __init__(self, agent_id, maze_size):
        self.agent_id = agent_id

        self.step_counter = 0
        self.trial_counter = 0

        self.history = []
        self.agent_list = []    # list of all agentcontroller

        # init traveled map
        self.traveled_map = numpy.zeros(maze_size, dtype=numpy.float) # map to store already visited locations
        self.traveled_map[:, 0, 0] = 1
        self.traveled_map[:,-1,0] = 1
        self.traveled_map[0,:,0] = 1
        self.traveled_map[-1,:,0] = 1

        self.one_action_per_step = False

    def init_modules(self, mov, qrl, exp):
        self.mov = mov
        self.qrl = qrl
        self.exp = exp
        self.sen = Sensor()

        self.mov.init_agent_modules(self)
        self.qrl.init_agent_modules(self)
        self.exp.init_agent_modules(self)

    def run(self):
        self.step_counter += 1
        if self.goal_reached():  # check if we reached the goal
            return True, self.current_position  # return True because current position is goal position

        self.add_current_position_to_history()

        action_list = self.qrl.get_action_list(self.mov.get_state(self.current_position), 0.5, self.action_selection)  # get action list from Q matrix

        # override action_list if we do exploration
        if self.do_exploration():
            action_list = self.exp.get_action_list()

        # check actions and get next position and reward
        for action in action_list:
            # get next position
            next_position = self.mov.get_next_position(self.current_position, action)  #  get target position

            # check if we can move to next position
            if self.mov.check_action(self.current_position, action, next_position, self.sen):  # check action if no obstacle is in the way
                self.move(action, next_position)  # move to new location and get reward
                self.step_counter += 1
                break  # do not check any further actions in action_list
            else:
                self.stay(action, next_position)  # stay and get reward
                if self.one_action_per_step:
                    self.step_counter += 1
                    break

        return False, self.current_position

    def move(self, action, next_position):
        # step reward as default
        reward = self.qrl.reward_step

        # check if goal position
        if [next_position[0], next_position[1]] in self.goal_position:  # check if target is goal
            reward = self.qrl.reward_goal

        # update Q matrix
        self.qrl.update_Q_mat(action,
                         self.mov.get_state(self.current_position),
                         self.mov.get_state(next_position),
                         reward)  # update q with reward step

        # update expertness
        self.qrl.expertness = self.qrl.expertness_modul.update_expertness(self)

        # set current position to next position
        self.current_position = next_position

    def stay(self, action, next_position):
        # wall reward as default
        reward = self.qrl.reward_wall

        # check if robot at next position
        if self.robot_at_position(next_position):
            reward = self.qrl.reward_robot

        # update Q matrix
        self.qrl.update_Q_mat(action,
                         self.mov.get_state(self.current_position),
                         self.mov.get_state(next_position),
                         reward)  # update q with reward wall

        # update expertness
        self.qrl.expertness = self.qrl.expertness_modul.update_expertness(self)

    def goal_reached(self):  # function to determine if goal is reached
        if [self.current_position[0], self.current_position[1]] in self.goal_position:
            return True
        return False

    def add_current_position_to_history(self):
        self.traveled_map[self.current_position[0], self.current_position[1], 0] = 1
        self.history.append([self.current_position[0], self.current_position[1]])  # add old position to history

    def do_exploration(self):
        if numpy.random.random_sample(1) < self.exp.get_exploration_rate(self.trial_counter):
            return True
        else:
            return False

    def robot_at_position(self, position):
        is_robot = False
        for agent in self.agent_list:  # check if robot
            if position[0] == agent.current_position[0] and position[1] == agent.current_position[1]:
                is_robot = True
                break
        return is_robot

    def reset(self, start, goal): # reset robot start and goal coordinates
        self.current_position = start
        self.goal_position = goal
        self.step_counter = 0
        self.trial_counter += 1
        self.traveled_map = numpy.zeros(numpy.shape(self.traveled_map), dtype=numpy.float) # map to store already visited locations
        self.traveled_map[:, 0, 0] = 1
        self.traveled_map[:, -1, 0] = 1
        self.traveled_map[0, :, 0] = 1
        self.traveled_map[-1, :, 0] = 1
