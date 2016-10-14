from abc import ABCMeta, abstractmethod
from src.framework.agentmodul import AgentModul


class Expertness(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_expertness(self, agent):
        pass
