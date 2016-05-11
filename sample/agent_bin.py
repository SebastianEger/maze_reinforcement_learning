import numpy
import matplotlib.pyplot as plt


class Agent(object):

    #path = []
    #path_to_finish = []
    #finish_known = False
    #maze = []
    #dec = 0 # dead end counter
    #agent_number = 1
    #x = 1
    #y = 1
    #goal_reached = False
    
    def __init__(self, shared_maze, start_pos, number = 1, do_agent_avoidance = 1):
        self.maze = shared_maze
        self.maze_size = numpy.shape(shared_maze)
        self.traveled_map = numpy.zeros((self.maze_size[0],self.maze_size[1]),dtype=numpy.uint8)
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.path = [[self.y-1,self.x],[self.y,self.x]] # 0 = y ; 1 = x
        self.agent_number = number
        self.goal_reached = False
        self.finish_known = False
        self.path_to_finish = []
        self.dec = 0
        self.do_agent_avoidance  = do_agent_avoidance
        self.fill_dead_ends = 1
        self.dead_end_found = False
        self.doesnt_move = 0
        self.path_to_reach_finish = []

    # returns true if agent reached the finish, false otherwise
    def do_step(self):

        # release our position
        if self.do_agent_avoidance:
            self.maze[self.y,self.x,2] = 0 # release our last position

        self.do_fill_dead_ends()

        # calculate next position
        if self.finish_known:
            #print 'Agent #' + str(self.agent_number) + ' ' + str(len(self.path_to_reach_finish))
            # check if there is no agent
            if self.maze[self.path_to_reach_finish[0][0],self.path_to_reach_finish[0][1],2] == 0:
                self.y = self.path_to_reach_finish[0][0]
                self.x = self.path_to_reach_finish[0][1]
                #print str(self.y) + '-' + str(self.x)
                self.path_to_reach_finish.pop(0)
        else:
            if not self.get_next_position_nv():
                self.get_next_position_nvbm()
                if self.y == self.path[-1][0] and self.x == self.path[-1][1]:
                    self.get_next_position()

        # marking
        self.maze[self.y,self.x,1] = self.agent_number # mark position as visited
        self.traveled_map[self.y,self.x] += 1
        if self.do_agent_avoidance:
            self.maze[self.y,self.x,2] = self.agent_number # set our position

        if len(self.path) > 6:
            if self.path[-1] == self.path[-2] == self.path[-3] == self.path[-4] == self.path[-5]:
                print '!Agent #' + str(self.agent_number) + " doesnt move!"
                self.doesnt_move = 1
            elif self.doesnt_move:
                print '!Agent #' + str(self.agent_number) + " moves again!"
                self.doesnt_move = 0

        self.path.append([self.y,self.x])

        # check if finish is reached
        if (self.y == self.maze_size[0]-2 and self.x == self.maze_size[1]-2):
            self.path.pop(0)
            print 'Agent #' + str(self.agent_number) + ' has reached the goal! Path len: ' + str(len(self.path))
            if self.do_agent_avoidance:
                self.maze[self.y,self.x,2] = 0
            self.goal_reached = True
            return True
        else:
            return False

    def do_run(self):
        while True:
            if self.do_step():
                break

    def get_next_position(self):
        if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
                self.x = self.x - 1
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
                self.y = self.y + 1
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
                self.x = self.x + 1
            elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
                self.y = self.y - 1
        elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
                self.x = self.x + 1
            elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
                self.y = self.y - 1
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
                self.x = self.x - 1
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
                self.y = self.y + 1
        elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
                self.y = self.y + 1
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
                self.x = self.x + 1
            elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
                self.y = self.y - 1
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
                self.x = self.x - 1
        elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == 0:
                self.y = self.y - 1
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == 0:
                self.x = self.x - 1
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == 0:
                self.y = self.y + 1
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == 0:
                self.x = self.x + 1

    # not traveled by me
    def get_next_position_nvbm(self):
        if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.traveled_map[self.y,self.x-1] == 0:
                self.x = self.x - 1
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
                self.y = self.y + 1
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
                self.x = self.x + 1
            elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
                self.y = self.y - 1
        elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
                self.x = self.x + 1
            elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
                self.y = self.y - 1
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.traveled_map[self.y,self.x-1] == 0:
                self.x = self.x - 1
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
                self.y = self.y + 1
        elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
                self.y = self.y + 1
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
                self.x = self.x + 1
            elif self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
                self.y = self.y - 1
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.traveled_map[self.y,self.x-1] == 0:
                self.x = self.x - 1
        elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,2] == self.traveled_map[self.y-1,self.x] == 0:
                self.y = self.y - 1
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-2,2] == self.traveled_map[self.y,self.x-1] == 0:
                self.x = self.x - 1
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.traveled_map[self.y+1,self.x] == 0:
                self.y = self.y + 1
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.traveled_map[self.y,self.x+1] == 0:
                self.x = self.x + 1

    def get_next_position_nv(self):
        # coming from TOP
        if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x-1,0]  == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
                self.x = self.x - 1
                return True
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
                self.y = self.y + 1
                return True
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2]== self.maze[self.y,self.x+1,1] == 0:
                self.x = self.x + 1
                return True
            elif self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
                self.y = self.y - 1
                return True
        # coming from DOWN
        elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.maze[self.y,self.x+1,1] == 0:
                self.x = self.x + 1
                return True
            elif self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
                self.y = self.y - 1
                return True
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
                self.x = self.x - 1
                return True
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
                self.y = self.y + 1
                return True
        # coming from LEFT
        elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
                self.y = self.y + 1
                return True
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.maze[self.y,self.x+1,1] == 0:
                self.x = self.x + 1
                return True
            elif self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
                self.y = self.y - 1
                return True
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
                self.x = self.x - 1
                return True
        # coming from RIGHT
        elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
            if self.maze[self.y - 1,self.x,0] == self.maze[self.y - 1,self.x,2] == self.maze[self.y - 1,self.x,1] == 0:
                self.y = self.y - 1
                return True
            elif self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,2] == self.maze[self.y,self.x-1,1] == 0:
                self.x = self.x - 1
                return True
            elif self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,2] == self.maze[self.y+1,self.x,1] == 0:
                self.y = self.y + 1
                return True
            elif self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,2] == self.maze[self.y,self.x+1,1] == 0:
                self.x = self.x + 1
                return True
        return False
    def do_fill_dead_ends(self):
        wall_counter = 0
        if self.maze[self.y,self.x+1,0] == 1 or self.maze[self.y,self.x+1,3] == 3:
            wall_counter += 1
        if self.maze[self.y,self.x-1,0] == 1 or self.maze[self.y,self.x-1,3] == 3:
            wall_counter += 1
        if self.maze[self.y+1,self.x,0] == 1 or self.maze[self.y+1,self.x,3] == 3:
            wall_counter += 1
        if self.maze[self.y-1,self.x,0] == 1 or self.maze[self.y-1,self.x,3] == 3:
            wall_counter += 1
        if wall_counter > 2 and [self.y, self.x] != [1,1]:
            self.maze[self.y,self.x,3] = wall_counter
            #print 'Warning! Agent #' + str(self.agent_number) + ' has a problem'

    def set_plan_to_reach_goal(self):
        crossing = []
        final_path_tmp = []
        self.path.reverse() # rotate path
        # get path we have to go back
        for pos1 in self.path:
            if pos1 in self.path_to_finish:
                crossing = pos1
                #print crossing
                if self.maze[pos1[0],pos1[1],3] == 0:
                    self.path_to_reach_finish.insert(0,pos1)
                break
            else:
                if self.maze[pos1[0],pos1[1],3] == 0:
                    self.path_to_reach_finish.insert(0,pos1)
        self.path.reverse()
        self.path_to_reach_finish.reverse()
        # get path to reach the finish
        for pos2 in self.path_to_finish:
            if pos2 == crossing:
                break
            else:
                if self.maze[pos2[0],pos2[1],3] == 0:
                    final_path_tmp.append(pos2)
        final_path_tmp.reverse()
        for iter in final_path_tmp:
            self.path_to_reach_finish.append(iter)
        self.finish_known = 1
if __name__ == '__main__':
    pass