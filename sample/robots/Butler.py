import time
import math
import numpy
from step_robot import StepRobot
from operator import add


class Butler(StepRobot):
    def __init__(self,id,maze,name):
        StepRobot.__init__(self,id,maze,name)

    def set_q_shared(self,q):
        self.q_m = q