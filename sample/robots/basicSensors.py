class BasicSensors:
    def __init__(self):
        self.sim_sensor_front = 0  # if there is a wall in front, sensor = 1, robot = 2, nothing = 0
        self.sim_sensor_back = 0
        self.sim_sensor_left = 0
        self.sim_sensor_right = 0
        self.sim_sensor_goal = 0  # goal = 1, no goal insight = 0

    def check_action(self, c_p, q_action): # checks q action
        # transform q action to robot action
        r_action = self.transform_q_action(c_p, q_action)
        # check all sensor if there is a wall
        if r_action == 0:
            if self.sim_sensor_front == 1:
                return False
        if r_action == 1:
            if self.sim_sensor_right == 1:
                return False
        if r_action == 2:
            if self.sim_sensor_back == 1:
                return False
        if r_action == 3:
            if self.sim_sensor_left == 1:
                return False
        # if way is free, return true
        return True
        pass

    def transform_q_action(self, c_p, q_action):
        if c_p[2] == 0:
            if q_action == 0:
                return 0
            elif q_action == 2:
                return 2
            if q_action == 3:
                return 3
            elif q_action == 1:
                return 1
        elif c_p[2] == 2:
            if q_action == 0:
                return 2
            elif q_action == 2:
                return 0
            if q_action == 3:
                return 1
            elif q_action == 1:
                return 3
        elif c_p[2] == 1:
            if q_action == 0:
                return 3
            elif q_action == 2:
                return 1
            if q_action == 3:
                return 2
            elif q_action == 1:
                return 0
        elif c_p[2] == 3:
            if q_action == 0:
                return 1
            elif q_action == 2:
                return 3
            if q_action == 3:
                return 0
            elif q_action == 1:
                return 2
        return 4  # wait