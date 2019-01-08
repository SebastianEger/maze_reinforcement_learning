import numpy

from package.framework.exploration import Exploration


class Random(Exploration):
    def get_action_list(self):
        action_list = []
        for action in range(self.mov.n_actions):
            action_list.append(action)
        numpy.random.shuffle(action_list)
        return action_list


class SmartRandom(Exploration):
    def get_action_list(self):
        new_action_list = []
        new_action_list_2 = []

        # get actions to not visited places
        for action in range(self.mov.n_actions):
            next_pos = self.mov.get_next_position(self.agt.current_position, action)
            if self.agt.traveled_map[next_pos[0], next_pos[1], 0] == 0:
                new_action_list.append(action)
        numpy.random.shuffle(new_action_list)

        # get remaining actions
        for action in range(self.mov.n_actions):
            if action not in new_action_list:
                new_action_list_2.append(action)
        numpy.random.shuffle(new_action_list_2)
        new_action_list.extend(new_action_list_2)
        return new_action_list
