from src.framework.expertness import Expertness


class Absolute(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        if agent.qrl.last_reward > agent.qrl.reward_wall:
            return agent.qrl.expertness + abs(agent.qrl.last_reward)
        else:
            return agent.qrl.expertness


class Normal(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        if agent.qrl.last_reward > agent.qrl.reward_wall:
            return agent.qrl.expertness + agent.qrl.last_reward
        else:
            return agent.qrl.expertness


class Positive(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        if agent.qrl.last_reward > 0:
            return agent.qrl.expertness + agent.qrl.last_reward
        else:
            return agent.qrl.expertness


class DistToGoal(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        return 1/float(self.distance_to_goal(agent) + 1)

    def distance_to_goal(self, agent):
        dx = abs(agent.current_position[0] - agent.goal_position[0][0])
        dy = abs(agent.current_position[1] - agent.goal_position[0][1])

        return dx+dy


class NeededSteps(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        return float(agent.step_counter)

class AllTheSame(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        return 1
