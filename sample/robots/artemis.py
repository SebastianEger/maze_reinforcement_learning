import time
import math
import numpy
from basicRobot import BasicRobot
from operator import add


class Artemis(BasicRobot):
    def __init__(self,id,maze,name):
        BasicRobot.__init__(self,id,maze,name)