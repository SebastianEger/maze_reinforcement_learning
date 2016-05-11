import numpy


class Agent:

    path = []
    maze = []
    dec = 0 # dead end counter
    agent_number = 1
    x = 0
    y = 0
    goal_reached = False
    
    def __init__(self, shared_maze, start_pos, number = 1):
        self.maze = shared_maze
        self.maze_size = numpy.shape(shared_maze)
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.path = [[self.y-1,self.x],[self.y,self.x]]
        self.agent_number = number

    # returns true if agent reached the finish, false otherwise
    def do_step(self):

        self.maze[self.y,self.x,5] = 1 # release our position
        # check if we reached finish
        if self.y == self.maze_size[0]-1 and self.x == self.maze_size[1]-1:
            self.path.pop(0)
            print 'Agent #' + str(self.agent_number) + ' has reached the goal! Path len: ' + str(len(self.path))
            self.goal_reached = True
            return True

        if not self.get_next_position_nv():
            self.get_next_position()
        #print 'DebugAgent #' + str(self.agent_number)
        self.maze[self.y,self.x,4] = 0 # mark as visited
        #self.maze[self.y,self.x,5] = 0 # set our position

        # if we already visited the next position, set current position as Wall
        # This should only happen when we reach a dead end
        #if [self.y,self.x] == self.path[-2-self.dec*2]:
        #    self.maze[self.path[-1][0],self.path[-1][1],5] = 0
        #    self.dec += 1
        #else:
        #    self.dec = 0
        self.path.append([self.y,self.x])
        return False

    def do_run(self):
        while True:
            if self.do_step():
                break

    def get_next_position(self):
        if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
            elif self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
            elif self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
            elif self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
        # coming from DOWN
        elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
            elif self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
            elif self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
            elif self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
        # coming from LEFT
        elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
            elif self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
            elif self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
            elif self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
        # coming from RIGHT
        elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
            elif self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
            elif self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
            elif self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1

    def get_next_position_nv(self):
        # coming from TOP
        if self.path[-2][0] - self.path[-1][0]   or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,4] and self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
                    return True
            if self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,4] and self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
                    return True
            if self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,4] and self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
                    return True
            if self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,4] and self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
                    return True
        # coming from DOWN
        elif self.path[-2][0] - self.path[-1][0] > 0  or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,4] and self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
                    return True
            if self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,4] and self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
                    return True
            if self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,4] and self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
                    return True
            if self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,4] and self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
                    return True
        # coming from LEFT
        elif self.path[-2][1] - self.path[-1][1] < 0  or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,4] and self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
                    return True
            if self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,4] and self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
                    return True
            if self.maze[self.y,self.x,1]:
                if  self.maze[self.y-1,self.x,4] and self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
                    return True
            if self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,4] and self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
                    return True
        # coming from RIGHT
        elif self.path[-2][1] - self.path[-1][1] > 0  or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x,1]:
                if self.maze[self.y-1,self.x,4] and self.maze[self.y-1,self.x,5]:
                    self.y = self.y - 1
                    return True
            if self.maze[self.y,self.x,0]:
                if self.maze[self.y,self.x-1,4] and self.maze[self.y,self.x-1,5]:
                    self.x = self.x - 1
                    return True
            if self.maze[self.y,self.x,3]:
                if self.maze[self.y+1,self.x,4] and self.maze[self.y+1,self.x,5]:
                    self.y = self.y + 1
                    return True
            if self.maze[self.y,self.x,2]:
                if self.maze[self.y,self.x+1,4] and self.maze[self.y,self.x+1,5]:
                    self.x = self.x + 1
                    return True
        return False