import time
import math
import numpy
from step_robot import StepRobot
from operator import add


class Artemis(StepRobot):
    def __init__(self,id,maze,name):
        StepRobot.__init__(self,id,maze,name)