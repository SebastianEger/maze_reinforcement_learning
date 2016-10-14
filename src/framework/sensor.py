from operator import add

class Sensor(object):
    sim_sensor_front = 0
    sim_sensor_back = 0
    sim_sensor_left = 0
    sim_sensor_right = 0

    def __init__(self):
        pass

    def sim_sensors(self, current_position, maze):
        r_pos_top = map(add, current_position,[-1,0,0])
        r_pos_down = map(add, current_position,[1,0,0])
        r_pos_left = map(add, current_position,[0,-1,0])
        r_pos_right = map(add, current_position,[0,1,0])
        o = current_position[2]  # orientation
        self.sim_sensor_front = 0
        self.sim_sensor_back = 0
        self.sim_sensor_left = 0
        self.sim_sensor_right = 0

        if maze[r_pos_top[0], r_pos_top[1], 0] >= 1:
            if o == 0:
                self.sim_sensor_front = 1
            if o == 1:
                self.sim_sensor_left = 1
            if o == 2:
                self.sim_sensor_back = 1
            if o == 3:
                self.sim_sensor_right = 1
        if maze[r_pos_right[0], r_pos_right[1], 0] >= 1:
            if o == 0:
                self.sim_sensor_right = 1
            if o == 1:
                self.sim_sensor_front = 1
            if o == 2:
                self.sim_sensor_left = 1
            if o == 3:
                self.sim_sensor_back = 1
        if maze[r_pos_down[0],r_pos_down[1],0] >= 1:
            if o == 0:
                self.sim_sensor_back = 1
            if o == 1:
                self.sim_sensor_right = 1
            if o == 2:
                self.sim_sensor_front = 1
            if o == 3:
                self.sim_sensor_left = 1
        if maze[r_pos_left[0],r_pos_left[1],0] >= 1:
            if o == 0:
                self.sim_sensor_left = 1
            if o == 1:
                self.sim_sensor_back = 1
            if o == 2:
                self.sim_sensor_right = 1
            if o == 3:
                self.sim_sensor_front = 1
