import numpy
from src.framework.exploration.baseExploration import BaseExploration


class SmartRandomExploration(BaseExploration):
    def __init__(self):
        pass

    def getActionList(self, basis, actionList):
        action_list = []
        action_list_2 = []
        # get actions to not visited places
        for action in range(basis.mas.nActions()):
            next_pos = basis.mas.getNextPos(basis.current_position, action)
            if basis.traveled_map[next_pos[0], next_pos[1], 0] == 0:
                action_list.append(action)
        numpy.random.shuffle(action_list)
        # get remaining actions
        for action in range(basis.mas.nActions()):
            if action not in action_list:
                action_list_2.append(action)
        numpy.random.shuffle(action_list_2)
        action_list.extend(action_list_2)
        return action_list

    def getExplorationRate(self):
        return self.explorationRate
