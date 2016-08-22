from sample.framework.baseExploration import BaseExploration
import numpy


class AdvExploration(BaseExploration):
    def __init__(self, basis, maze):
        BaseExploration.__init__(self, basis)

    def explore(self, actionList):
        if numpy.random.random_sample(1) < self.getExplorationRate():
            action_list = []
            action_list_2 = []
            # get actions to not visited places
            for action in range(self.basis.nActions):
                next_pos = self.basis.getNextPos(self.basis.current_position, action)
                if self.basis.traveled_map[next_pos[0], next_pos[1], 0] == 0:
                    action_list.append(action)
            numpy.random.shuffle(action_list)
            # get remaining actions
            for action in range(self.basis.nActions):
                if action not in action_list:
                    action_list_2.append(action)
            numpy.random.shuffle(action_list_2)
            action_list.extend(action_list_2)
            return action_list
        else:
            return actionList

    def getExplorationRate(self):
        return self.exploration_rate