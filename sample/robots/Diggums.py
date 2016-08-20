import time
import math
import numpy
from basicRobot import BasicRobot
from operator import add

""" Simple Q-learning agent
    States: (y,x,o) | Actions: Forward = 0 , Right = 1, Backwards = 2, Left = 3
"""


class Diggums(BasicRobot):
    def __init__(self,id,maze,name):
        BasicRobot.__init__(self,id, maze, name)
        self.q_m = numpy.zeros((4*self.rows*self.columns,4),dtype=numpy.float)

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
    
    def getNextPos(self, current_position, r_action): # get next position for q action
        target_pos = []
        if self.current_position[2] == 0:
            y = -1
            x = +1
            if r_action == 0:
                target_pos = map(add,self.current_position,[y,0,0])
                target_pos[2] = 0
            elif r_action == 1:
                target_pos = map(add,self.current_position,[0,x,0])
                target_pos[2] = 1
            elif r_action == 2:
                target_pos = map(add,self.current_position,[-1*y,0,0])
                target_pos[2] = 2
            elif r_action == 3:
                target_pos = map(add,self.current_position,[0,-1*x,0])
                target_pos[2] = 3
            else:
                target_pos = self.current_position
        elif self.current_position[2] == 2:
            y = +1
            x = -1
            if r_action == 0:
                target_pos = map(add,self.current_position,[y,0,0])
                target_pos[2] = 2
            elif r_action == 1:
                target_pos = map(add,self.current_position,[0,x,0])
                target_pos[2] = 3
            elif r_action == 2:
                target_pos = map(add,self.current_position,[-1*y,0,0])
                target_pos[2] = 0
            elif r_action == 3:
                target_pos = map(add,self.current_position,[0,-1*x,0])
                target_pos[2] = 1
            else:
                target_pos = self.current_position
        elif self.current_position[2] == 1:
            y = +1
            x = +1
            if r_action == 0:
                target_pos = map(add,self.current_position,[0,x,0])
                target_pos[2] = 1
            elif r_action == 1:
                target_pos = map(add,self.current_position,[y,0,0])
                target_pos[2] = 2
            elif r_action == 2:
                target_pos = map(add,self.current_position,[0,-1*x,0])
                target_pos[2] = 3
            elif r_action == 3:
                target_pos = map(add,self.current_position,[-1*y,0,0])
                target_pos[2] = 0
            else:
                target_pos = self.current_position
        elif self.current_position[2] == 3:
            y = -1
            x = -1
            if r_action == 0:
                target_pos = map(add,self.current_position,[0,x,0])
                target_pos[2] = 3
            elif r_action == 1:
                target_pos = map(add,self.current_position,[y,0,0])
                target_pos[2] = 0
            elif r_action == 2:
                target_pos = map(add,self.current_position,[0,-1*x,0])
                target_pos[2] = 1
            elif r_action == 3:
                target_pos = map(add,self.current_position,[-1*y,0,0])
                target_pos[2] = 2
            else:
                target_pos = self.current_position
        return target_pos

    def set_q_shared(self,q):
        self.q_m = q