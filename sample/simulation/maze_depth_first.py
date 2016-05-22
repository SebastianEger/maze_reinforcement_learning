import random
import numpy as np
from itertools import chain
import matplotlib.pyplot as plt


def generate_maze(num_rows = 10, num_cols=10, convert = False):
    M = np.zeros((num_rows,num_cols,6), dtype=np.uint8)
    # The array M is going to hold the array information for each cell.
    # The first four coordinates tell if walls exist on those sides
    # and the fifth indicates if the cell has been visited in the search.
    # M(LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED)
    # Set starting row and column

    r = 0
    c = 0
    history = [(r,c)] # The history is the

    # Trace a path though the cells of the maze and open walls along the path.
    # We do this with a while loop, repeating the loop until there is no history,
    # which would mean we backtracked to the initial start.
    while history:
        M[r,c,4] = 1 # designate this location as visited
        # check if the adjacent cells are valid for moving to
        check = []
        if c > 0 and M[r,c-1,4] == 0:
            check.append('L')
        if r > 0 and M[r-1,c,4] == 0:
            check.append('U')
        if c < num_cols-1 and M[r,c+1,4] == 0:
            check.append('R')
        if r < num_rows-1 and M[r+1,c,4] == 0:
            check.append('D')

        if len(check): # If there is a valid cell to move to.
            # Mark the walls between cells as open if we move
            history.append([r,c])
            move_direction = random.choice(check)
            if move_direction == 'L':
                M[r,c,0] = 1
                c = c-1
                M[r,c,2] = 1
            if move_direction == 'U':
                M[r,c,1] = 1
                r = r-1
                M[r,c,3] = 1
            if move_direction == 'R':
                M[r,c,2] = 1
                c = c+1
                M[r,c,0] = 1
            if move_direction == 'D':
                M[r,c,3] = 1
                r = r+1
                M[r,c,1] = 1
        else: # If there are no valid cells to move to.
        # retrace one step back in history if no move is possible
            r,c = history.pop()


    # Open the walls at the start and finish
    # M[0,0,0] = 1
    # M[num_rows-1,num_cols-1,2] = 1
    M[:,:,4] = 1
    M[:,:,5] = 1

    if convert:
        Mbin = np.zeros((num_rows*2+1,num_cols*2+1,6), dtype=np.uint8)
        # 0=binary maze, 1 visited yes/no, 2 blocked by agent?
        for i in xrange(num_rows*2+1):
            Mbin[i,:] = 1
        for i in xrange(num_cols*2+1):
            Mbin[:,i] = 1
        l = chain.from_iterable(zip(*M))
        helper_h = 0
        helper_v = 0
        for iter in list(l):
            Mbin[helper_v+1,helper_h+1,0] = 0
            Mbin[helper_v,helper_h+1,0] = not iter[1]
            Mbin[helper_v+1,helper_h,0] = not iter[0]
            #Mbin[helper_v+2,helper_h+1,0] = not iter[3]
            #Mbin[helper_v+1,helper_h+2,0] = not iter[2]
            helper_v += 2
            if helper_v == num_rows*2:
                helper_h += 2
                helper_v = 0
        Mbin[:,:,1] = 0
        Mbin[:,:,2] = 0
        Mbin[:,:,3] = 0
        return Mbin
    else:
        return M

def convertToBin(M):
    maze_size = np.shape(M)
    Mbin = np.zeros((maze_size[0]*2+1,maze_size[1]*2+1,3), dtype=np.uint8)
    # 0=binary maze, 1 visited yes/no, 2 blocked by agent?
    for i in xrange(maze_size[0]*2+1):
        Mbin[i,:] = 1
    for i in xrange(maze_size[1]*2+1):
        Mbin[:,i] = 1
    l = chain.from_iterable(zip(*M))
    helper_h = 0
    helper_v = 0
    for iter in list(l):
        Mbin[helper_v+1,helper_h+1,0] = 0
        Mbin[helper_v,helper_h+1,0] = not iter[1]
        Mbin[helper_v+1,helper_h,0] = not iter[0]
        #Mbin[helper_v+2,helper_h+1,0] = not iter[3]
        #Mbin[helper_v+1,helper_h+2,0] = not iter[2]
        helper_v += 2
        if helper_v == maze_size[0]*2:
            helper_h += 2
            helper_v = 0
    Mbin[:,:,1] = 0
    Mbin[:,:,2] = 0
    return Mbin


if __name__ == '__main__':

    M = generate_maze(20,20,True)

    plt.figure(figsize=(10, 5))
    plt.imshow(M[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()

