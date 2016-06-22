import time
import math
import numpy
from basicRobot import BasicRobot
from operator import add


class Butler(BasicRobot):
    def __init__(self,id,maze,name):
        BasicRobot.__init__(self,id,maze,name)

    def set_q_shared(self,q):
        self.q_m = q