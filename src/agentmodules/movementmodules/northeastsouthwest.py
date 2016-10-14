import numpy

from operator import add

from src.framework.movement import Movement


# converts action (North, East, South, West) to direction (Forward, Left, Backwards, Right)
def get_direction(current_position, action):
        if current_position[2] == 0:
            if action == 0:
                return 0
            elif action == 2:
                return 2
            if action == 3:
                return 3
            elif action == 1:
                return 1
        elif current_position[2] == 2:
            if action == 0:
                return 2
            elif action == 2:
                return 0
            if action == 3:
                return 1
            elif action == 1:
                return 3
        elif current_position[2] == 1:
            if action == 0:
                return 3
            elif action == 2:
                return 1
            if action == 3:
                return 2
            elif action == 1:
                return 0
        elif current_position[2] == 3:
            if action == 0:
                return 1
            elif action == 2:
                return 3
            if action == 3:
                return 0
            elif action == 1:
                return 2
        return 4  # wait


class NorthEastSouthWest(Movement):
    def __init__(self, maze_size):
        self.rows = maze_size[0]
        self.columns = maze_size[1]
        self.n_actions = 4  # 0 = North, 1 = East, 2 = South, 3 = West
        self.n_states = self.rows*self.columns

    def get_next_position(self, current_position, action):  # returns position after q_action
        if action == 0:
            target_pos = map(add, current_position, [-1,0,0])
            target_pos[2] = 0
        elif action == 1:
            target_pos = map(add, current_position, [0,+1,0])
            target_pos[2] = 1
        elif action == 2:
            target_pos = map(add, current_position, [+1,0,0])
            target_pos[2] = 2
        elif action == 3:
            target_pos = map(add, current_position, [0,-1,0])
            target_pos[2] = 3
        else:
            target_pos = current_position
        return target_pos

    def get_state(self, position):  # get current state
        return position[1]*self.rows + position[0]

    def check_action(self, current_position, action, next_position, sensors): # checks action
        direction = get_direction(current_position, action)
        # check all sensor if there is a wall
        if direction == 0:
            if sensors.sim_sensor_front == 1:
                return False
        if direction == 1:
            if sensors.sim_sensor_right == 1:
                return False
        if direction == 2:
            if sensors.sim_sensor_back == 1:
                return False
        if direction == 3:
            if sensors.sim_sensor_left == 1:
                return False
        # if way is free, return true
        return True

