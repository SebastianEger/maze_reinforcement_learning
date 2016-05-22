import agents.agent_bin as agent_bin
import matplotlib.pyplot as plt
import maze_depth_first
import agents.helper_functions as hf
import numpy


def do_plot():
    plt.subplot(121)
    plt.imshow(M[:,:,0]+M[:,:,1], cmap=plt.cm.binary, interpolation='nearest')
    plt.subplot(122)
    plt.imshow(M[:,:,3], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()

mazes = []
for _ in range(1):
    mazes.append(maze_depth_first.generate_maze(5,5,True))

ag = agent_bin.Agent(mazes[0],[1,1],1)
counter = 0

counter = 0
for _ in mazes:
    ag.set_new_maze(_)
    counter +=ag.do_run()
print float(counter)/20
print ag.Qmat
#input_text = input("Press Enter to continue...")
#plt.imshow(ag.Qmat2, cmap=plt.cm.binary, interpolation='nearest')
#plt.show()
ag.use_q_learning = True

counter = 0
for _ in mazes:
    ag.set_new_maze(_)
    counter +=ag.do_run()

print float(counter)/20



#plt.imshow(ag.Qmat, cmap=plt.cm.binary, interpolation='nearest')
#plt.show()

