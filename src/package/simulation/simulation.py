import Tkinter

import matplotlib.pyplot as plt


class Simulation:
    console = None

    def __init__(self, ac, maze):
        self.agent_controller = ac
        self.cooperationTime = -1
        self.do_plot = False
        self.refresh_rate = 0
        self.max_steps = 3000
        self.maze = maze

    def load_maze(self, maze):
        self.maze = maze
        self.maze[:, :, 1] = self.maze[:, :, 0]
        self.agent_controller.maze = self.maze
        self.agent_controller.reset_robots()

    def run(self, configuration, PB=None):
        steps = []
        avg_steps_per_agent = []
        coop_counter = 0
        doStop = False

        # do n_trials runs
        for current_trial in xrange(int(configuration['iterations'])):
            self.agent_controller.reset_agents()
            step_counter = 0

            # main while loop
            while True:
                all_finished = True

                # shuffle(self.robot_controller.robot_list)
                for agent in self.agent_controller.agent_list:

                    for it in xrange(agent.info['agent_speed']):

                        # simulate agent sensor
                        agent.sen.sim_sensors(agent.current_position, self.maze)

                        # set current position to old position
                        old_position = agent.current_position

                        # agent makes one step/action
                        goal_reached, new_position = agent.run()

                        # check if agent has reached the goal
                        if goal_reached:
                            # free goal position
                            self.maze[new_position[0], new_position[1], 0] = 0 # is this necessary?
                            break
                        else:
                            # traveled map
                            self.agent_controller.traveled_map[agent.current_position[0], agent.current_position[1], 0] += 1

                            # free old position
                            self.maze[old_position[0], old_position[1], 0] = 0

                            # block current position
                            self.maze[agent.current_position[0], agent.current_position[1], 0] = agent.info['id']+2

                            # at least one robot has not finished
                            all_finished = False

                    # after each simulation step add expertness of each agent to history
                    # agent.expertness_history.append(agent.qrl.expertness)

                if all_finished:
                    steps.append(step_counter)
                    avg_steps_per_agent.append(self.get_avg_steps_per_agent())
                    self.write_console('Simulation: Trial [' + str(current_trial+1) + '] finished! Steps: [' +
                                       str(step_counter) + '] Avg steps per agent: [' + str(avg_steps_per_agent[-1]) + ']')
                    break

                # inc step counter
                step_counter += 1

                if configuration['cooperation_type'] == 'Steps':
                    # coop learning in trial
                    coop_counter += 1

                    # check if we should we cooperative learning
                    if coop_counter == configuration['cooperation_time']:
                        # self.write_console('Simulation: Exchanging Q matrices!')
                        self.agent_controller.do_coop_learning(show_expertness=False)
                        coop_counter = 0


                # check if we exceeded number of steps
                if step_counter > configuration['max_steps']> 0:
                    self.write_console('Simulation: Reached step limit, stopping execution!')

                    for agent in self.agent_controller.agent_list:
                        self.maze[agent.current_position[0], agent.current_position[1], 0] = 0

                    doStop = True
                    steps = None
                    break

            if configuration['cooperation_type'] == 'Trials':
                coop_counter += 1
                # check if we should we cooperative learning
                if coop_counter == configuration['cooperation_time']:
                    self.write_console('Simulation: Exchanging Q matrices!')
                    self.agent_controller.do_coop_learning(show_expertness=True)
                    coop_counter = 0

            # update progressbar
            if PB:
                PB["value"] = current_trial+1
                PB.update_idletasks()

            # check if we should stop the run
            if doStop:
                break

        return steps, avg_steps_per_agent

    def init_plot(self):
        plt.ion()
        plt.figure(figsize=(10, 5))
        plt.imshow(self.maze[:, :, 0], cmap=plt.cm.binary, interpolation='nearest')
        for agent in self.agent_controller.agent_list:
            plt.plot(agent.current_position[0], agent.current_position[1], 'ro')
        plt.show()
        plt.pause(0.00001)

    def get_avg_steps_per_agent(self):
        avg_steps_per_agent = 0
        for agent in self.agent_controller.agent_list:
            avg_steps_per_agent += agent.step_counter

        avg_steps_per_agent /= float(len(self.agent_controller.agent_list))
        return avg_steps_per_agent

    def show_run(self, configuration):
        coop_counter = 0
        step_counter = 0
        self.init_plot()
        self.agent_controller.reset_agents()
        do_stop = False
        while True:
            all_finished = True

            # shuffle(self.robot_controller.robot_list)
            for agent in self.agent_controller.agent_list:

                for it in xrange(agent.info['agent_speed']):

                    # simulate agent sensor
                    agent.sen.sim_sensors(agent.current_position, self.maze)

                    # set current position to old position
                    old_position = agent.current_position

                    # agent makes one step/action
                    goal_reached, new_position = agent.run()

                    # check if agent has reached the goal
                    if goal_reached:
                        # free goal position
                        self.maze[new_position[0], new_position[1], 0] = 0 # is this necessary?
                        break
                    else:
                        # traveled map
                        self.agent_controller.traveled_map[agent.current_position[0], agent.current_position[1], 0] += 1

                        # free old position
                        self.maze[old_position[0], old_position[1], 0] = 0

                        # block current position
                        self.maze[agent.current_position[0], agent.current_position[1], 0] = agent.info['id']+2

                        # at least one robot has not finished
                        all_finished = False

                # after each simulation step add expertness of each agent to history
                # agent.expertness_history.append(agent.qrl.expertness)
            # inc step counter
            step_counter += 1

            self.show_current_maze()

            if all_finished:
                break

            # check if we exceeded number of steps
            if step_counter > self.max_steps > 0:
                self.write_console('Simulation: Reached step limit, stopping execution!')
                for agent in self.agent_controller.agent_list:
                    self.maze[agent.current_position[0], agent.current_position[1], 0] = 0
                do_stop = True
                break

            # check if we should stop the run
            if do_stop:
                break

    def show_current_maze(self):
        plt.clf()
        plt.imshow(self.maze[:, :, 0], cmap=plt.cm.binary, interpolation='nearest')
        for agent in self.agent_controller.agent_list:
            # plt.plot(robot.current_position[1], robot.current_position[0], 'ro')
            if agent.current_position[2] == 0:
                plt.arrow(agent.current_position[1],
                          agent.current_position[0]+0.4,
                          0, -0.8, color='b', head_width=0.1, head_length=0.1)
            if agent.current_position[2] == 1:
                plt.arrow(agent.current_position[1]-0.4,
                          agent.current_position[0],
                          +0.8, 0, color='b', head_width=0.1, head_length=0.1)
            if agent.current_position[2] == 2:
                plt.arrow(agent.current_position[1],
                          agent.current_position[0]-0.4,
                          0, +0.8, color='b', head_width=0.1, head_length=0.1)
            if agent.current_position[2] == 3:
                plt.arrow(agent.current_position[1]+0.4,
                          agent.current_position[0],
                          -0.8, 0, color='b', head_width=0.1, head_length=0.1)
        plt.show()
        plt.pause(0.00001)

    def write_console(self, text):
        self.console.config(state=Tkinter.NORMAL)
        self.console.insert('1.0', text + '\n')
        self.console.config(state=Tkinter.DISABLED)
