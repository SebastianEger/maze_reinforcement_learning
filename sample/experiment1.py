import agent_controller
import maze_depth_first
import matplotlib.pyplot as plt

#settings
num_rows = 12
num_cols = 12
#num_agents = 5
iterations = 50

data = []

for num_agents in xrange(1,20):
    tmp = 0
    for i in xrange(iterations):
        M = maze_depth_first.generate_maze(num_rows,num_cols,True)
        ac = agent_controller.AgentController(M,10)
        ac.run_agents_bin()
        tmp += float(ac.num_step_sum)
    print float(num_agents)/20
    data.append(tmp/iterations)

plt.plot(data)
plt.show()