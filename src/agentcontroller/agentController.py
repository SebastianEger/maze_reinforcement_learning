import numpy

from src.framework.agent import Agent

from src.agentmodules.movementmodules import forwardbackwardturn, forwardrightbackwardleft, northeastsouthwest
from src.agentmodules.qlearningmodules import expertnessmodules, weightingmodules
from src.agentmodules import explorationmodules

from src.framework.qlearning import QLearning


class AgentController:

    def __init__(self, maze):
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
            new_agent = Agent(agent_id, self.maze_shape)
            new_agent.current_position = start_positions[agent_id]
            new_agent.goal_position = goal_positions[agent_id]

            mov = None
            if configuration['mov'] == 'North East South West':
                mov = northeastsouthwest.NorthEastSouthWest(self.maze_shape)
            elif configuration['mov'] == 'Forward Backward Turn':
                mov = forwardbackwardturn.ForwardBackwardTurn(self.maze_shape)
            elif configuration['mov'] == 'Forward Right Backward Left':
                mov = forwardrightbackwardleft.ForwardRightBackwardLeft(self.maze_shape)
            else:
                return False, "AgentController: Couldn't find this movement modul!"

            if configuration['expertness modul'] == 'Normal':
                expertness_modul = expertnessmodules.Normal()
            elif configuration['expertness modul'] == 'Absolute':
                expertness_modul = expertnessmodules.Absolute()
            else:
                return False, "AgentController: Couldn't find this expertness modul!"

            if configuration['weighting modul'] == 'Learn From All':
                weighting_modul = weightingmodules.LearnFromAll()
            else:
                return False, "AgentController: Couldn't find this weighting modul!"

            qrl = QLearning(expertness_modul, weighting_modul)

            exp = None
            if configuration['exp'] == 'Random':
                exp = explorationmodules.Random()
            elif configuration['exp'] == 'Smart Random':
                exp = explorationmodules.SmartRandom()
            else:
                return False, "AgentController: Couldn't find this exploration modul!"

            new_agent.init_modules(mov, qrl, exp)

            if configuration['use shared Q']:
                if self.shared_Q_mat is None:
                    # create shared Q matrix
                    print 'AgentController: Generated shared Q matrix!'
                    self.shared_Q_mat = new_agent.qrl.zero_Q_mat()
                new_agent.qrl.Q_mat = self.shared_Q_mat

            self.agent_list.append(new_agent)

        # load configuration
        for agent in self.agent_list:
            agent.agent_list = self.agent_list
            agent.qrl.learn_rate = configuration['learn rate']
            agent.qrl.discount = configuration['discount']
            agent.qrl.reward_wall = configuration['reward wall']
            agent.qrl.reward_step = configuration['reward step']
            agent.qrl.reward_robot = configuration['reward robot']
            agent.qrl.reward_goal = configuration['reward goal']
            agent.exp.exploration_rate = configuration['exploration rate']

        return True, 'AgentController: All agents were successfully initiated! Configuration: ' \
               + configuration['mov'] \
               + ' - ' + configuration['exp']

    def reset_agents(self):
        i = 0
        for agent in self.agent_list:
            agent.reset(self.start_positions[i], self.goal_positions[i])
            i += 1

    def do_coop_learning(self):
        for agent in self.agent_list:
            agent.qrl.create_Q_mat_new(self.agent_list)
        for agent in self.agent_list:
            agent.qrl.learn_Q_mat_new()


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
