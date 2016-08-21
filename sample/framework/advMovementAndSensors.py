from operator import add
from sample.framework.baseMovementAndSensors import BaseMovementAndSensors
import numpy


class AdvMovementAndSensors(BaseMovementAndSensors):
    def __init__(self, basis, maze):
        BaseMovementAndSensors.__init__(self, basis)
        self.rows, self.columns, self.dims = numpy.shape(maze)
        self.nActions = 4  # 0 = North, 1 = East, 2 = South, 3 = West
        self.nStates = 4*self.rows*self.columns
        self.sim_sensor_front = 0  # if there is a wall in front, sensor = 1, robot = 2, nothing = 0
        self.sim_sensor_back = 0
        self.sim_sensor_left = 0
        self.sim_sensor_right = 0
        self.sim_sensor_goal = 0  # goal = 1, no goal insight = 0

    def getNextPos(self, current_position, action): # get next position for q action
        target_pos = []
        if current_position[2] == 0:
            y = -1
            x = +1
            if action == 0:
                target_pos = map(add,current_position,[y,0,0])
                target_pos[2] = 0
            elif action == 1:
                target_pos = map(add,current_position,[0,x,0])
                target_pos[2] = 1
            elif action == 2:
                target_pos = map(add,current_position,[-1*y,0,0])
                target_pos[2] = 2
            elif action == 3:
                target_pos = map(add,current_position,[0,-1*x,0])
                target_pos[2] = 3
            else:
                target_pos = current_position
        elif current_position[2] == 2:
            y = +1
            x = -1
            if action == 0:
                target_pos = map(add,current_position,[y,0,0])
                target_pos[2] = 2
            elif action == 1:
                target_pos = map(add,current_position,[0,x,0])
                target_pos[2] = 3
            elif action == 2:
                target_pos = map(add,current_position,[-1*y,0,0])
                target_pos[2] = 0
            elif action == 3:
                target_pos = map(add,current_position,[0,-1*x,0])
                target_pos[2] = 1
            else:
                target_pos = current_position
        elif current_position[2] == 1:
            y = +1
            x = +1
            if action == 0:
                target_pos = map(add,current_position,[0,x,0])
                target_pos[2] = 1
            elif action == 1:
                target_pos = map(add,current_position,[y,0,0])
                target_pos[2] = 2
            elif action == 2:
                target_pos = map(add,current_position,[0,-1*x,0])
                target_pos[2] = 3
            elif action == 3:
                target_pos = map(add,current_position,[-1*y,0,0])
                target_pos[2] = 0
            else:
                target_pos = current_position
        elif current_position[2] == 3:
            y = -1
            x = -1
            if action == 0:
                target_pos = map(add,current_position,[0,x,0])
                target_pos[2] = 3
            elif action == 1:
                target_pos = map(add,current_position,[y,0,0])
                target_pos[2] = 0
            elif action == 2:
                target_pos = map(add,current_position,[0,-1*x,0])
                target_pos[2] = 1
            elif action == 3:
                target_pos = map(add,current_position,[-1*y,0,0])
                target_pos[2] = 2
            else:
                target_pos = current_position
        return target_pos

    def getState(self, position):
        return position[2]*self.rows*self.columns + position[1]*self.rows+position[0]

    def checkAction(self, current_position, directionToMove): # checks q action
        # check all sensor if there is a wall
        if directionToMove == 0:
            if self.sim_sensor_front == 1:
                return False
        if directionToMove == 1:
            if self.sim_sensor_right == 1:
                return False
        if directionToMove == 2:
            if self.sim_sensor_back == 1:
                return False
        if directionToMove == 3:
            if self.sim_sensor_left == 1:
                return False
        # if all sensor are false return true
        return True
    
    def simSensors(self, current_position, maze):
        r_pos_top = map(add,current_position,[-1,0,0])
        r_pos_down = map(add,current_position,[1,0,0])
        r_pos_left = map(add,current_position,[0,-1,0])
        r_pos_right = map(add,current_position,[0,1,0])
        o = current_position[2] # orientation
        self.sim_sensor_front = 0
        self.sim_sensor_back = 0
        self.sim_sensor_left = 0
        self.sim_sensor_right = 0

        if maze[r_pos_top[0],r_pos_top[1],0] >= 1:
            if o == 0:
                self.sim_sensor_front = 1
            if o == 1:
                self.sim_sensor_left = 1
            if o == 2:
                self.sim_sensor_back = 1
            if o == 3:
                self.sim_sensor_right = 1
        if maze[r_pos_right[0],r_pos_right[1],0] >= 1:
            if o == 0:
                self.sim_sensor_right = 1
            if o == 1:
                self.sim_sensor_front = 1
            if o == 2:
                self.sim_sensor_left = 1
            if o == 3:
                self.sim_sensor_back = 1
        if maze[r_pos_down[0],r_pos_down[1],0] >= 1:
            if o == 0:
                self.sim_sensor_back = 1
            if o == 1:
                self.sim_sensor_right = 1
            if o == 2:
                self.sim_sensor_front = 1
            if o == 3:
                self.sim_sensor_left = 1
        if maze[r_pos_left[0],r_pos_left[1],0] >= 1:
            if o == 0:
                self.sim_sensor_left = 1
            if o == 1:
                self.sim_sensor_back = 1
            if o == 2:
                self.sim_sensor_right = 1
            if o == 3:
                self.sim_sensor_front = 1