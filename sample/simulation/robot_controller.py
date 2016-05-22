import robot
import numpy
import simulation
import maze_generator
import matplotlib.pyplot as plt


class RobotController:

    def __init__(self, number, maze, run_mode):
        self.number_robots = number
        self.maze = maze
        self.maze_shape = numpy.shape(maze)
        self.run_mode = 0   # 0 = stepwise
        self.robot_list = []
        self.traveled_map = numpy.zeros(self.maze_shape,dtype=numpy.uint8)
        for _ in xrange(number):
            new_robot = robot.Robot(_)
            new_robot.current_position = [1,1,2]
            new_robot.goal_position = [self.maze_shape[0]-2,self.maze_shape[1]-2]
            new_robot.init_q_matrix(maze)
            new_robot.traveled_map = self.traveled_map
            maze[new_robot.current_position[0],new_robot.current_position[1],0] = 1
            self.robot_list.append(new_robot)
        for _ in self.robot_list:
            _.robot_list = self.robot_list

    def add_robot(self):
        new_robot = robot.Robot(self.number_robots+1)
        self.number_robots += 1
        self.robot_list.append(new_robot)

    def reset_robots(self):
        i = 0
        self.traveled_map = numpy.zeros(numpy.shape(self.traveled_map),dtype=numpy.uint8)
        for _ in self.robot_list:
            _.traveled_map = self.traveled_map
            self.maze[_.current_position[0],_.current_position[1],0] = 0
            _.current_position = [1,1,2]
            _.goal_position = [self.maze_shape[0]-2,self.maze_shape[1]-2]
            self.maze[_.current_position[0],_.current_position[1],0] = 1
            i += 1

    def set_exploration_mode(self,mode):
        for _ in self.robot_list:
            _.exploration_mode = mode

    def set_exploration_rate(self,rate):
        for _ in self.robot_list:
            _.exploration_rate = rate


if __name__ == '__main__':

    maze = maze_generator.get_static_maze_1()
    rc = RobotController(3,maze,0)
    sim = simulation.Simulation(rc,maze)
    sim.refresh_rate = 0
    sim.do_plot = False
    print sim.run_simulation()
    plt.figure(figsize=(10, 10))
    plt.imshow(rc.robot_list[0].traveled_map[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    print rc.robot_list[0].traveled_map[:,:,0]
    y,x = zip(*rc.robot_list[0].history)
    plt.scatter(x,y, color='b', alpha=0.2,)
    plt.show()
