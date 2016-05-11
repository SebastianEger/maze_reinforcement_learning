import numpy
import matplotlib.pyplot as plt
import maze
import maze_depth_first


def agent_function(maze_in, x=1, y=1):
    maze = numpy.empty_like(maze_in)
    maze[:] = maze_in
    mat_size = numpy.shape(maze)
    path = [[y-1,x]]
    path.append([y,x])

    while True:
        if y == mat_size[0]-2 and x == mat_size[1]-2:
            break

        if path[-2][0] - path[-1][0] < 0:
            if not maze[y,x-1]:
                x = x - 1
            elif not maze[y+1,x]:
                y = y + 1
            elif not maze[y,x+1]:
                x = x + 1
            elif not maze[y-1,x]:
                y = y - 1
        if path[-2][0] - path[-1][0] > 0:
            if not maze[y,x+1]:
                x = x + 1
            elif not maze[y-1,x]:
                y = y - 1
            elif not maze[y,x-1]:
                x = x - 1
            elif not maze[y+1,x]:
                y = y + 1
        if path[-2][1] - path[-1][1] < 0:
            if not maze[y+1,x]:
                y = y + 1
            elif not maze[y,x+1]:
                x = x + 1
            elif not maze[y-1,x]:
                y = y - 1
            elif not maze[y,x-1]:
                x = x - 1
        if path[-2][1] - path[-1][1] > 0:
            if not maze[y-1,x]:
                y = y - 1
            elif not maze[y,x-1]:
                x = x - 1
            elif not maze[y+1,x]:
                y = y + 1
            elif not maze[y,x+1]:
                x = x + 1

        next_position = [y,x]
        if path[-1] == next_position:
            print 'Error! No new state found!'
            break
        for item in path:
            if item == next_position:
                maze[path[-1][0],path[-1][1]] = 1
        path.append(next_position)
    path.pop(0)
    return path

if __name__ == '__main__':
    maze_mat = maze.maze(20,20)
    #maze_mat = maze_depth_first.generate_maze(20,20,True)
    path = agent_function(maze_mat,1,1)
    print len(path)

    plt.figure(figsize=(10, 5))
    plt.imshow(maze_mat, cmap=plt.cm.binary, interpolation='nearest')
    y,x = zip(*path)
    plt.scatter(x,y)
    plt.show()