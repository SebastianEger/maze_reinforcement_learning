import agent_controller
import maze_depth_first
import matplotlib.pyplot as plt

#settings
num_rows = 12
num_cols = 12
#num_agents = 5
iterations = 250

data = []

for i in xrange(iterations):
    counter = 0
    M = maze_depth_first.generate_maze(num_rows,num_cols, True)
    ac = agent_controller.AgentController(M, 3)
    ac.run_agents_bin()
    print float(i)/iterations
    data.append(float(ac.num_steps))

plt.plot(data)
plt.show()