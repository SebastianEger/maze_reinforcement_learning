from abc import ABCMeta, abstractmethod
from package.framework.agentmodul import AgentModul


class Exploration(AgentModul):
    __metaclass__ = ABCMeta

    exploration_rate = 0
    exploration_type = 'constant'

    @abstractmethod
    def get_action_list(self):
        pass

    def get_exploration_rate(self, current_trial):
        if self.exploration_type == 'Constant':
            return self.exploration_rate
        elif self.exploration_type == '1/(trial+1)':
            return float(self.exploration_rate)/(float(current_trial) + 1)
