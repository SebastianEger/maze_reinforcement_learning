import numpy, Tkinter

from package.framework.agent import Agent

from package.agentmodules.movementmodules import forwardbackwardturn, forwardrightbackwardleft, northeastsouthwest
from package.agentmodules.qlearningmodules import expertnessmodules, weightingmodules
from package.agentmodules import explorationmodules

from package.framework.qlearning import QLearning


class AgentController:

    def __init__(self, maze, console):
        self.console = console
        self.maze = maze
        self.q_matrix_size = numpy.shape(maze)

        self.maze_shape = numpy.shape(maze)
        """ all """
        self.traveled_map = numpy.zeros(self.maze_shape, dtype=numpy.uint8)
        self.agent_list = []
        self.start_positions = None
        self.goal_positions = None

        self.shared_Q_mat = None

    def init_agents(self, configuration, start_positions, goal_positions):
        self.start_positions = start_positions
        self.goal_positions = goal_positions
        n_agents = len(start_positions)
        print configuration

        # reset variables
        self.agent_list = []
        self.shared_Q_mat = None

        for agent_id in xrange(n_agents):

            # base
            new_agent = Agent(agent_id, self.maze_shape, configuration)
            new_agent.current_position = start_positions[agent_id]
            new_agent.goal_position = goal_positions[agent_id]

            # movement modul
            if configuration['mov'] == 'North East South West':
                mov = northeastsouthwest.NorthEastSouthWest(self.maze_shape)
            elif configuration['mov'] == 'Forward Backward Turn':
                mov = forwardbackwardturn.ForwardBackwardTurn(self.maze_shape)
            elif configuration['mov'] == 'Forward Right Backward Left':
                mov = forwardrightbackwardleft.ForwardRightBackwardLeft(self.maze_shape)
            else:
                return False, "AgentController: Couldn't find this movement modul!"

            # expertness
            if configuration['expertness'] == 'Normal':
                expertness_modul = expertnessmodules.Normal()
            elif configuration['expertness'] == 'Absolute':
                expertness_modul = expertnessmodules.Absolute()
            elif configuration['expertness'] == 'Positive':
                expertness_modul = expertnessmodules.Positive()
            elif configuration['expertness'] == 'Distance To Goal':
                expertness_modul = expertnessmodules.DistToGoal()
            elif configuration['expertness'] == 'Needed Steps':
                expertness_modul = expertnessmodules.NeededSteps()
            elif configuration['expertness'] == 'All The Same':
                expertness_modul = expertnessmodules.AllTheSame()
            else:
                return False, "AgentController: Couldn't find this expertness modul!"

            # weighting
            if configuration['weighting'] == 'Learn From All':
                weighting_modul = weightingmodules.LearnFromAll()
            elif configuration['weighting'] == 'Learn From All Positive':
                weighting_modul = weightingmodules.LearnFromAllPositive()
            elif configuration['weighting'] == 'Learn From Experts':
                weighting_modul = weightingmodules.LearningFromExperts()
            else:
                return False, "AgentController: Couldn't find this weighting modul!"

            # Q reinforcement learning modul
            qrl = QLearning(configuration, expertness_modul, weighting_modul)

            # exploration modul
            if configuration['exp'] == 'Random':
                exp = explorationmodules.Random()
            elif configuration['exp'] == 'Smart Random':
                exp = explorationmodules.SmartRandom()
            else:
                return False, "AgentController: Couldn't find this exploration modul!"

            # init modules
            new_agent.init_modules(mov, qrl, exp)

            # set use shared Q option
            if configuration['use_shared_Q']:
                if self.shared_Q_mat is None:
                    # create shared Q matrix
                    self.shared_Q_mat = new_agent.qrl.zero_Q_mat()
                new_agent.qrl.Q_mat = self.shared_Q_mat

            # set agent speed
            if configuration['agent_speed'] == 'All Equal':
                new_agent.info['agent_speed'] = 1
            elif configuration['agent_speed'] == '2 different speeds':
                if float(agent_id)/float(n_agents) < 0.5:
                    new_agent.info['agent_speed'] = 1
                else:
                    new_agent.info['agent_speed'] = 2
            elif configuration['agent_speed'] == '3 different speeds':
                if float(agent_id)/float(n_agents) < 0.33:
                    new_agent.info['agent_speed'] = 1
                elif float(agent_id)/float(n_agents) < 0.66:
                    new_agent.info['agent_speed'] = 2
                elif float(agent_id)/float(n_agents):
                    new_agent.info['agent_speed'] = 3

            # add new agent to agent list
            self.agent_list.append(new_agent)

        # load configuration
        for agent in self.agent_list:
            agent.agent_list = self.agent_list
            agent.action_selection = configuration['action_selection']
            agent.exp.exploration_rate = configuration['exploration_rate']
            agent.exp.exploration_type = configuration['exploration_type']
            agent.tau = configuration['tau']

        return True, 'AgentController: All agents were successfully initiated! Configuration: ' \
               + str(configuration)

    def reset_agents(self):
        i = 0
        for agent in self.agent_list:
            agent.reset(self.start_positions[i], self.goal_positions[i])
            i += 1

    def do_coop_learning(self, show_expertness):
        expertness_list = []
        weight_mat = None
        for agent in self.agent_list:
            agent.qrl.create_Q_mat_new(self.agent_list)
        for agent in self.agent_list:
            if weight_mat is None:
                weight_mat = agent.qrl.weights
            else:
                weight_mat = numpy.row_stack((weight_mat, agent.qrl.weights))
            expertness_list.append(round(agent.qrl.expertness,3))
            agent.qrl.learn_Q_mat_new()

        # print weight_mat
        if show_expertness:
            self.write_console('AgentController: Expertness of each agent: ' + str(expertness_list))

    def write_console(self, text):
        self.console.config(state=Tkinter.NORMAL)
        self.console.insert('1.0', text + '\n')
        self.console.config(state=Tkinter.DISABLED)

    def cmd(self, cmd, value=None):
        def set_exploration_mode(mode):
            for _ in self.agent_list:
                _.exploration_mode = mode

        def set_exploration_rate(rate):
            for _ in self.agent_list:
                _.exploration_rate = rate

        def set_doOneActionPerStep(a):
            for _ in self.agent_list:
                _.doOnlyOneActionPerStep = a
                print _.doOnlyOneActionPerStep

        if cmd == "reset_robots":
            self.reset_robots()
        if cmd == "set_exploration_rate":
            set_exploration_rate(value)
        if cmd == "set_exploration_mode":
            set_exploration_mode(value)
        if cmd == "set_doOnlyOneActionPerStep":
            set_doOneActionPerStep(value)
