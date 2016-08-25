import time
from random import shuffle
from operator import add

import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, rc, maze):
        self.robot_controller = rc
        self.cooperationTime = -1
        self.do_plot = False
        self.refresh_rate = 0
        self.max_iterations = 3000
        self.maze = maze

    def load_maze(self, maze):
        self.maze = maze
        self.robot_controller.maze = self.maze
        self.robot_controller.reset_robots()

    def run_simulation(self, numberTrials=1, PB=None):
        data = []
        coop_counter = 0
        if self.do_plot:
            self.initPlot()
        for curTrial in xrange(numberTrials):
            self.robot_controller.reset_robots()
            step_counter = 0
            while True:
                # do actions
                all_finished = True
                # shuffle(self.robot_controller.robot_list)
                for robot_it in self.robot_controller.robot_list:
                    robot_it.simSensors(robot_it.current_position, self.maze)   # simulate robot sensor
                    oldPosition = robot_it.current_position
                    goalReached, newPosition = robot_it.makeStep()

                    if goalReached:
                        # free goal position
                        self.maze[newPosition[0], newPosition[1], 0] = 0
                    else:
                        # traveled map
                        self.robot_controller.traveled_map[robot_it.current_position[0], robot_it.current_position[1], 0] += 1
                        # free old position
                        self.maze[oldPosition[0], oldPosition[1], 0] = 0
                        # block current position
                        self.maze[robot_it.current_position[0], robot_it.current_position[1], 0] = robot_it.id+2
                        # at least one robot has not finished
                        all_finished = False
                if self.do_plot:
                    self.showCurMaze()
                step_counter += 1
                if all_finished:
                    data.append(step_counter)
                    break
                if step_counter > self.max_iterations:
                    print "Too many iterations! Execution stopped!"
                    break
            coop_counter += 1
            if coop_counter == self.cooperationTime:
                print "Exchanging Q matrices"
                self.robot_controller.cmd("do_coop_learning")
                coop_counter = 0
            if PB:
                PB["value"] = curTrial+1
                PB.update_idletasks()
        return data

    def do_animation(self):
        pass

    def initPlot(self):
        plt.ion()
        plt.figure(figsize=(10, 5))
        plt.imshow(self.maze[:, :, 0], cmap=plt.cm.binary, interpolation='nearest')
        plt.show()
        plt.pause(0.0001)

    def showCurMaze(self):
        plt.clf()
        plt.imshow(self.maze[:, :, 0], cmap=plt.cm.binary, interpolation='nearest')
        plt.show()
        plt.pause(0.00001)
