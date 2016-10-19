from abc import ABCMeta, abstractmethod


class Weighting(object):
    __metaclass__ = ABCMeta

    def get_weighting(self, agent, agent_list):
        return 1
