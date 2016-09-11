import src.robots.robotController
from src.mazes import random_maze

maze = random_maze.maze(10,10)
rc = src.robots.robotController.RobotController(1, maze, "Holly")
sim = src.simulation.Simulation(rc, maze)
sim.do_plot = False

for i in xrange(100):
    sim.run()
    maze = random_maze.maze(10,10)
    sim.maze = maze
    rc.maze = maze
    rc.reset_robots()

rc.robot_list[0].use_learning = True
sim.do_plot = True
sim.run()

print rc.robot_list[0].q_m
