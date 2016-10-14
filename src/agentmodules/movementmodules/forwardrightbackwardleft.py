import numpy

from src.framework.movement import Movement


class ForwardRightBackwardLeft(Movement):
    def __init__(self, maze_size):
        self.rows = maze_size[0]
        self.columns = maze_size[1]
        self.n_actions = 4
        self.n_states = 4*self.rows*self.columns
        # 0 = Forward
        # 1 = Right
        # 2 = Backward
        # 3 = Left

    def check_action(self, current_position, action, next_position, sensors):
        if action == 0 and sensors.sim_sensor_front == 1:
            return False
        if action == 1 and sensors.sim_sensor_right == 1:
            return False
        if action == 2 and sensors.sim_sensor_back == 1:
            return False
        if action == 3 and sensors.sim_sensor_left == 1:
            return False
        return True

    def get_next_position(self, current_position, action):
        nextPosition = [0, 0, 0]
        nextPosition[:] = current_position[:]

        if action == 0:
            if current_position[2] == 0:
                nextPosition[0] -= 1
            if current_position[2] == 1:
                nextPosition[1] += 1
            if current_position[2] == 2:
                nextPosition[0] += 1
            if current_position[2] == 3:
                nextPosition[1] -= 1
        if action == 1:
            if current_position[2] == 0:
                nextPosition[1] += 1
            if current_position[2] == 1:
                nextPosition[0] += 1
            if current_position[2] == 2:
                nextPosition[1] -= 1
            if current_position[2] == 3:
                nextPosition[0] -= 1
            nextPosition[2] += 1
        if action == 2:
            if current_position[2] == 0:
                nextPosition[0] += 1
            if current_position[2] == 1:
                nextPosition[1] -= 1
            if current_position[2] == 2:
                nextPosition[0] -= 1
            if current_position[2] == 3:
                nextPosition[1] += 1
            nextPosition[2] += 2
        if action == 3:
            if current_position[2] == 0:
                nextPosition[1] -= 1
            if current_position[2] == 1:
                nextPosition[0] -= 1
            if current_position[2] == 2:
                nextPosition[1] += 1
            if current_position[2] == 3:
                nextPosition[0] += 1
            nextPosition[2] -= 1

        if nextPosition[2] < 0:
            nextPosition[2] += 4
        if nextPosition[2] > 3:
            nextPosition[2] -= 4

        # print current_position, action, nextPosition
        return nextPosition

    def get_state(self, position):
        return position[2]*self.rows*self.columns + position[1]*self.rows+position[0]
