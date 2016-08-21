from sample.framework.basicQlearning import BasicQlearning


class FolQLearning(BasicQlearning):
    def __init__(self, ms, maze):
        BasicQlearning.__init__(self, ms, maze)

    def computeExpertness(self):
        return self.parent.q.expertness+self.parent.q.lastReward

    def computeWeight(self):
        expertness_sum = 0
        for robot in self.parent.robot_list:
            expertness_sum += robot.q.expertness

        if expertness_sum == 0:
            return 1

        return self.parent.q.expertness/expertness_sum


