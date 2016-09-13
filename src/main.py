from Tkinter import *
import ttk
import math
import matplotlib.pyplot as plt
import numpy
from mazes import dfs_maze, random_maze, staticMazes
from robots import robotController
from simulation import simulation

top = Tk()
top.wm_title('Simulation panel')
plt.ion()

maze = numpy.zeros((10,10,5))
data = []
rc = robotController.RobotController(maze)
sim = simulation.Simulation(rc, maze)

vMOV = StringVar(top)
vEXP = StringVar(top)
vQRL = StringVar(top)
vAction = StringVar(top)

def writeConsole(text):
    T1.config(state=NORMAL)
    T1.insert('1.0', text + '\n')
    T1.config(state=DISABLED)

def startSim():
    print 'Starting simulation!'
    PB1["value"] = 0
    PB1["maximum"] = int(E22.get())

    """ generate start and goal positions (to do: own class for that?)"""
    start_positions, goal_positions = genStartGoalPositions()

    """ Robot controller """
    global rc
    rc = robotController.RobotController(maze)
    success, message = rc.initAgents([vMOV.get(), vQRL.get(), vEXP.get(), useQshared.get()], start_positions, goal_positions)
    writeConsole(message)

    if not success:
        return False

    rc.q_settings(float(E31.get()), float(E32.get()), float(E33.get()), float(E34.get()),float(E35.get()),float(E36.get()),float(E37.get()))
    if vAction.get() == 'Do one action each round':
        rc.cmd('set_doOnlyOneActionPerStep', True)

    """ Simulation """
    global sim
    sim = simulation.Simulation(rc, maze)
    sim.cooperationTime = float(E41.get())
    sim.max_steps = float(E23.get())
    sim.do_plot = False
    PB1.update_idletasks()  # ? do I need this ?

    """ Run """
    global data
    data = sim.run(int(E22.get()), PB1)

    """ Show results """
    if data:
        T1.config(state=NORMAL)
        T1.insert('1.0','Simulation finished! - Sum steps: %f - Avg steps: %f \n' % (math.fsum(data), (math.fsum(data)/len(data))))
        T1.config(state=DISABLED)

def genStartGoalPositions():
    start_positions = []
    goal_positions = []
    maze_shape = numpy.shape(maze)
    numberRobots = int(E21.get())
    if LB2.curselection() == (3,):
        for i in xrange(numberRobots):
            if i % 4 == 0:
                start_positions.append([1,1,2])
            if i % 4 == 1:
                start_positions.append([1,13,2])
            if i % 4 == 2:
                start_positions.append([13,1,2])
            if i % 4 == 3:
                start_positions.append([13,13,2])
        for i in xrange(numberRobots):
            goal_positions.append([7,7,0])
    else:
        for i in xrange(numberRobots):
            start_positions.append([1,1,2])
        for i in xrange(numberRobots):
            goal_positions.append([maze_shape[0]-2,maze_shape[1]-2,0])
    return start_positions, goal_positions

def restartSim():
    rc.q_settings(float(E31.get()),
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
        rc.reset_robots()
        data.append(sim.run())
        PB1["value"] = i+1
        PB1.update_idletasks()
    plt.plot(data)
    plt.show()

def LB2onSelect(evt):
    global maze
    w = evt.widget
    index = int(w.curselection()[0])
    T1.config(state=NORMAL)
    if index == 0:
        T1.insert('1.0', 'Loaded Static Maze 1\n')
    if index == 1:
        T1.insert('1.0', 'Loaded Depth-first search maze | tree type, only one solution | Height and Width are doubled! \n')
    if index == 2:
        T1.insert('1.0', 'Loaded Unknown Random Maze Generator | random maze with more than one solution \n')
    if index == 3:
        pass
    generateMaze()
    T1.config(state=DISABLED)

def generateMaze():
    global maze
    if LB2.curselection() == (0,):
        maze = staticMazes.get_static_maze_2()
    if LB2.curselection() == (1,):
        maze = dfs_maze.generate_maze(int(E11.get()), int(E12.get()), True)
    if LB2.curselection() == (2,):
        maze = random_maze.maze(int(E12.get()), int(E11.get()), float(E13.get()), float(E14.get()))
    if LB2.curselection() == (3,):
        maze = staticMazes.get_static_maze_3()
    if LB2.curselection() == (4,):
        maze = dfs_maze.generate_maze_special(int(E11.get()), int(E12.get()))
    # showMaze()

def showMaze():
    global maze
    plt.figure(figsize=(10, 10))
    plt.imshow(maze[:,:,0], cmap='Greys', interpolation='nearest')
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
            actions_unsorted = list(rc.sharedQmatrix[ind,:])
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

Label(top, text="Agent settings",font = "Helvetica 14 bold italic").grid(row=0, column = 0, sticky=W)

frameAgentCreator = Frame(bd=2, relief=GROOVE)
frameAgentCreator.grid(row=1, column=0, sticky=EW)

""" Robot Builder """
Label(frameAgentCreator, text="Movement model").grid(row=1, column = 0)
vMOV.set("North East South West") # default value
OM1 = OptionMenu(frameAgentCreator, vMOV, "North East South West", "Forward Backward Turn", "Forward Right Backward Left")
OM1.grid(row=1,column = 1, sticky=EW)
OM1.config(justify=LEFT)

Label(frameAgentCreator, text="Exploration model").grid(row=2, column = 0)
vEXP.set("Random") # default value
OM2 = OptionMenu(frameAgentCreator, vEXP, "Random", "Smart Random", "Decreasing Exploration Rate")
OM2.grid(row=2,column = 1, sticky=EW)
OM2.config(justify=LEFT)

Label(frameAgentCreator, text="Reinforcement model").grid(row=1, column = 2)
vQRL.set("Basic Q learning") # default value
OM3 = OptionMenu(frameAgentCreator, vQRL, "Basic Q learning", "Weighted Q learning")
OM3.grid(row=1,column = 3, sticky=EW)
OM3.config(justify=LEFT)

Label(frameAgentCreator, text="Step counting rule").grid(row=2, column = 2)
vAction.set("Do one step each round") # default value
OM4 = OptionMenu(frameAgentCreator, vAction, "Do one step each round", "Do one action each round")
OM4.grid(row=2, column = 3, sticky=EW)
OM4.config(justify=LEFT)

variable1 = StringVar(top)
Label(frameAgentCreator, text="Exploration rate rule").grid(row=1, column = 4)
variable1.set("Constant") # default value
OM5 = OptionMenu(frameAgentCreator, variable1, "Constant", "Decreasing over steps")
OM5.grid(row=1, column = 5, sticky=EW)
OM5.config(justify=LEFT)


variable2 = StringVar(top)
Label(frameAgentCreator, text="Goal setting").grid(row=2, column = 4)
variable2.set("One Goal") # default value
OM6 = OptionMenu(frameAgentCreator, variable2, "One Goal", "Multiple Goals")
OM6.grid(row=2, column = 5, sticky=EW)


frameSettings = Frame(bd=2, relief=GROOVE)
frameSettings.grid(row=4, column=0)

""" Maze selection """
Label(frameSettings, text="Maze",font = "Helvetica 14 bold italic", width=25).grid(row=0, column = 0)
LB2 = Listbox(frameSettings, exportselection=0)
LB2.grid(row=1,column = 0, rowspan = 5)
LB2.insert(END, "Static maze 1")
LB2.insert(END, "Depth-first search maze")
LB2.insert(END, "URMG")
LB2.insert(END, "Static maze 3")
LB2.insert(END, "DFS special")
LB2.bind('<<ListboxSelect>>', LB2onSelect)

""" Maze settings """
Label(frameSettings, text="Random maze settings", font = "Helvetica 14 bold italic", width=25).grid(row=0, column = 1, columnspan=2)

startColumn = 1
startRow = 1
Label(frameSettings, text="Height").grid(row=startRow, column = startColumn)
E11 = Entry(frameSettings, bd =2,width = 3)
E11.config(justify=CENTER)
E11.insert(3,'10')
E11.grid(row = startRow, column = startColumn+1)

Label(frameSettings, text="Width").grid(row=startRow+1, column = startColumn)
E12 = Entry(frameSettings, bd =2,width = 3)
E12.config(justify=CENTER)
E12.insert(3,'10')
E12.grid(row = startRow+1, column = startColumn+1)

Label(frameSettings, text="Density").grid(row=startRow+2, column = startColumn)
E13 = Entry(frameSettings, bd =2,width = 3)
E13.config(justify=CENTER)
E13.insert(4,'0.75')
E13.grid(row = startRow+2, column = startColumn+1)

Label(frameSettings, text="Complexity").grid(row=startRow+3, column = startColumn)
E14 = Entry(frameSettings, bd =2,width = 3)
E14.config(justify=CENTER)
E14.insert(4,'0.75')
E14.grid(row = startRow+3, column = startColumn+1)

""" Simulation settings """
Label(frameSettings, text="Simulation settings", font = "Helvetica 14 bold italic", width = 25).grid(row=0, column = 3, columnspan=2)

startColumn = 3
startRow = 1

Label(frameSettings, text="Number robots").grid(row=startRow, column = startColumn)
E21 = Entry(frameSettings, bd =2,width = 3)
E21.config(justify=CENTER)
E21.insert(3,'10')
E21.grid(row = startRow, column = startColumn+1)

Label(frameSettings, text="Iterations").grid(row=startRow+1, column = startColumn)
E22 = Entry(frameSettings, bd =2,width = 3)
E22.config(justify=CENTER)
E22.insert(4,'50')
E22.grid(row = startRow+1, column = startColumn+1)

Label(frameSettings, text="Max steps").grid(row=startRow+2, column = startColumn)
E23 = Entry(frameSettings, bd =2, width = 3)
E23.config(justify=CENTER)
E23.insert(3, '-1')
E23.grid(row=startRow+2, column=startColumn+1)

""" Q learning settings """
Label(frameSettings, text="Q-learning settings", font = "Helvetica 14 bold italic", width = 50).grid(row=0, column = 5, columnspan=4)


startColumn = 5
startRow = 1

Label(frameSettings, text="Learn rate").grid(row=startRow, column = startColumn)
E31 = Entry(frameSettings, bd =2,width = 3)
E31.config(justify=CENTER)
E31.insert(3,'0.2')
E31.grid(row = startRow, column = startColumn+1)

Label(frameSettings, text="Discount").grid(row=startRow+1, column = startColumn)
E32 = Entry(frameSettings, bd =2,width = 3)
E32.config(justify=CENTER)
E32.insert(3,'0.9')
E32.grid(row = startRow+1, column = startColumn+1)

Label(frameSettings, text="Reward goal").grid(row=startRow+2, column = startColumn)
E33 = Entry(frameSettings, bd =2,width = 3)
E33.config(justify=CENTER)
E33.insert(3,'100')
E33.grid(row = startRow+2, column = startColumn+1)

Label(frameSettings, text="Reward wall").grid(row=startRow+3, column = startColumn)
E34 = Entry(frameSettings, bd =2,width = 3)
E34.config(justify=CENTER)
E34.insert(3,'-10')
E34.grid(row = startRow+3, column = startColumn+1)

Label(frameSettings, text="Reward robot").grid(row=startRow, column = startColumn+2)
E35 = Entry(frameSettings, bd =2,width = 4)
E35.config(justify=CENTER)
E35.insert(3,'-0.01')
E35.grid(row = startRow, column = startColumn+3)

Label(frameSettings, text="Reward step").grid(row=startRow+1, column = startColumn+2)
E36 = Entry(frameSettings, bd =2,width = 4)
E36.config(justify=CENTER)
E36.insert(3,'-0.01')
E36.grid(row = startRow+1, column = startColumn+3)

Label(frameSettings, text="Exploration rate").grid(row=startRow+2, column = startColumn+2)
E37 = Entry(frameSettings, bd =2,width = 4)
E37.config(justify=CENTER)
E37.insert(3,'0')
E37.grid(row = startRow+2, column = startColumn+3)

Label(frameSettings, text="Cooperation time").grid(row=startRow+3, column = startColumn+2)
E41 = Entry(frameSettings, bd =2,width = 4)
E41.config(justify=CENTER)
E41.insert(3,'-1')
E41.grid(row = startRow+3, column = startColumn+3)

""" Additional options """
Label(frameSettings, text="Additional Options", font = "Helvetica 14 bold italic", width=25).grid(row=0, column = 9, columnspan=2)

useQshared = IntVar()
Label(frameSettings, text="Use shared Q matrix").grid(row=1, column = 9)
C31 = Checkbutton(frameSettings,variable=useQshared)
C31.grid(row = 1, column = 10)

""" Buttons """
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



""" Progressbar """
PB1 = ttk.Progressbar(top, orient="horizontal", mode="determinate")
PB1.grid(row=5, column=0, sticky=EW)
PB1["value"] = 0
PB1["maximum"] = int(E22.get())

""" Console """
T1 = Text(top, height=14, width=180)
T1.grid(row=6,column=0)
T1.config(state=DISABLED)


top.mainloop()
