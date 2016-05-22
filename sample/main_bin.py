import sample.maze
import sample.agent_controller
import sample.maze_depth_first
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import itertools

#settings
num_rows = 30
num_cols = 20
num_agents = 7
iterations = 1
do_plot = True

path_len_counter = 0


for i in xrange(iterations):
    M = sample.maze_depth_first.generate_maze(num_rows, num_cols, True)
    #M = maze.maze(num_rows,num_cols,0.75,2)
    ac = sample.agent_controller.AgentController(M, num_agents, do_agent_avoidance=1)
    ac.run_agents_bin()
    print str(ac.num_steps)

if do_plot:
    #print ac.agents_list[0].maze[:,:,5]
    colors = itertools.cycle(["r", "b", "y", 'g'])
    #colors = np.random.rand(N)
    #plt.figure(figsize=(10, 5))
    #plt.imshow(ac.maze_shared[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    i=0
    plt.figure(figsize=(10, 10))
    for agent in ac.agents_list:
        plt.subplot(241+i)
        plt.imshow(agent.traveled_map, cmap=plt.cm.binary, interpolation='nearest')
        y,x = zip(*agent.path)
        #plt.scatter(x,y, color=next(colors), alpha=0.2,)
        i += 1
    plt.subplot(248)
    plt.imshow(M[:,:,0]+ac.maze_shared[:,:,2], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()
else:
    plt.figure(figsize=(10, 10))
    plt.imshow(M[:,:,0]+ac.maze_shared[:,:,2], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()
    pass