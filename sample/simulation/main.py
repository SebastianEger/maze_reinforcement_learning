import matplotlib.pyplot as plt
import mazes.maze as maze_gen
import mazes.maze_depth_first as maze_dfs
import mazes.maze_generator as maze_static
import robot_controller
import simulation

plt.figure(figsize=(10, 10))

#maze = maze_bin.maze_dfs(10,10,True)
maze = maze_gen.maze(20,20,density=0.2)
#maze = maze_generator.get_static_maze_2()
plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
plt.show()
rc1 = robot_controller.RobotController(5,maze,1)
rc1.set_exploration_rate(0)

sim1 = simulation.Simulation(rc1,maze)
sim1.do_plot = False
sim1.refresh_rate = 0.0

rc2 = robot_controller.RobotController(5,maze,2)
rc2.set_exploration_rate(0)

sim2 = simulation.Simulation(rc2,maze)
sim2.do_plot = False
sim2.refresh_rate = 0.0

data1 = []
data2 = []
iterations = 500

for i in xrange(iterations):
    rc1.reset_robots()
    data1.append(sim1.run_simulation())
    print float(i)/float(iterations)
i = 0
for i in xrange(iterations):
    rc2.reset_robots()
    data2.append(sim2.run_simulation())
    print float(i)/float(iterations)

plt.plot(data1, color='b')
plt.plot(data2, color='r')
plt.show()