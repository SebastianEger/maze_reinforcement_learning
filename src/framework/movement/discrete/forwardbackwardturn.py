import numpy

from src.framework.movement.baseMovement import BaseMovementAndSensors


class ForwardBackwardTurn(BaseMovementAndSensors):
    def __init__(self, maze):
        self.rows, self.columns, self.dims = numpy.shape(maze)
        self.nActions = 3
        self.nStates = 4*self.rows*self.columns
        # 0 = Forward
        # 3 = Backward
        # 1 = Turn Right
        # 2 = Turn Left

    def checkAction(self, current_position, action, next_position, sensors):
        if action == 0 and sensors.sim_sensor_front == 1:
            return False
        if action == 1 and sensors.sim_sensor_back == 1:
            return False
        return True

    def getNextPos(self, current_position, action):
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
        if action == 4:
            if current_position[2] == 0:
                nextPosition[0] += 1
            if current_position[2] == 1:
                nextPosition[1] -= 1
            if current_position[2] == 2:
                nextPosition[0] -= 1
            if current_position[2] == 3:
                nextPosition[1] += 1
        if action == 1:
            nextPosition[2] += 1
        if action == 2:
            nextPosition[2] -= 1

        if nextPosition[2] < 0:
            nextPosition[2] = 3
        if nextPosition[2] > 3:
            nextPosition[2] = 0

        return nextPosition

    def getState(self, position):
        return position[2]*self.rows*self.columns + position[1]*self.rows+position[0]
