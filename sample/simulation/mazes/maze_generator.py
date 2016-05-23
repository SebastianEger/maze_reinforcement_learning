import numpy as np
import matplotlib.pyplot as plt

def get_static_maze_1():
    maze = np.zeros((10,10,5),dtype=np.uint8)
    maze[0,:,0] = 1
    maze[9,:,0] = 1
    maze[:,0,0] = 1
    maze[:,9,0] = 1
    maze[3:5,3:5,0] = 1
    maze[1:6,7,0] = 1
    maze[6,2:6,0] = 1
    return maze

def get_static_maze_2():
    maze = np.zeros((17,20,5),dtype=np.uint8)
    maze[0,:,0] = 1
    maze[16,:,0] = 1
    maze[:,0,0] = 1
    maze[:,19,0] = 1
    maze[2:5,14:17,0] = 1
    maze[4:8,4:9,0] = 1
    maze[4:8,4:9,0] = 1
    maze[9:13,4,0] = 1
    maze[12:13,7:9,0] = 1
    return maze

if __name__ == '__main__':
    maze_1 = get_static_maze_1()
    plt.figure(figsize=(10, 10))
    plt.imshow(maze_1[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()