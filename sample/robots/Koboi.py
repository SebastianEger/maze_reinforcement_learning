from sample.framework.basicRobot import BasicRobot


# Expertness: Normal
# Weight Calculation: Learning From All
class Koboi(BasicRobot):
    def __init__(self, id, maze, name):
        BasicRobot.__init__(self, id, maze, name)

    def set_q_shared(self,q):
        self.q_m = q

    def compute_weight(self):
        expertness_sum = 0
        for robot in self.robot_list:
            expertness_sum += robot.expertness

        if expertness_sum == 0:
            return 1

        return self.expertness/expertness_sum

    def compute_expertness(self):
        return self.expertness+self.last_reward