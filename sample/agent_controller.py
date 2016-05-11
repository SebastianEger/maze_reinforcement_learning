import agent
import agent_bin
import numpy


class AgentController:

    #maze_shared = []
    #num_agents = 0
    #agents_list = []
    #paths_list = []
    #num_step_sum = 0

    def __init__(self, maze, num_agents = 1, do_agent_avoidance = 1):
        self.maze_shared = numpy.empty_like(maze)
        self.maze_shared[:] = maze
        self.num_agents = num_agents
        self.agents_list = []
        self.paths_list = []
        self.num_step_sum = 0
        self.do_agent_avoidance = do_agent_avoidance

    def create_agents(self):
        for i in range(self.num_agents):
            self.agents_list.append(agent.Agent(self.maze_shared,[0,0],i+1))
            #print 'Agent #' + str(i+1) + ' created!'

    def run_agents(self):
        self.create_agents()
        while True:
            # every agents does one step
            for agents_it in self.agents_list:
                if not agents_it.goal_reached:
                    agents_it.do_step()
            # check if every one has reached the goal
            if all(i.goal_reached for i in self.agents_list):
                #print 'All finished'
                break
        # get all paths
        for agents_it in self.agents_list:
            self.paths_list.append(agents_it.path)

    def create_agents_bin(self):
        for i in range(self.num_agents):
            self.agents_list.append(agent_bin.Agent(self.maze_shared,[1,1],i+1,self.do_agent_avoidance))
            #print 'Agent #' + str(i+1) + ' created!'

    def run_agents_bin(self):
        self.create_agents_bin()
        while True:
            # every agents does one step
            for agents_it in self.agents_list:
                if not agents_it.goal_reached:
                    agents_it.do_step()
            # check if someone reached the goal
            for agents_it in self.agents_list:
                if agents_it.goal_reached:
                    # reverse path from winner
                    agents_it.path.reverse()
                    # finish run
                    for iter in self.agents_list:
                        iter.path_to_finish = agents_it.path
                        iter.finish_known = True
                        if not iter.goal_reached:
                            iter.do_step()
                    agents_it.path.reverse()
                    break
            # check if every one has reached the goal
            if all(i.goal_reached for i in self.agents_list):
                #print 'All finished'
                break
        # get all paths
        for agents_it in self.agents_list:
            self.paths_list.append(agents_it.path)
        self.num_step_sum = 0
        for path_it in self.paths_list:
            if self.num_step_sum < len(path_it):
                self.num_step_sum = len(path_it)