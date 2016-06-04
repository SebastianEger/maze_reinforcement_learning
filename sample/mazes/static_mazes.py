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

def get_static_maze_3():
    maze = np.zeros((15,15,5),dtype=np.uint8)
    maze[0,:,0] = 1
    maze[14,:,0] = 1
    maze[:,0,0] = 1
    maze[:,14,0] = 1

    maze[3,3:7,0] = 1
    maze[3,8:12,0] = 1
    maze[11,3:7,0] = 1
    maze[11,8:12,0] = 1

    maze[3:6,3,0] = 1
    maze[9:12,3,0] = 1
    maze[3:6,11,0] = 1
    maze[9:12,11,0] = 1

    maze[6:9,5,0] = 1
    maze[6:9,9,0] = 1

    maze[5,7,0] = 1
    maze[9,7,0] = 1
    return maze

if __name__ == '__main__':
    maze_1 = get_static_maze_1()
    plt.figure(figsize=(10, 10))
    plt.imshow(maze_1[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()