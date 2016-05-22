import numpy
import matplotlib.pyplot as plt
import helper_functions as hf


class Agent(object):

    def __init__(self, shared_maze, start_pos, number = 1, do_agent_avoidance = 1):
        self.maze = shared_maze
        self.maze_size = numpy.shape(shared_maze)
        self.traveled_map = numpy.zeros((self.maze_size[0],self.maze_size[1]),dtype=numpy.uint8)
        self.Qmat = numpy.zeros((4*self.maze_size[0]*self.maze_size[1],4),dtype=numpy.float)
        self.Qmat2 = numpy.zeros((4,4),dtype=numpy.float)
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.path = [[self.y-1,self.x],[self.y,self.x]] # 0 = y ; 1 = x
        self.path_to_finish = [] # path of the winner agent to finish
        self.path_to_reach_finish = [] # path to reach the finish
        self.agent_number = number
        self.goal_reached = False
        self.finish_known = False
        self.action = 0 # 0: go left, 1: go top, 2: go right, 3: go down
        self.do_agent_avoidance  = do_agent_avoidance
        self.do_Q_learning = True
        self.use_q_learning = False
        self.coming_from = 0

    def do_step(self): # returns true if agent reached the finish, false otherwise

        if self.do_agent_avoidance: # release our position
            self.maze[self.y,self.x,1] = 0

        self.do_fill_dead_ends()

        # calculate next position
        if self.finish_known:
            # check if we can skip part of the path
            tmp_path  = []
            tmp_path[:] = self.path_to_reach_finish
            if [self.y,self.x] in self.path_to_reach_finish:
                for it in tmp_path:
                    if it == [self.y,self.x]:
                        self.path_to_reach_finish.pop(0)
                        break
                    self.path_to_reach_finish.pop(0)
            # check if there is no agent
            if self.maze[self.path_to_reach_finish[0][0],self.path_to_reach_finish[0][1],1] == 0:
                self.y = self.path_to_reach_finish[0][0]
                self.x = self.path_to_reach_finish[0][1]
                #print str(self.y) + '-' + str(self.x)
                self.path_to_reach_finish.pop(0)

        else: # compute next step
            if self.use_q_learning:
                self.use_Qmat()
            else:
                self.get_next_pos()

        # marking position and visited space
        self.maze[self.y,self.x,4] = self.agent_number # mark position as visited
        self.traveled_map[self.y,self.x] += 1 # mark position as visited by me
        if self.do_agent_avoidance:
            self.maze[self.y,self.x,1] = self.agent_number

        if abs(self.y-self.path[-1][0]) > 1 or abs(self.x-self.path[-1][1]) > 1:
            raise Exception('Invalid step!')
        self.path.append([self.y,self.x])

        #plt.imshow(self.maze[:,:,1], cmap=plt.cm.binary, interpolation='nearest')
        #plt.show()

        # check if finish is reached
        if (self.y == self.maze_size[0]-2 and self.x == self.maze_size[1]-2):
            self.path.pop(0) # remove first path element
            # print 'Agent #' + str(self.agent_number) + ' has reached the goal! Path len: ' + str(len(self.path))
            if self.do_agent_avoidance:
                self.maze[self.y,self.x,1] = 0
            self.goal_reached = True
            return True
        else:
            return False

    def do_run(self): # for running without the agentcontroller
        step_counter = 0
        while True:
            step_counter += 1
            if self.do_step():
                return step_counter

    def do_fill_dead_ends(self):
        wall_counter = 0
        if self.maze[self.y,self.x+1,0] == 1 or self.maze[self.y,self.x+1,2] == 3:
            wall_counter += 1
        if self.maze[self.y,self.x-1,0] == 1 or self.maze[self.y,self.x-1,2] == 3:
            wall_counter += 1
        if self.maze[self.y+1,self.x,0] == 1 or self.maze[self.y+1,self.x,2] == 3:
            wall_counter += 1
        if self.maze[self.y-1,self.x,0] == 1 or self.maze[self.y-1,self.x,2] == 3:
            wall_counter += 1
        if wall_counter > 2 and [self.y, self.x] != [1,1]:
            self.maze[self.y,self.x,2] = wall_counter
            #print 'Warning! Agent #' + str(self.agent_number) + ' has a problem'

    def set_plan_to_reach_goal(self):
        crossing = []
        final_path_tmp = []
        self.path.reverse() # rotate path
        # get path we have to go back
        for pos1 in self.path:
            if pos1 in self.path_to_finish:
                crossing = pos1
                self.path_to_reach_finish.insert(0,pos1)
                break
            else:
                self.path_to_reach_finish.insert(0,pos1)
        self.path.reverse()
        self.path_to_reach_finish.reverse()
        # get path to reach the finish
        for pos2 in self.path_to_finish:
            if pos2 == crossing:
                break
            else:
                final_path_tmp.append(pos2)
        final_path_tmp.reverse()
        # add two paths together
        for iter in final_path_tmp:
            self.path_to_reach_finish.append(iter)
        self.finish_known = 1

    def check_position(self,y_pos,x_pos,level):
            for i in range(level):
                if self.maze[y_pos,x_pos,i] != 0:
                    return False
            # write qmatrix


            if self.do_Q_learning:
                if y_pos == self.maze_size[0]-2 and x_pos == self.maze_size[1]-2:
                    reward = -0.01
                else:
                    reward =  -1/float(level)
                    #reward = -0.01
                learn_rate = 0.01
                discount = 0.9
                estimate = max(self.Qmat[y_pos*self.maze_size[1]+x_pos,:])
                if y_pos-self.y == -1:
                    self.Qmat[self.y*self.maze_size[1]+self.x,1] += learn_rate*(reward+discount*estimate-self.Qmat[self.y*self.maze_size[1]+self.x,1])
            
                if y_pos-self.y == 1:
                    self.Qmat[self.y*self.maze_size[1]+self.x,3] += learn_rate*(reward+discount*estimate-self.Qmat[self.y*self.maze_size[1]+self.x,3])
                    
                if x_pos-self.x == -1:
                    self.Qmat[self.y*self.maze_size[1]+self.x,0] += learn_rate*(reward+discount*estimate-self.Qmat[self.y*self.maze_size[1]+self.x,0])
                    
                if x_pos-self.x == 1:
                    self.Qmat[self.y*self.maze_size[1]+self.x,2] += learn_rate*(reward+discount*estimate-self.Qmat[self.y*self.maze_size[1]+self.x,2])
                    
            return True

    def get_next_pos(self):
        # since maze is shared, he have to copy your traveled_map
        self.maze[:,:,3] = self.traveled_map
        # level 1: no agent and no wall
        # level 2: level_1 and no dead ends
        # level_3: level_2 and not visited by me
        # level_4: level_3 and not visited by any agent
        if self.path[-2][0] - self.path[-1][0] < 0 or self.path[-1] == self.path[-2]:
            self.coming_from = 1
            for level in range(5, 1, -1):
                if self.check_position(self.y,self.x-1,level):
                    self.x = self.x - 1
                    return True
                elif self.check_position(self.y+1,self.x,level):
                    self.y = self.y + 1
                    return True
                elif self.check_position(self.y,self.x+1,level):
                    self.x = self.x + 1
                    return True
                elif self.check_position(self.y-1,self.x,level):
                    self.y = self.y - 1
                    return True
        elif self.path[-2][0] - self.path[-1][0] > 0 or self.path[-1] == self.path[-2]:
            self.coming_from = 3
            for level in range(5, 1, -1):
                if self.check_position(self.y,self.x+1,level):
                    self.x = self.x + 1
                    return True
                elif self.check_position(self.y-1,self.x,level):
                    self.y = self.y - 1
                    return True
                elif self.check_position(self.y,self.x-1,level):
                    self.x = self.x - 1
                    return True
                elif self.check_position(self.y+1,self.x,level):
                    self.y = self.y + 1
                    return True
        elif self.path[-2][1] - self.path[-1][1] < 0 or self.path[-1] == self.path[-2]:
            self.coming_from = 0
            for level in range(5, 1, -1):
                if self.check_position(self.y+1,self.x,level):
                    self.y = self.y + 1
                    return True
                elif self.check_position(self.y,self.x+1,level):
                    self.x = self.x + 1
                    return True
                elif self.check_position(self.y-1,self.x,level):
                    self.y = self.y - 1
                    return True
                elif self.check_position(self.y,self.x-1,level):
                    self.x = self.x - 1
                    return True
        elif self.path[-2][1] - self.path[-1][1] > 0 or self.path[-1] == self.path[-2]:
            self.coming_from = 2
            for level in range(5, 1, -1):
                if self.check_position(self.y-1,self.x,level):
                    self.y = self.y - 1
                    return True
                elif self.check_position(self.y,self.x-1,level):
                    self.x = self.x - 1
                    return True
                elif self.check_position(self.y+1,self.x,level):
                    self.y = self.y + 1
                    return True
                elif self.check_position(self.y,self.x+1,level):
                    self.x = self.x + 1
                    return True

    def use_Qmat(self):
        actions = list(self.Qmat[self.y*self.maze_size[1]+self.x,:])
        #actions = list(self.Qmat2[self.coming_from,:])
        indices = [i[0] for i in sorted(enumerate(actions), key=lambda x:x[1])]
        indices.reverse()
        for _ in indices:
            # print indices

            self.coming_from = _
            #if actions[_] == 0:
            #    self.get_next_pos()
            #    return True
            if _ == 0:
                if self.maze[self.y,self.x-1,0] == self.maze[self.y,self.x-1,1] == 0:
                    self.x = self.x - 1
                    return True
            if _ == 1:
                if self.maze[self.y-1,self.x,0] == self.maze[self.y-1,self.x,1] == 0:
                    self.y = self.y - 1
                    return True
            if _ == 2:
                if self.maze[self.y,self.x+1,0] == self.maze[self.y,self.x+1,1] == 0:
                    self.x = self.x + 1
                    return True
            if _ == 3:
                if self.maze[self.y+1,self.x,0] == self.maze[self.y+1,self.x,1] == 0:
                    self.y = self.y + 1
                    return True

    def reset(self):
        self.path_to_reach_finish[self.path_to_reach_finish > 0] = 0
        self.traveled_map[self.traveled_map > 0] = 0
        pass

    def set_new_maze(self, new_maze):
        self.path_to_reach_finish = []
        self.path = []
        self.traveled_map = numpy.zeros((self.maze_size[0],self.maze_size[1]),dtype=numpy.uint8)
        self.maze = new_maze
        self.goal_reached = False
        self.finish_known = False
        self.x = 1
        self.y = 1
        self.path = [[self.y-1,self.x],[self.y,self.x]]

if __name__ == '__main__':
    pass