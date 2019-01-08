from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy, ttk, pickle, math
from package.mazes import dfs_maze, random_maze, staticMazes
import frames
from package.agentcontroller.agentcontroller import AgentController
from package.simulation.simulation import Simulation
from operator import add


class GUI:
    maze = None
    data = None
    avg_steps = None
    agent_controller = None
    simulation = None
    configuration = None

    def __init__(self, top, configuration):
        self.configuration = configuration

        # init frames
        self.agent_settings = frames.AgentSettings(self, top, configuration)
        self.simulation_settings = frames.SimulationSettings(self, top, configuration)
        self.buttons = frames.Buttons(self, self.simulation_settings.frame)

        """ Progressbar """
        self.PB1 = ttk.Progressbar(top, orient="horizontal", mode="determinate")
        self.PB1.grid(row=6, column=0, sticky='EW')
        self.PB1["value"] = 0
        self.PB1["maximum"] = int(self.simulation_settings.E22.get())

        self.PB2 = ttk.Progressbar(top, orient="horizontal", mode="determinate")
        self.PB2.grid(row=5, column=0, sticky='EW')
        self.PB2["value"] = 0
        self.PB2["maximum"] = int(self.simulation_settings.E24.get())

        """ Console """
        self.console = Text(top, height=14, width=180)
        self.console.grid(row=7,column=0)
        self.console.config(state=DISABLED)

        # data file name
        frame_save_data = Frame(bd=2, relief=GROOVE)
        frame_save_data.grid(row=8, column=0)

        self.entry_file_name = Entry(frame_save_data, bd=2,width=5)
        self.entry_file_name.config(justify=CENTER, width=30)
        self.entry_file_name.insert(3,'data')
        self.entry_file_name.grid(row = 0, column = 0)

        self.button_save_data = Button(frame_save_data, text ="Save data", command=self.save_data)
        self.button_save_data.grid(row=0, column=1)

        self.entry_row = Entry(frame_save_data, bd=2,width=5)
        self.entry_row.config(justify=CENTER, width=10)
        self.entry_row.insert(3,'0')
        self.entry_row.grid(row = 0, column = 2)

        self.entry_col = Entry(frame_save_data, bd=2,width=5)
        self.entry_col.config(justify=CENTER, width=10)
        self.entry_col.insert(3,'0')
        self.entry_col.grid(row = 0, column = 3)

        self.entry_agent = Entry(frame_save_data, bd=2,width=5)
        self.entry_agent.config(justify=CENTER, width=10)
        self.entry_agent.insert(3,'1')
        self.entry_agent.grid(row = 0, column = 4)

        self.button_show_q_entry = Button(frame_save_data, text ="Show", command=self.show_q_entry)
        self.button_show_q_entry.grid(row=0, column=5)


        # init maze
        self.generate_new_maze()

    def show_maze(self):
        plt.figure(figsize=(10, 10))
        plt.imshow(self.maze[:, :, 0], cmap='Greys', interpolation='nearest')

        # show goals
        goal_positions = numpy.where(self.maze[:, :, 2] == 1)
        for goal in xrange(len(goal_positions[0])):
            plt.text(goal_positions[1][goal]-0.1, goal_positions[0][goal]+0.2, 'G', fontsize=15)

        # show starts
        start_positions = numpy.where(self.maze[:, :, 1] == 1)
        for start in xrange(len(start_positions[0])):
            plt.text(start_positions[1][start]-0.1, start_positions[0][start]+0.2, 'S', fontsize=15)
        plt.show()

    def show_q_entry(self):
        agent = self.agent_controller.agent_list[int(self.entry_agent.get())-1]
        rows = agent.maze_shape[0]

        output = ''
        for i in range(4):
            output += '[' + str(agent.qrl.Q_mat[int(self.entry_col.get())*rows + int(self.entry_row.get()), i]) + '] '

        self.write_console(output)

    def generate_new_maze(self):
        maze_name = self.simulation_settings.LB2.get(self.simulation_settings.LB2.curselection()[0])
        self.write_console("MazeGenerator: Generated new [" + maze_name + ']')
        if maze_name == 'Static maze 1':
            self.maze = staticMazes.get_static_maze_1()
        if maze_name == 'Static maze 2':
            self.maze = staticMazes.get_static_maze_2()
        if maze_name == 'Static maze 3':
            self.maze = staticMazes.get_static_maze_3()
        if maze_name == 'Static maze 4':
            self.maze = staticMazes.get_static_maze_4()
        if maze_name == 'Small Test Maze':
            self.maze = staticMazes.get_small_test_maze(int(self.simulation_settings.E12.get()), int(self.simulation_settings.E11.get()))
        if maze_name == 'URMG':
            self.maze = random_maze.maze(int(self.simulation_settings.E12.get()),
                                         int(self.simulation_settings.E11.get()),
                                         float(self.simulation_settings.E13.get()),
                                         float(self.simulation_settings.E14.get()))
        if maze_name == 'Depth-first search':
            self.maze = dfs_maze.generate_maze(int(self.simulation_settings.E11.get()),
                                               int(self.simulation_settings.E12.get()), True)
        if maze_name == 'DFS special':
            self.maze = dfs_maze.generate_maze_special(int(self.simulation_settings.E11.get()),
                                                       int(self.simulation_settings.E12.get()))

    def start_simulation(self):
        self.configuration = dict()

        self.agent_settings.get_configuration(self.configuration)
        self.simulation_settings.get_configuration(self.configuration)

        # save current configuration
        output = open('configuration.pkl', 'wb')
        pickle.dump(self.configuration, output)
        output.close()

        configuration = self.configuration

        # init progressbar
        self.PB1["value"] = 0
        self.PB1["maximum"] = configuration['iterations']

        """ generate start and goal positions (to do: own class for that?)"""
        start_positions, goal_positions = self.get_start_goal_positions(configuration['number_agents'])

        """ Agent controller """
        self.agent_controller = AgentController(self.maze, self.console)

        # if vAction.get() == 'Do one action each round':
        #    ac.cmd('set_doOnlyOneActionPerStep', True)

        """ Simulation """
        self.simulation = Simulation(self.agent_controller, self.maze)
        self.simulation.console = self.console
        self.simulation.do_plot = False
        self.PB1.update_idletasks()  # ? do I need this ?

        """ Run """
        self.data = None

        self.PB2["value"] = 0
        self.PB2["maximum"] = configuration['repetitions']
        for current_run in xrange(configuration['repetitions']):
            success, message = self.agent_controller.init_agents(configuration, start_positions, goal_positions)

            # check if agents are initiated
            if not success:
                return False
            self.write_console(message)

            # init data
            if self.data is None:
                self.data, self.avg_steps = self.simulation.run(configuration, self.PB1)
            else: # add result to data list
                sim_result, avg_steps = self.simulation.run(configuration, self.PB1)
                self.data[:] = map(add, self.data, sim_result)
                self.avg_steps[:] = map(add, self.avg_steps, avg_steps)

            # update progressbar
            self.PB2["value"] += 1
            self.PB2.update_idletasks()

        self.data[:] = [x / configuration['repetitions'] for x in self.data]

        """ Show results """
        if self.data:
            self.write_console('Simulation: Run finished! - Sum steps: %f - Avg steps: %f - Result: %f' % (math.fsum(self.data),
                                                                                                             (math.fsum(self.data)/len(self.data)),
                                                                                                             self.data[-1]))
        else:
            self.write_console('Simulation: Run stopped!')

    def restart_simulation(self):
        pass

    def plot_data(self):
        # plt.plot(self.avg_steps)
        plt.plot(self.data)

    def visualize(self):
        self.simulation.show_run(self.configuration)
        plt.clf()

    def showDecisionMaze(self):
        plt.imshow(self.maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
        row, col, dim = numpy.shape(self.maze)
        qM = numpy.zeros((row,col))
        for ii in xrange(row):
            for jj in xrange(col):
                ind = jj*row + ii
                actions_unsorted = list(self.agent_controller.shared_Q_mat[ind, :])
                actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1],reverse=True)]
                qM[ii,jj] = actions_sorted[0]
                if self.maze[ii,jj,0] == 1:
                    continue
                if actions_sorted[0] == 0:
                    plt.arrow(jj, ii+0.4, 0, -0.8, color='b', head_width=0.1, head_length=0.1)
                elif actions_sorted[0] == 1:
                    plt.arrow(jj-0.4, ii, 0.8, 0, color='b', head_width=0.1, head_length=0.1)
                elif actions_sorted[0] == 2:
                    plt.arrow(jj, ii-0.4, 0, 0.8, color='b', head_width=0.1, head_length=0.1)
                elif actions_sorted[0] == 3:
                    plt.arrow(jj+0.4, ii, -0.8, 0, color='b', head_width=0.1, head_length=0.1)
        plt.show()

    def get_start_goal_positions(self, number_agents):
        start_positions = []
        goal_positions = []

        possible_start_positions = numpy.where(self.maze[:, :, 1] == 1)
        possible_goals = numpy.where(self.maze[:, :, 2] == 1)

        for i in xrange(number_agents):
            start_pos = [1, 1, 2]
            number_start_pos = len(possible_start_positions[0])
            start_pos[0] = possible_start_positions[0][i % number_start_pos]
            start_pos[1] = possible_start_positions[1][i % number_start_pos]
            start_positions.append(start_pos)

            goal_pos = []
            number_goals = len(possible_goals[0])
            for goal in xrange(number_goals):
                goal_pos.append([possible_goals[0][goal], possible_goals[1][goal]])
            goal_positions.append(goal_pos)

        return start_positions, goal_positions

    def write_console(self, text):
        self.console.config(state=NORMAL)
        self.console.insert('1.0', text + '\n')
        self.console.config(state=DISABLED)

    def save_data(self):
        output_1 = open('data/' + self.entry_file_name.get() + '_steps.txt', 'wb')
        output_2 = open('data/' + self.entry_file_name.get() + '_info.txt', 'wb')
        output_3 = open('data/' + self.entry_file_name.get() + '_avg_steps.txt', 'wb')
        # print self.data
        output_data = [str(i) for i in self.data]
        output_1.write(' '.join(output_data))
        output_2.write(str(self.configuration))
        output_1.close()
        output_2.close()
        output_data = [str(i) for i in self.avg_steps]
        output_3.write(' '.join(output_data))
        output_3.close()

        # write data for each agent
        for agent in self.agent_controller.agent_list:
            file_name_3 = 'data/' + self.entry_file_name.get() + '_a' + str(agent.info['id']) + '_expertness.txt'
            output_3 = open(file_name_3, 'wb')
            output_data = [str(i) for i in agent.expertness_history]
            output_3.write(' '.join(output_data))
            output_3.close()

            file_name_4 = 'data/' + self.entry_file_name.get() + '_a' + str(agent.info['id']) + '_steps.txt'
            output_4 = open(file_name_4, 'wb')
            # print agent.steps_per_trial
            output_data = [str(i) for i in agent.steps_per_trial]
            output_4.write(' '.join(output_data))
            output_4.close()
