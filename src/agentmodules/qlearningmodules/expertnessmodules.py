from src.framework.expertness import Expertness


class Absolute(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        return agent.qrl.expertness + abs(agent.qrl.last_reward)

class Normal(Expertness):
    def __init__(self):
        pass

    def update_expertness(self, agent):
        return agent.qrl.expertness + agent.qrl.last_reward
