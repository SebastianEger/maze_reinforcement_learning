import maze
import agent_controller
import maze_depth_first
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import itertools

#settings
num_rows = 20
num_cols = 20
num_agents = 4
iterations = 1
do_plot = True

path_len_counter = 0
path = []
ac = 0

for i in xrange(iterations):
    M = maze_depth_first.generate_maze(num_rows,num_cols,True)
    ac = agent_controller.AgentController(M,num_agents)
    ac.run_agents_bin()
print(float(path_len_counter)/iterations)


if do_plot:


    print 'Anzahl an Pfaden:' + str(len(ac.paths_list))
    #print ac.agents_list[0].maze[:,:,5]
    colors = itertools.cycle(["r", "b", "g"])
    helper = 1
    plt.figure(figsize=(10, 5))
    plt.imshow(M[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    ac.paths_list.reverse()
    for path_it in ac.paths_list:
        y,x = zip(*path_it)
        plt.scatter(x,y, color=next(colors))
    plt.show()
else:
    #plt.imshow(ac.maze_shared[:,:,5], cmap = plt.cm.binary, interpolation='nearest')
    #plt.show()
    pass