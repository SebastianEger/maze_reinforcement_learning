from src.framework.weighting import Weighting


class LearnFromAll(Weighting):
    def __init__(self):
        pass

    def get_weighting(self, agent, agent_list):
        sum_expertness = 0

        for agent_it in agent_list:
            sum_expertness += agent_it.qrl.expertness

        return float(agent.qrl.expertness) / float(sum_expertness)


class LearnFromAllPositive(Weighting):
    def __init__(self):
        pass

    def get_weighting(self, agent, agent_list):
        e_min = None
        c = 0
        denominator = 0

        # get min expertness
        for agent_it in agent_list:
            if e_min is None:
                e_min = agent_it.qrl.expertness
            else:
                if e_min > agent_it.qrl.expertness:
                    e_min = agent_it.qrl.expertness

        for agent_it in agent_list:
            denominator += (agent_it.qrl.expertness - e_min + c)

        return float(agent.qrl.expertness - e_min + c) / float(denominator)

