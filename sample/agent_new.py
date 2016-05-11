import numpy

def agent_function(maze_in, x=1, y=1):
    maze = numpy.empty_like(maze_in)
    maze[:] = maze_in
    mat_size = numpy.shape(maze)
    path = [[y-1,x],[y,x]]

    while True:
        if y == mat_size[0]-1 and x == mat_size[1]-1:
            break

        if path[-2][0] - path[-1][0] < 0:
            if maze[y,x,0]:
                x = x - 1
            elif maze[y,x,3]:
                y = y + 1
            elif maze[y,x,2]:
                x = x + 1
            elif maze[y,x,1]:
                y = y - 1
        if path[-2][0] - path[-1][0] > 0:
            if maze[y,x,2]:
                x = x + 1
            elif maze[y,x,1]:
                y = y - 1
            elif maze[y,x,0]:
                x = x - 1
            elif maze[y,x,3]:
                y = y + 1
        if path[-2][1] - path[-1][1] < 0:
            if maze[y,x,3]:
                y = y + 1
            elif maze[y,x,2]:
                x = x + 1
            elif maze[y,x,1]:
                y = y - 1
            elif maze[y,x,0]:
                x = x - 1
        if path[-2][1] - path[-1][1] > 0:
            if maze[y,x,1]:
                y = y - 1
            elif maze[y,x,0]:
                x = x - 1
            elif maze[y,x,3]:
                y = y + 1
            elif maze[y,x,2]:
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