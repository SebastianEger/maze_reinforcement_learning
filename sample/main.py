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
num_agents = 3
iterations = 1
do_plot = True

path_len_counter = 0
path = []
ac = 0

for i in xrange(iterations):
    M = maze_depth_first.generate_maze(num_rows,num_cols)
    ac = agent_controller.AgentController(M,num_agents)
    ac.run_agents()
print(float(path_len_counter)/iterations)


if do_plot:

    image = np.zeros((num_rows*10,num_cols*10), dtype=np.uint8)
    # Generate the image for display

    for row in range(0,num_rows):
        for col in range(0,num_cols):
            cell_data = M[row,col]
            for i in range(10*row+1,10*row+9):
                image[i,range(10*col+1,10*col+9)] = 255
                if cell_data[0] == 1:image[range(10*row+1,10*row+9),10*col] = 255
                if cell_data[1] == 1:image[10*row,range(10*col+1,10*col+9)] = 255
                if cell_data[2] == 1:image[range(10*row+1,10*row+9),10*col+9] = 255
                if cell_data[3] == 1:image[10*row+9,range(10*col+1,10*col+9)] = 255

    # Display the image
    plt.imshow(image, cmap = cm.Greys_r, interpolation='nearest')

    print 'Anzahl an Pfaden:' + str(len(ac.paths_list))
    #print ac.agents_list[0].maze[:,:,5]
    colors = itertools.cycle(["r", "b", "g"])
    helper = 1
    for path_it in ac.paths_list:
        y,x = zip(*path_it)
        x = [i * 10 + 2.5*helper for i in x]
        y = [i * 10 + 2.5*helper for i in y]
        helper += 1
        plt.scatter(x,y, color=next(colors))
    plt.show()
else:
    #plt.imshow(ac.maze_shared[:,:,5], cmap = plt.cm.binary, interpolation='nearest')
    #plt.show()
    pass