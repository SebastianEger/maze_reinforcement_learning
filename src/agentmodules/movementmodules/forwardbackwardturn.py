import numpy

from src.framework.movement import Movement


class ForwardBackwardTurn(Movement):
    def __init__(self, maze_size):
        self.rows = maze_size[0]
        self.columns = maze_size[1]
        self.n_actions = 3
        self.n_states = 4*self.rows*self.columns
        # 0 = Forward
        # 3 = Backward
        # 1 = Turn Right
        # 2 = Turn Left

    def check_action(self, current_position, action, next_position, sensors):
        if action == 0 and sensors.sim_sensor_front == 1:
            return False
        if action == 1 and sensors.sim_sensor_back == 1:
            return False
        return True

    def get_next_position(self, current_position, action):
        next_position = [0, 0, 0]
        next_position[:] = current_position[:]

        if action == 0:
            if current_position[2] == 0:
                next_position[0] -= 1
            if current_position[2] == 1:
                next_position[1] += 1
            if current_position[2] == 2:
                next_position[0] += 1
            if current_position[2] == 3:
                next_position[1] -= 1
        if action == 4:
            if current_position[2] == 0:
                next_position[0] += 1
            if current_position[2] == 1:
                next_position[1] -= 1
            if current_position[2] == 2:
                next_position[0] -= 1
            if current_position[2] == 3:
                next_position[1] += 1
        if action == 1:
            next_position[2] += 1
        if action == 2:
            next_position[2] -= 1

        if next_position[2] < 0:
            next_position[2] = 3
        if next_position[2] > 3:
            next_position[2] = 0

        return next_position

    def get_state(self, position):
        return position[2]*self.rows*self.columns + position[1]*self.rows+position[0]
