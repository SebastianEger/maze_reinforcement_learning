from abc import ABCMeta, abstractmethod
from package.framework.agentmodul import AgentModul


class Movement(AgentModul):
    __metaclass__ = ABCMeta

    n_states = None
    n_actions = None

    @abstractmethod
    def get_next_position(self, current_position, action):
        pass

    @abstractmethod
    def check_action(self, current_position, action, next_position, sensors):
        pass

    @abstractmethod
    def get_state(self, position):
        pass


