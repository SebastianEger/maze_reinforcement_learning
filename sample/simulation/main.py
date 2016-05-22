import simulation
import robot_controller
import maze_generator
import maze as maze_gen
import maze_depth_first as maze_bin
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))

maze = maze_bin.generate_maze(10,10,True)
maze = maze_gen.maze(30,30)
plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
plt.show()
rc = robot_controller.RobotController(10,maze,0)
rc.set_exploration_mode(1)
rc.set_exploration_rate(0)

sim = simulation.Simulation(rc,maze)
sim.do_plot = False
sim.refresh_rate = 0.0

data = []
iterations = 250

for i in xrange(iterations):
    rc.reset_robots()
    data.append(sim.run_simulation())
    print float(i)/float(iterations)

plt.subplot(211)
plt.plot(data)
data = []

data.append(sim.run_simulation())
print float(i)/float(iterations)

for _ in rc.robot_list:
    print _.expertness_nrm
plt.subplot(212)
plt.plot(data)
plt.show()