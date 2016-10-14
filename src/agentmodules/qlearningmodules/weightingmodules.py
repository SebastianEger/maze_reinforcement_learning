from src.framework.weighting import Weighting


class LearnFromAll(Weighting):
    def __init__(self):
        pass

    def get_weighting(self, expertness, agent_list):
        sum_expertness = 0

        for agent in agent_list:
            sum_expertness += agent.qrl.expertness

        return float(expertness) / float(sum_expertness)
