import time
from operator import add

import matplotlib.pyplot as plt


class Simulation:
    def __init__(self,rc,maze):
        self.robot_controller = rc
        self.do_plot = False
        self.refresh_rate = 0
        self.max_iterations = 10000
        self.maze = maze

    def load_maze(self,maze):
        self.maze = maze
        self.robot_controller.maze = self.maze
        self.robot_controller.reset_robots()

    def sim_sensor(self, r):  # simluates sensor of robot r
        r_pos_top = map(add,r.c_p,[-1,0,0])
        r_pos_down = map(add,r.c_p,[1,0,0])
        r_pos_left = map(add,r.c_p,[0,-1,0])
        r_pos_right = map(add,r.c_p,[0,1,0])
        o = r.c_p[2] # orientation
        r.sim_sensor_front = 0
        r.sim_sensor_back = 0
        r.sim_sensor_left = 0
        r.sim_sensor_right = 0

        if self.maze[r_pos_top[0],r_pos_top[1],0] >= 1:
            if o == 0:
                r.sim_sensor_front = 1
            if o == 1:
                r.sim_sensor_left = 1
            if o == 2:
                r.sim_sensor_back = 1
            if o == 3:
                r.sim_sensor_right = 1
        if self.maze[r_pos_right[0],r_pos_right[1],0] >= 1:
            if o == 0:
                r.sim_sensor_right = 1
            if o == 1:
                r.sim_sensor_front = 1
            if o == 2:
                r.sim_sensor_left = 1
            if o == 3:
                r.sim_sensor_back = 1
        if self.maze[r_pos_down[0],r_pos_down[1],0] >= 1:
            if o == 0:
                r.sim_sensor_back = 1
            if o == 1:
                r.sim_sensor_right = 1
            if o == 2:
                r.sim_sensor_front = 1
            if o == 3:
                r.sim_sensor_left = 1
        if self.maze[r_pos_left[0],r_pos_left[1],0] >= 1:
            if o == 0:
                r.sim_sensor_left = 1
            if o == 1:
                r.sim_sensor_back = 1
            if o == 2:
                r.sim_sensor_right = 1
            if o == 3:
                r.sim_sensor_front = 1

    def run_simulation(self):
        if self.do_plot:
            plt.ion()
            plt.figure(figsize=(10, 5))
            plt.imshow(self.maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
            plt.show()
            plt.pause(0.0001)
        step_counter = 0
        while True:
            # do actions
            all_finished = True
            for robot_it in self.robot_controller.robot_list:
                self.sim_sensor(robot_it)   # simulate robot sensor
                if robot_it.make_step():
                    # free current position
                    self.maze[robot_it.c_p[0],robot_it.c_p[1],0] = 0
                else:
                    # traveled map
                    self.robot_controller.traveled_map[robot_it.c_p[0],robot_it.c_p[1],0] += 1
                    # free old position
                    self.maze[robot_it.o_p[0],robot_it.o_p[1],0] = 0
                    # block current position
                    self.maze[robot_it.c_p[0],robot_it.c_p[1],0] = robot_it.id+2
                    all_finished = False
            if self.do_plot:
                plt.clf()
                plt.imshow(self.maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
                plt.show()
                plt.pause(0.00001)
            step_counter += 1
            if all_finished:
                return step_counter

    def do_animation(self):
        pass

