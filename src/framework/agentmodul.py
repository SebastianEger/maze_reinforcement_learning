from abc import ABCMeta, abstractmethod


class AgentModul(object):
    __metaclass__ = ABCMeta

    mov = None
    qrl = None
    exp = None
    agt = None

    def init_agent_modules(self, agent):
        self.agt = agent
        self.mov = agent.mov
        self.qrl = agent.qrl
        self.exp = agent.exp
        self.sen = agent.sen
