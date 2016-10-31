from src.framework.weighting import Weighting


class LearnFromAll(Weighting):
    def __init__(self):
        pass

    def get_weighting(self, student, teacher, agent_list):
        sum_expertness = 0

        for agent_it in agent_list:
            sum_expertness += agent_it.qrl.expertness

        return float(teacher.qrl.expertness) / float(sum_expertness)


class LearnFromAllPositive(Weighting):
    def __init__(self):
        pass

    def get_weighting(self, student, teacher, agent_list):
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

        return float(teacher.qrl.expertness - e_min + c) / float(denominator)


class LearningFromExperts(Weighting):

    def __init__(self):
        pass

    def get_weighting(self, student, teacher, agent_list):
        alpha = 0.9

        # i == j
        if student.info['id'] == teacher.info['id']:
            return 1 - alpha

        # ej > ei
        if teacher.qrl.expertness > student.qrl.expertness:
            d = 0

            for agent in agent_list:
                d += agent.qrl.expertness - student.qrl.expertness

            return alpha * float(teacher.qrl.expertness - student.qrl.expertness) / d

        # otherwise
        return 0
