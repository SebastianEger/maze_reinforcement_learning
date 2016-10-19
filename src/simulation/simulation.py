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

    def run(self, n_trials=1, PB=None):
        data = []
        coop_counter = 0
        doStop = False

        # check if we should plot the run
        if self.do_plot:
            self.init_plot()

        # do n_trials runs
        for current_trial in xrange(n_trials):
            self.agent_controller.reset_agents()
            step_counter = 0

            # main while loop
            while True:
                all_finished = True

                # shuffle(self.robot_controller.robot_list)
                for agent in self.agent_controller.agent_list:

                    # simulate agent sensor
                    agent.sen.sim_sensors(agent.current_position, self.maze)

                    # set current position to old position
                    old_position = agent.current_position

                    # let agent make one step/action
                    goalReached, newPosition = agent.run()

                    # check if agent has reached the goal
                    if goalReached:
                        # free goal position
                        self.maze[newPosition[0], newPosition[1], 0] = 0
                    else:
                        # traveled map
                        self.agent_controller.traveled_map[agent.current_position[0], agent.current_position[1], 0] += 1
                        # free old position
                        self.maze[old_position[0], old_position[1], 0] = 0
                        # block current position
                        self.maze[agent.current_position[0], agent.current_position[1], 0] = agent.agent_id+2
                        # at least one robot has not finished
                        all_finished = False

                if self.do_plot:
                    self.show_current_maze()

                # inc step counter
                step_counter += 1

                # check if every agent has finished
                if all_finished:
                    data.append(step_counter)
                    self.write_console('Simulation: Trial [' + str(current_trial+1) + '] finished!')
                    break

                # check if we exceeded number of steps
                if step_counter > self.max_steps > 0:
                    self.write_console('Simulation: Reached step limit, stopping execution!')
                    for agent in self.agent_controller.agent_list:
                        self.maze[agent.current_position[0], agent.current_position[1], 0] = 0
                    doStop = True
                    break

            coop_counter += 1

            # check if we should we cooperative learning
            if coop_counter == self.cooperationTime:
                self.write_console('Simulation: Exchanging Q matrices!')
                self.agent_controller.do_coop_learning()
                coop_counter = 0

            # update progressbar
            if PB:
                PB["value"] = current_trial+1
                PB.update_idletasks()

            # check if we should stop the run
            if doStop:
                break

        # for agent in self.agent_controller.agent_list:
        #    print agent.qrl.Q_mat[23,:]

        return data

    def init_plot(self):
        plt.ion()
        plt.figure(figsize=(10, 5))
        plt.imshow(self.maze[:, :, 0], cmap=plt.cm.binary, interpolation='nearest')
        for agent in self.agent_controller.agent_list:
            plt.plot(agent.current_position[0], agent.current_position[1], 'ro')
        plt.show()
        plt.pause(0.00001)

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
