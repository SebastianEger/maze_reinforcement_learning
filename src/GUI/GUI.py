from Tkinter import *
import matplotlib.pyplot as plt

import agentsettings

class GUI:

    T1 = None
    maze = None
    data = []
    sim = None
    agent_controller = None

    def __init__(self):
        self.top = Tk()
        self.top.wm_title('Simulation panel')
        plt.ion()
        
        self.vMOV = StringVar(self.top)
        self.vEXP = StringVar(self.top)
        self.vQRL = StringVar(self.top)
        self.vExpertness = StringVar(self.top)
        self.vWeighting = StringVar(self.top)
        self.vExplorationRate = StringVar(self.top)
        self.vAction = StringVar(self.top)

        agentsettings.init_frame(self.top, self.vMOV, self.vEXP, self.vExpertness, self.vWeighting, self.vExplorationRate)

    def write_console(self, text):
        self.T1.config(state=NORMAL)
        self.T1.insert('1.0', text + '\n')
        self.T1.config(state=DISABLED)
        
    def LB2onSelect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.T1.config(state=NORMAL)
        if index == 0:
            self.write_console('GUI: Selected Static Maze 1\n')
        if index == 1:
            self.write_console('GUI: Selected Depth-first search maze | tree type, only one solution | Height and Width are doubled! \n')
        if index == 2:
            self.write_console('Selected Unknown Random Maze Generator | random maze with more than one solution \n')
            
        self.generate_new_maze()
        
    def generate_new_maze(self):
        writeConsole("GUI: Generated new " + LB2.get(LB2.curselection()[0]))
        if LB2.curselection() == (0,):
            self.maze = staticMazes.get_static_maze_2()
        if LB2.curselection() == (1,):
            self.maze = dfs_maze.generate_maze(int(E11.get()), int(E12.get()), True)
        if LB2.curselection() == (2,):
            self.maze = random_maze.maze(int(E12.get()), int(E11.get()), float(E13.get()), float(E14.get()))
        if LB2.curselection() == (3,):
            self.maze = staticMazes.get_static_maze_3()
        if LB2.curselection() == (4,):
            self.maze = dfs_maze.generate_maze_special(int(E11.get()), int(E12.get()))
        # showMaze()
        
    def show_maze(self):
        self.write_console("GUI: Show maze")
        plt.figure(figsize=(10, 10))
        plt.imshow(self.maze[:,:,0], cmap='Greys', interpolation='nearest')
        plt.show()
        
    def plot_data(self):
        plt.plot(self.data)
        
    def visualize(self):
        self.sim.do_plot = True
        self.sim.run(1)
        plt.clf()
