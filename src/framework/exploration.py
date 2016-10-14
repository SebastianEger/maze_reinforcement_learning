from abc import ABCMeta, abstractmethod
from src.framework.agentmodul import AgentModul


class Exploration(AgentModul):
    __metaclass__ = ABCMeta

    exploration_rate = 0

    @abstractmethod
    def get_action_list(self):
        pass

    @abstractmethod
    def get_exploration_rate(self):
        pass
