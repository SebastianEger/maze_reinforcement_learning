import agent
import agent_bin
import numpy


class AgentController:

    maze_shared = []
    num_agents = 0
    agents_list = []
    paths_list = []

    def __init__(self, maze, num_agents = 1):
        self.maze_shared = numpy.empty_like(maze)
        self.maze_shared[:] = maze
        self.num_agents = num_agents

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
                print 'All finished'
                break
        # get all paths
        for agents_it in self.agents_list:
            self.paths_list.append(agents_it.path)

    def create_agents_bin(self):
        for i in range(self.num_agents):
            self.agents_list.append(agent_bin.Agent(self.maze_shared,[1,1],i+1))
            #print 'Agent #' + str(i+1) + ' created!'

    def run_agents_bin(self):
        self.create_agents_bin()
        while True:
            # every agents does one step
            for agents_it in self.agents_list:
                if not agents_it.goal_reached:
                    agents_it.do_step()
            # check if every one has reached the goal
            if all(i.goal_reached for i in self.agents_list):
                print 'All finished'
                break
        # get all paths
        for agents_it in self.agents_list:
            self.paths_list.append(agents_it.path)