from Tkinter import *
import ttk, math, numpy, pickle
import matplotlib.pyplot as plt
from mazes import dfs_maze, random_maze, staticMazes
from agentcontroller import agentController
from simulation import simulation
from operator import add

from src.GUI import agentsettings

top = Tk()
top.wm_title('Simulation panel')
plt.ion()

pkl_file = open('data.pkl', 'rb')
configuration = pickle.load(pkl_file)

maze = None
data = []
ac = None
sim = None

vMOV = StringVar(top)
vMOV.set(configuration.get('mov', 'North East South West'))

vEXP = StringVar(top)
vEXP.set(configuration.get('exp', 'Random'))

vExpertness = StringVar(top)
vExpertness.set(configuration.get('expertness', 'Normal'))

vWeighting = StringVar(top)
vWeighting.set(configuration.get('weighting', 'Learn From All'))

vExplorationType = StringVar(top)
vExplorationType.set(configuration.get('exploration_type', 'Constant'))

vActionSel = StringVar(top)
vActionSel.set(configuration.get('action_selection', 'Greedy'))

vAction = StringVar(top)


def writeConsole(text):
    T1.config(state=NORMAL)
    T1.insert('1.0', text + '\n')
    T1.config(state=DISABLED)

def startSim():
    configuration = dict()

    # moduls
    configuration['mov'] = vMOV.get()
    configuration['exp'] = vEXP.get()
    configuration['expertness'] = vExpertness.get()
    configuration['weighting'] = vWeighting.get()
    configuration['exploration_type'] = vExplorationType.get()
    configuration['action_selection'] = vActionSel.get()

    # settings
    configuration['number_agents'] = int(E21.get())
    configuration['use_shared_Q'] = useQshared.get()
    configuration['learn_rate'] = float(E31.get())
    configuration['discount'] = float(E32.get())
    configuration['reward_goal'] = float(E33.get())
    configuration['reward_wall'] = float(E34.get())
    configuration['reward_robot'] = float(E35.get())
    configuration['reward_step'] = float(E36.get())
    configuration['exploration_rate'] = float(E37.get())
    configuration['cooperation_time'] = float(E41.get())
    configuration['maze'] = LB2.get(LB2.curselection())
    configuration['iterations'] = E22.get()
    configuration['repetitions'] = int(E24.get())

    output = open('data.pkl', 'wb')

    # Pickle dictionary using protocol 0.
    pickle.dump(configuration, output)
    output.close()

    # init progressbar
    PB1["value"] = 0
    PB1["maximum"] = int(E22.get())

    """ generate start and goal positions (to do: own class for that?)"""
    start_positions, goal_positions = genStartGoalPositions()

    """ Agent controller """
    global ac
    ac = agentController.AgentController(maze, T1)

    if vAction.get() == 'Do one action each round':
        ac.cmd('set_doOnlyOneActionPerStep', True)

    """ Simulation """
    global sim
    sim = simulation.Simulation(ac, maze)
    sim.console = T1
    sim.cooperationTime = float(E41.get())
    sim.max_steps = float(E23.get())
    sim.do_plot = False
    PB1.update_idletasks()  # ? do I need this ?

    """ Run """
    global data
    data = None
    for current_run in xrange(configuration['repetitions']):
        success, message = ac.init_agents(configuration, start_positions, goal_positions)
        if not success:
            return False
        writeConsole(message)

        if data is None:
            data = sim.run(int(E22.get()), PB1)
        else:
            sim_result = sim.run(int(E22.get()), PB1)
            data[:] = map(add, data, sim_result)

    data[:] = [x / configuration['repetitions'] for x in data]

    """ Show results """
    if data:
        T1.config(state=NORMAL)
        T1.insert('1.0','Simulation: Run finished! - Sum steps: %f - Avg steps: %f - Result: %f\n' % (math.fsum(data), (math.fsum(data)/len(data)), data[-1]))
        T1.config(state=DISABLED)


def genStartGoalPositions():
    start_positions = []
    goal_positions = []

    possible_start_positions = numpy.where(maze[:, :, 1] == 1)
    possible_goals = numpy.where(maze[:, :, 2] == 1)

    number_agents = int(E21.get())

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

def restartSim():
    ac.q_settings(float(E31.get()),
                  float(E32.get()),
                  float(E33.get()),
                  float(E34.get()),
                  float(E35.get()),
                  float(E36.get()),
                  float(E37.get()))
    global data
    data = []
    PB1.update_idletasks()
    for i in xrange(int(E22.get())):
        ac.reset_agents()
        data.append(sim.run())
        PB1["value"] = i+1
        PB1.update_idletasks()
    plt.plot(data)
    plt.show()

def LB2onSelect(evt):
    generateMaze()
    return 0
    '''
    w = evt.widget
    index = int(w.curselection()[0])
    T1.config(state=NORMAL)
    if index == 0:
        T1.insert('1.0', 'Selected Static Maze 1\n')
    if index == 1:
        T1.insert('1.0', 'Selected Depth-first search maze | tree type, only one solution | Height and Width are doubled! \n')
    if index == 2:
        T1.insert('1.0', 'Selected Unknown Random Maze Generator | random maze with more than one solution \n')
    if index == 3:
        pass
    T1.config(state=DISABLED)
    '''

def generateMaze():
    global maze
    writeConsole("MazeGenerator: Generated new [" + LB2.get(LB2.curselection()[0]) + ']')
    maze_name = LB2.get(LB2.curselection()[0])
    if maze_name == 'Static maze 1':
        maze = staticMazes.get_static_maze_2()
    if maze_name == 'Static maze 3':
        maze = staticMazes.get_static_maze_3()
    if maze_name == 'Static maze 4':
        maze = staticMazes.get_static_maze_4()
    if maze_name == 'URMG':
        maze = random_maze.maze(int(E12.get()), int(E11.get()), float(E13.get()), float(E14.get()))
    if maze_name == 'Depth-first search':
        maze = dfs_maze.generate_maze(int(E11.get()), int(E12.get()), True)
    if maze_name == 'DFS special':
        maze = dfs_maze.generate_maze_special(int(E11.get()), int(E12.get()))


def showMaze():
    global maze
    plt.figure(figsize=(10, 10))
    plt.imshow(maze[:, :, 0], cmap='Greys', interpolation='nearest')

    # show goals
    goal_positions = numpy.where(maze[:, :, 2] == 1)
    for goal in xrange(len(goal_positions[0])):
        plt.text(goal_positions[1][goal]-0.1, goal_positions[0][goal]+0.2, 'G', fontsize=15)

    # show starts
    start_positions = numpy.where(maze[:, :, 1] == 1)
    for start in xrange(len(start_positions[0])):
        plt.text(start_positions[1][start]-0.1, start_positions[0][start]+0.2, 'S', fontsize=15)

    plt.show()

def plotData():
    global data
    plt.plot(data)

def visualize():
    sim.do_plot = True
    sim.run(1)
    plt.clf()

def showDecisionMaze():
    plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    row, col, dim = numpy.shape(maze)
    qM = numpy.zeros((row,col))
    for ii in xrange(row):
        for jj in xrange(col):
            ind = jj*row + ii
            actions_unsorted = list(ac.shared_Q_mat[ind, :])
            actions_sorted = [i[0] for i in sorted(enumerate(actions_unsorted), key=lambda x:x[1],reverse=True)]
            qM[ii,jj] = actions_sorted[0]
            if maze[ii,jj,0] == 1:
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


# Label
Label(top, text="Agent settings",font = "Helvetica 14 bold italic").grid(row=0, column = 0, sticky=W)

# Frame
frameAgentCreator = Frame(bd=2, relief=GROOVE)
frameAgentCreator.grid(row=1, column=0, sticky=EW)

# Objects
Label(frameAgentCreator, text="Movement model").grid(row=1, column = 0)
OM1 = OptionMenu(frameAgentCreator, vMOV, "North East South West", "Forward Backward Turn", "Forward Right Backward Left")
OM1.config(width=25)
OM1.grid(row=1,column = 1, sticky=EW)
# OM1.config(justify=LEFT)

Label(frameAgentCreator, text="Exploration model").grid(row=2, column = 0)
OM2 = OptionMenu(frameAgentCreator, vEXP, "Random", "Smart Random")
OM2.grid(row=2,column = 1, sticky=EW)
# OM2.config(justify=LEFT)

Label(frameAgentCreator, text="Expertness model").grid(row=1, column = 2)
OM3 = OptionMenu(frameAgentCreator, vExpertness, "Normal", "Absolute", "Positive", "Distance To Goal")
OM3.grid(row=1,column = 3, sticky=EW)
# OM3.config(justify=LEFT)

Label(frameAgentCreator, text="Weighting model").grid(row=2, column = 2)
OM4 = OptionMenu(frameAgentCreator, vWeighting, "Learn From All", "Learn From All Positive")
OM4.config(width=20)
OM4.grid(row=2, column = 3, sticky=EW)
# OM4.config(justify=LEFT)

Label(frameAgentCreator, text="Exploration type").grid(row=1, column = 4)
OM5 = OptionMenu(frameAgentCreator, vExplorationType, "Constant", "1/(trial+1)")
OM5.config(width=20)
OM5.grid(row=1, column = 5, sticky=EW)

Label(frameAgentCreator, text="Action selection").grid(row=2, column = 4)
vActionSel.set("Greedy") # default value
OM6 = OptionMenu(frameAgentCreator, vActionSel, "Greedy", "Probabilistic")
OM6.grid(row=2, column = 5, sticky=EW)


""" ------------------------------------------------------------------ """
""" ---------------------- Simulation settings ----------------------- """
""" ------------------------------------------------------------------ """
# Label
Label(top, text="Simulation settings",font = "Helvetica 14 bold italic").grid(row=2, column = 0, sticky=W)

# Frame
frameSettings = Frame(bd=2, relief=GROOVE)
frameSettings.grid(row=4, column=0)

# Objects
""" Maze selection """
Label(frameSettings, text="Maze",font = "Helvetica 14 bold italic", width=15).grid(row=0, column = 0)
LB2 = Listbox(frameSettings, exportselection=0)
LB2.grid(row=1,column = 0, rowspan = 5)
LB2.insert(END, "Static maze 1")
LB2.insert(END, "Static maze 3")
LB2.insert(END, "Static maze 4")
LB2.insert(END, "URMG")
LB2.insert(END, "Depth-first search")
LB2.insert(END, "DFS special")
# LB2.select_set(configuration.get('maze', 0))
LB2.select_set(0)
LB2.bind('<<ListboxSelect>>', LB2onSelect)

# Maze settings
Label(frameSettings, text="Random maze settings", font = "Helvetica 14 bold italic", width=20).grid(row=0, column = 1, columnspan=2)

startColumn = 1
startRow = 1
Label(frameSettings, text="Height").grid(row=startRow, column = startColumn)
E11 = Entry(frameSettings, bd =2,width = 5)
E11.config(justify=CENTER)
E11.insert(3,'10')
E11.grid(row = startRow, column = startColumn+1)

Label(frameSettings, text="Width").grid(row=startRow+1, column = startColumn)
E12 = Entry(frameSettings, bd =2,width = 5)
E12.config(justify=CENTER)
E12.insert(3,'10')
E12.grid(row = startRow+1, column = startColumn+1)

Label(frameSettings, text="Density").grid(row=startRow+2, column = startColumn)
E13 = Entry(frameSettings, bd =2,width = 5)
E13.config(justify=CENTER)
E13.insert(4,'0.75')
E13.grid(row = startRow+2, column = startColumn+1)

Label(frameSettings, text="Complexity").grid(row=startRow+3, column = startColumn)
E14 = Entry(frameSettings, bd =2,width = 5)
E14.config(justify=CENTER)
E14.insert(4,'0.75')
E14.grid(row = startRow+3, column = startColumn+1)

# Simulation settings
Label(frameSettings, text="Simulation settings", font = "Helvetica 14 bold italic", width = 20).grid(row=0, column = 3, columnspan=2)

startColumn = 3
startRow = 1

Label(frameSettings, text="Number agents").grid(row=startRow, column = startColumn)
E21 = Entry(frameSettings, bd =2,width = 5)
E21.config(justify=CENTER)
E21.insert(3, configuration.get('number_agents', 5))
E21.grid(row = startRow, column = startColumn+1)

Label(frameSettings, text="Iterations").grid(row=startRow+1, column = startColumn)
E22 = Entry(frameSettings, bd =2,width = 5)
E22.config(justify=CENTER)
E22.insert(4, configuration.get('iterations', 50))
E22.grid(row = startRow+1, column = startColumn+1)

Label(frameSettings, text="Max steps").grid(row=startRow+2, column = startColumn)
E23 = Entry(frameSettings, bd =2, width = 5)
E23.config(justify=CENTER)
E23.insert(3, configuration.get('max_steps', 5000))
E23.grid(row=startRow+2, column=startColumn+1)

Label(frameSettings, text="Repetitions").grid(row=startRow+3, column = startColumn)
E24 = Entry(frameSettings, bd =2, width = 5)
E24.config(justify=CENTER)
E24.insert(3, configuration.get('repetitions', 1))
E24.grid(row=startRow+3, column=startColumn+1)


# Q learning settings
Label(frameSettings, text="Q-learning settings", font = "Helvetica 14 bold italic", width = 50).grid(row=0, column = 5, columnspan=4)


startColumn = 5
startRow = 1

Label(frameSettings, text="Learn rate").grid(row=startRow, column = startColumn)
E31 = Entry(frameSettings, bd =2,width = 5)
E31.config(justify=CENTER)
E31.insert(3, configuration.get('learn_rate', 1))
E31.grid(row = startRow, column = startColumn+1)

Label(frameSettings, text="Discount").grid(row=startRow+1, column = startColumn)
E32 = Entry(frameSettings, bd =2,width = 5)
E32.config(justify=CENTER)
E32.insert(3, configuration.get('discount', 0.9))
E32.grid(row = startRow+1, column = startColumn+1)

Label(frameSettings, text="Reward goal").grid(row=startRow+2, column = startColumn)
E33 = Entry(frameSettings, bd =2,width = 5)
E33.config(justify=CENTER)
E33.insert(3, configuration.get('reward_goal', 100))
E33.grid(row = startRow+2, column = startColumn+1)

Label(frameSettings, text="Reward wall").grid(row=startRow+3, column = startColumn)
E34 = Entry(frameSettings, bd =2,width = 5)
E34.config(justify=CENTER)
E34.insert(3, configuration.get('reward_wall', -10))
E34.grid(row = startRow+3, column = startColumn+1)

Label(frameSettings, text="Reward robot").grid(row=startRow, column = startColumn+2)
E35 = Entry(frameSettings, bd =2,width = 5)
E35.config(justify=CENTER)
E35.insert(3, configuration.get('reward_robot', -0.01))
E35.grid(row = startRow, column = startColumn+3)

Label(frameSettings, text="Reward step").grid(row=startRow+1, column = startColumn+2)
E36 = Entry(frameSettings, bd =2,width = 5)
E36.config(justify=CENTER)
E36.insert(3, configuration.get('reward_step', -0.01))
E36.grid(row = startRow+1, column = startColumn+3)

Label(frameSettings, text="Exploration rate").grid(row=startRow+2, column = startColumn+2)
E37 = Entry(frameSettings, bd =2,width = 5)
E37.config(justify=CENTER)
E37.insert(3, configuration.get('exploration_rate', 0.1))
E37.grid(row = startRow+2, column = startColumn+3)

Label(frameSettings, text="Cooperation time").grid(row=startRow+3, column = startColumn+2)
E41 = Entry(frameSettings, bd =2,width = 5)
E41.config(justify=CENTER)
E41.insert(3, configuration.get('cooperation_time', -1))
E41.grid(row = startRow+3, column = startColumn+3)

# Additional options
Label(frameSettings, text="Additional Options", font = "Helvetica 14 bold italic", width=25).grid(row=0, column = 9, columnspan=2)

useQshared = IntVar()
useQshared.set(configuration.get('use_shared_Q', 0))
Label(frameSettings, text="Use shared Q matrix").grid(row=1, column = 9)
C31 = Checkbutton(frameSettings,variable=useQshared)
C31.grid(row = 1, column = 10)

# Buttons
startColumn = 0
startRow = 9

B4 = Button(frameSettings, text ="Show maze", command = showMaze)
B4.grid(row=startRow, column=startColumn)

B2 = Button(frameSettings, text ="Generate maze", command = generateMaze)
B2.grid(row=startRow, column=startColumn+1, columnspan=2)

B1 = Button(frameSettings, text ="Start simulation", command = startSim)
B1.grid(row=startRow, column=startColumn+3, columnspan=2)
B3 = Button(frameSettings, text ="Restart simulation", command = restartSim)
B3.grid(row=startRow+1, column=startColumn+3, columnspan=2)

B5 = Button(frameSettings, text ="Plot data", command = plotData)
B5.grid(row=startRow, column=startColumn+9, columnspan=2)

B6 = Button(frameSettings, text ="Visualize", command = visualize)
B6.grid(row=startRow+1, column=startColumn+9, columnspan=2)

B7 = Button(frameSettings, text ="Decision maze (only NESW model)", command = showDecisionMaze)
B7.grid(row=startRow+2, column=startColumn+9, columnspan=2)

""" ---------------------------------------------------------------- """

""" Progressbar """
PB1 = ttk.Progressbar(top, orient="horizontal", mode="determinate")
PB1.grid(row=5, column=0, sticky=EW)
PB1["value"] = 0
PB1["maximum"] = int(E22.get())

""" Console """
T1 = Text(top, height=14, width=180)
T1.grid(row=6,column=0)
T1.config(state=DISABLED)

# init maze
generateMaze()

top.mainloop()
