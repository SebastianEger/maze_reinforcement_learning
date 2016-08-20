import math
from basicRobot import BasicRobot


# Expertness: Inverse Distance to Goal (IDG)
# Weight Calculation: Learning From All
class Foaly(BasicRobot):
    def __init__(self, id, maze, name):
        BasicRobot.__init__(self, id, maze, name)
        self.dist_start_goal = 0

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
        return 1/self.dist_to_goal()

    def dist_to_goal(self):
        y_diff = math.fabs(self.c_p[0]-self.goal_position[0])
        x_diff = math.fabs(self.c_p[1]-self.goal_position[1])
        return x_diff + y_diff

    def set_dist_start_goal(self):
        self.dist_start_goal = self.dist_to_goal()