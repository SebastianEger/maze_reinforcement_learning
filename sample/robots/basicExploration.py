import numpy


class BasicExploration:
    def __init__(self):
        self.exploration_rate = 0

    def explore(self):
        action_list = []
        for action in range(4):
            action_list.append(action)
        numpy.random.shuffle(action_list)