from abc import ABCMeta, abstractmethod


class Weighting(object):
    __metaclass__ = ABCMeta

    def get_weighting(self, student, teacher, agent_list):
        return 1
