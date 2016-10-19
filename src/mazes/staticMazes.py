import numpy as np
import matplotlib.pyplot as plt
from src.framework.maze import Maze


class StaticMazeOne(Maze):
    def __init__(self):
       self.maze = self.get_maze()

    def get_maze(self):
        maze = np.zeros((10,10,5),dtype=np.uint8)
        maze[0,:,0] = 1
        maze[9,:,0] = 1
        maze[:,0,0] = 1
        maze[:,9,0] = 1
        maze[3:5,3:5,0] = 1
        maze[1:6,7,0] = 1
        maze[6,2:6,0] = 1
        return maze

    def get_goal_positions(self):
        return [8,8, 0]

    def get_start_positions(self):
        return [1,1, 2]

    def get_size(self):
        return [10, 10]


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


    maze[1, 1, 1] = 1
    maze[15, 18, 2] = 1
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

    maze[1,1,1] = 1
    maze[13,1,1] = 1
    maze[1,13,1] = 1
    maze[13,13,1] = 1

    maze[7, 7, 2] = 1

    return maze

def get_static_maze_4():
    maze = np.zeros((28,31,5),dtype=np.uint8)
    maze[0,:,0] = 1
    maze[-1,:,0] = 1
    maze[:,0,0] = 1
    maze[:,-1,0] = 1

    maze[1:11,7,0] = 1
    maze[15:23, 7, 0] = 1
    maze[8:15, 11, 0] = 1
    maze[4:11, 15, 0] = 1
    maze[8:25, 22, 0] = 1
    maze[19:27, 19, 0] = 1
    maze[19:27, 25, 0] = 1

    maze[4, 8:15, 0] = 1
    maze[15, 8:22, 0] = 1
    maze[23, 7:16, 0] = 1
    maze[19, 11:19, 0] = 1

    maze[1,1,1] = 1
    maze[26,29,2] = 1
    return maze

if __name__ == '__main__':
    maze_1 = get_static_maze_2()
    #plt.figure(figsize=(17, 20))
    #plt.imshow(maze_1[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    #plt.show()
    points = np.where(maze_1[:,:,1]==1)
    print points[0], points[1], len(points[0])

