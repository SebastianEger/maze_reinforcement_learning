import Tkinter
import ttk
from threading import Thread
import matplotlib.pyplot as plt
import math
import robotController
import simulation
import numpy
from mazes import dfs_maze
from mazes import random_maze
from mazes import staticMazes

top = Tkinter.Tk()
top.wm_title('Simulation panel')
plt.ion()

maze = numpy.zeros((10,10,5))
data = []
rc = robotController.RobotController(maze)
sim = simulation.Simulation(rc,maze)

def startSimThread():
    thread = Thread(target=startSim, args=[])
    thread.start()

def startSim():
    print 'Starting simulation!'
    start_positions = []
    goal_positions = []
    numberRobots = int(E21.get())
    PB1["value"] = 0
    PB1["maximum"] = int(E22.get())

    """ set start and goal positions """
    start_positions, goal_positions = genStartGoalPositions()

    """ Robot controller """
    global rc
    robot_name = LB1.get(LB1.curselection()[0],LB1.curselection()[0])
    rc = robotController.RobotController(maze)
    rc.init_robots(robot_name[0],start_positions,goal_positions)
    rc.q_settings(float(E31.get()),float(E32.get()),float(E33.get()),float(E34.get()),float(E35.get()),float(E36.get()),float(E37.get()),float(E41.get()))

    """ Simulation """
    global sim
    sim = simulation.Simulation(rc, maze)
    sim.do_plot = False
    # sim.do_plot = do_plot.get()
    PB1.update_idletasks()

    global data
    data = []
    for i in xrange(int(E22.get())):
        rc.reset_robots(start_positions,goal_positions)
        data.append(sim.run_simulation())
        PB1["value"] = i+1
        PB1.update_idletasks()

    sim.do_plot = do_plot.get()
    rc.reset_robots(start_positions,goal_positions)
    sim.run_simulation()
    if data:
        T1.config(state=Tkinter.NORMAL)
        T1.insert('1.0','Simulation finished | avg steps: %f | \n' % (math.fsum(data)/len(data)))
        T1.config(state=Tkinter.DISABLED)
    # for i in xrange(int(E6.get())):
    #     if LB2.curselection() == (2,):
    #         maze = random_maze.maze(int(E1.get()), int(E2.get()), float(E3.get()), float(E4.get()))
    #     rc = robot_controller.RobotController(int(E5.get()),maze,robot_name[0])
    #     sim = simulation.Simulation(rc,maze)
    #     sim.do_plot = do_plot.get()
    #     data.append(sim.run_simulation())
    #     # PB1["value"] = i+1
    # plt.figure()
    if sim.do_plot:
        plt.clf()

    '''
    plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    row, col, dim = numpy.shape(maze)
    qM = numpy.zeros((row,col))
    for ii in xrange(row):
        for jj in xrange(col):
            ind = jj*row + ii
            actions_unsorted = list(rc.butler_sq[ind,:])
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
    '''
    # plt.plot(data)
    # nPB1["value"] = 0


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
    start_positions, goal_positions = genStartGoalPositions()
    rc.q_settings(float(E31.get()),float(E32.get()),float(E33.get()),float(E34.get()),float(E35.get()),float(E36.get()),float(E37.get()),float(E41.get()))
    data = []
    PB1.update_idletasks()
    for i in xrange(int(E22.get())):
        rc.reset_robots(start_positions,goal_positions)
        data.append(sim.run_simulation())
        PB1["value"] = i+1
        PB1.update_idletasks()
    plt.plot(data)
    plt.show()


def LB1onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    T1.config(state=Tkinter.NORMAL)
    if index == 0:
        T1.insert('1.0', 'Loaded Artemis | States: position        | Actions: North, East, South, West        | Individual Q-learning  |\n')
    if index == 1:
        T1.insert('1.0', 'Loaded Butler  | States: position        | Actions: North, East, South, West        | Cooperative Q-learning | Shared Q matrix      |\n')
    if index == 3:
        T1.insert('1.0', 'Loaded Koboi   | States: position        | Actions: North, East, South, West        | Cooperative Q-learning | Learning from all    | '
                         'Normal \n')
    if index == 4:
        T1.insert('1.0', 'Loaded Holly   | States: position        | Actions: North, East, South, West        | Cooperative Q-learning | Learning from Expert | '
                         'Distance to goal\n')
    if index == 5:
        T1.insert('1.0', 'Loaded Diggums | States: pos,orientation | Actions: Forward, Right, Backwards, Left | Cooperative Q-learning | Shared Q matrix      |\n')
    T1.config(state=Tkinter.DISABLED)


def LB2onSelect(evt):
    global maze
    w = evt.widget
    index = int(w.curselection()[0])
    T1.config(state=Tkinter.NORMAL)
    if index == 0:
        T1.insert('1.0', 'Loaded Static Maze 1\n')
    if index == 1:
        T1.insert('1.0', 'Loaded Depth-first search maze | tree type, only one solution | Height and Width are doubled! \n')
    if index == 2:
        T1.insert('1.0', 'Loaded Unknown Random Maze Generator | random maze with more than one solution \n')
    if index == 3:
        pass
    generateMaze()
    T1.config(state=Tkinter.DISABLED)

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
    showMaze()

def showMaze():
    global maze
    plt.figure(figsize=(10, 10))
    plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    plt.show()

def plotData():
    global data
    plt.plot(data)


Tkinter.Label(top, text="Robot",font = "Helvetica 14 bold italic").grid(row=0, column = 0)
Tkinter.Label(top, text="Maze",font = "Helvetica 14 bold italic").grid(row=0, column = 1)
Tkinter.Label(top, text="Random maze settings",font = "Helvetica 14 bold italic").grid(row=0, column = 2, columnspan=2)
Tkinter.Label(top, text="Simulation settings",font = "Helvetica 14 bold italic").grid(row=0, column = 4, columnspan=2)
Tkinter.Label(top, text="Q-learning settings",font = "Helvetica 14 bold italic").grid(row=0, column = 6, columnspan=2)
Tkinter.Label(top, text="Cooperative learning settings",font = "Helvetica 14 bold italic").grid(row=0, column = 10, columnspan=2)

LB1 = Tkinter.Listbox(top, height=7, width=15, exportselection=0)
LB1.grid(row=1,column = 0, rowspan=5)
LB1.insert(Tkinter.END, "Artemis")
LB1.insert(Tkinter.END, "Butler")
LB1.insert(Tkinter.END, "Foaly")
LB1.insert(Tkinter.END, "Koboi")
LB1.insert(Tkinter.END, "Holly")
LB1.insert(Tkinter.END, "Diggums")
LB1.bind('<<ListboxSelect>>', LB1onSelect)

T1 = Tkinter.Text(top, height=14, width=180)
T1.grid(row=6,column=0, columnspan=13)
#T1.tag_config('n',justify=Tkinter.LEFT)
#T1.insert(Tkinter.END, "No coop Q learning")
T1.config(state=Tkinter.DISABLED)

LB2 = Tkinter.Listbox(top, height=7, exportselection=0)
LB2.grid(row=1,column = 1, rowspan=5)
LB2.insert(Tkinter.END, "Static maze 1")
LB2.insert(Tkinter.END, "Depth-first search maze")
LB2.insert(Tkinter.END, "URMG")
LB2.insert(Tkinter.END, "Static maze 3")
LB2.insert(Tkinter.END, "DFS special")
LB2.bind('<<ListboxSelect>>', LB2onSelect)

Tkinter.Label(top, text="Height").grid(row=1, column = 2)
E11 = Tkinter.Entry(top, bd =2,width = 3)
E11.config(justify=Tkinter.CENTER)
E11.insert(3,'10')
E11.grid(row = 1, column = 3)

Tkinter.Label(top, text="Width").grid(row=2, column = 2)
E12 = Tkinter.Entry(top, bd =2,width = 3)
E12.config(justify=Tkinter.CENTER)
E12.insert(3,'10')
E12.grid(row = 2, column = 3)

Tkinter.Label(top, text="Density").grid(row=3, column = 2)
E13 = Tkinter.Entry(top, bd =2,width = 3)
E13.config(justify=Tkinter.CENTER)
E13.insert(4,'0.75')
E13.grid(row = 3, column = 3)

Tkinter.Label(top, text="Complexity").grid(row=4, column = 2)
E14 = Tkinter.Entry(top, bd =2,width = 3)
E14.config(justify=Tkinter.CENTER)
E14.insert(4,'0.75')
E14.grid(row = 4, column = 3)

""" Simulation settings """

Tkinter.Label(top, text="Number robots").grid(row=1, column = 4)
E21 = Tkinter.Entry(top, bd =2,width = 3)
E21.config(justify=Tkinter.CENTER)
E21.insert(3,'10')
E21.grid(row = 1, column = 5)

do_plot = Tkinter.IntVar()
Tkinter.Label(top, text="Visualization").grid(row=2, column = 4)
C21 = Tkinter.Checkbutton(top,variable=do_plot)
C21.grid(row = 2, column = 5)

Tkinter.Label(top, text="Iterations").grid(row=3, column = 4)
E22 = Tkinter.Entry(top, bd =2,width = 3)
E22.config(justify=Tkinter.CENTER)
E22.insert(4,'50')
E22.grid(row = 3, column = 5)

""" Q learning settings """

Tkinter.Label(top, text="Learn rate").grid(row=1, column = 6)
E31 = Tkinter.Entry(top, bd =2,width = 3)
E31.config(justify=Tkinter.CENTER)
E31.insert(3,'0.2')
E31.grid(row = 1, column = 7)

Tkinter.Label(top, text="Discount").grid(row=2, column = 6)
E32 = Tkinter.Entry(top, bd =2,width = 3)
E32.config(justify=Tkinter.CENTER)
E32.insert(3,'0.9')
E32.grid(row = 2, column = 7)

Tkinter.Label(top, text="Reward goal").grid(row=3, column = 6)
E33 = Tkinter.Entry(top, bd =2,width = 3)
E33.config(justify=Tkinter.CENTER)
E33.insert(3,'100')
E33.grid(row = 3, column = 7)

Tkinter.Label(top, text="Reward wall").grid(row=4, column = 6)
E34 = Tkinter.Entry(top, bd =2,width = 3)
E34.config(justify=Tkinter.CENTER)
E34.insert(3,'-10')
E34.grid(row = 4, column = 7)

Tkinter.Label(top, text="Reward robot").grid(row=1, column = 8)
E35 = Tkinter.Entry(top, bd =2,width = 4)
E35.config(justify=Tkinter.CENTER)
E35.insert(3,'-0.01')
E35.grid(row = 1, column = 9)

Tkinter.Label(top, text="Reward step").grid(row=2, column = 8)
E36 = Tkinter.Entry(top, bd =2,width = 4)
E36.config(justify=Tkinter.CENTER)
E36.insert(3,'-0.01')
E36.grid(row = 2, column = 9)

Tkinter.Label(top, text="Exploration rate").grid(row=3, column = 8)
E37 = Tkinter.Entry(top, bd =2,width = 4)
E37.config(justify=Tkinter.CENTER)
E37.insert(3,'0')
E37.grid(row = 3, column = 9)

""" Cooperative learning settings """
Tkinter.Label(top, text="Cooperation time").grid(row=1, column = 10)
E41 = Tkinter.Entry(top, bd =2,width = 4)
E41.config(justify=Tkinter.CENTER)
E41.insert(3,'50')
E41.grid(row = 1, column = 11)

PB1 = ttk.Progressbar(top, orient="horizontal", length=120, mode="determinate")
PB1.grid(row=0, column=12)
PB1["value"] = 0
PB1["maximum"] = int(E22.get())

B2 = Tkinter.Button(top, text ="Generate maze", command = generateMaze)
B2.grid(row=1, column=12)
B1 = Tkinter.Button(top, text ="Start simulation", command = startSim)
B1.grid(row=2, column=12)
B3 = Tkinter.Button(top, text ="Restart simulation", command = restartSim)
B3.grid(row=3, column=12)
B4 = Tkinter.Button(top, text ="Show maze", command = showMaze)
B4.grid(row=4, column=12)
B5 = Tkinter.Button(top, text ="Plot data", command = plotData)
B5.grid(row=5, column=12)

top.mainloop()
