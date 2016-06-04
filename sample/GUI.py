import Tkinter
import ttk
from threading import Thread
import matplotlib.pyplot as plt

import robot_controller
import simulation
import numpy
from sample.mazes import dfs_maze
from sample.mazes import random_maze
from sample.mazes import static_mazes

top = Tkinter.Tk()
plt.ion()

maze = []

def startSimThread():
    thread = Thread(target=startSim, args=[])
    thread.start()

def startSim():
    start_positions = []
    goal_positions = []
    numberRobots = int(E5.get())
    PB1["value"] = 0

    """ Maze """
    # if LB2.curselection() == (0,):
    #     maze = static_mazes.get_static_maze_2()
    # if LB2.curselection() == (1,):
    #     maze = dfs_maze.generate_maze(int(E1.get()), int(E2.get()), True)
    # if LB2.curselection() == (2,):
    #     maze = random_maze.maze(int(E1.get()), int(E2.get()), float(E3.get()), float(E4.get()))
    # if LB2.curselection() == (3,):
    #     maze = static_mazes.get_static_maze_3()
    # if show_maze.get():
    #     print 'Show maze!'
    #     plt.figure(figsize=(10, 10))
    #     plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
    #     plt.show()

    """ set start and goal positions """
    maze_shape = numpy.shape(maze)
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


    """ Robot controller """
    robot_name = LB1.get(LB1.curselection()[0],LB1.curselection()[0])
    rc = robot_controller.RobotController(maze)
    rc.init_robots(robot_name[0],start_positions,goal_positions)
    rc.q_settings(float(E7.get()),float(E8.get()),float(E9.get()),float(E10.get()),float(E11.get()),float(E12.get()),float(E13.get()))

    """ Simulation """
    sim = simulation.Simulation(rc,maze)
    sim.do_plot = False
    # sim.do_plot = do_plot.get()
    data = []
    PB1.update_idletasks()
    for i in xrange(int(E6.get())):
        rc.reset_robots(start_positions,goal_positions)
        data.append(sim.run_simulation())
        PB1["value"] = i+1
        PB1.update_idletasks()

    sim.do_plot = do_plot.get()
    rc.reset_robots(start_positions,goal_positions)
    sim.run_simulation()
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
    plt.plot(data)
    plt.show()
    # nPB1["value"] = 0


def LB1onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    T1.config(state=Tkinter.NORMAL)
    if index == 0:
        T1.insert('1.0', 'Loaded Artemis | States: position | Actions: Top,left,right,down | Individual Q-learning  |\n')
    if index == 1:
        T1.insert('1.0', 'Loaded Butler  | States: position | Actions: Top,left,right,down | Cooperative Q-learning | Shared Q matrix\n')
    if index == 2:
        T1.insert('1.0', 'Loaded Koboi   | States: position | Actions: Top,left,right,down | Cooperative Q-learning | Learning from all | '
                         'Normal (Steps+Goal)\n')
    if index == 3:
        T1.insert('1.0', 'Loaded Holly   | States: position | Actions: Top,left,right,down | Cooperative Q-learning | Learning from Expert | '
                         'Distance to goal\n')
    T1.config(state=Tkinter.DISABLED)


def LB2onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    T1.config(state=Tkinter.NORMAL)
    if index == 0:
        T1.insert('1.0', 'Loaded Static Maze 1\n')
    if index == 1:
        T1.insert('1.0', 'Loaded Depth-first search maze | tree type, only one solution | Height and Width are doubled! \n')
    if index == 2:
        T1.insert('1.0', 'Loaded Random maze | random maze with more than one solution \n')
    T1.config(state=Tkinter.DISABLED)


def generate_maze():
    global maze
    if LB2.curselection() == (0,):
        maze = static_mazes.get_static_maze_2()
    if LB2.curselection() == (1,):
        maze = dfs_maze.generate_maze(int(E1.get()), int(E2.get()), True)
    if LB2.curselection() == (2,):
        maze = random_maze.maze(int(E2.get()), int(E1.get()), float(E3.get()), float(E4.get()))
    if LB2.curselection() == (3,):
        maze = static_mazes.get_static_maze_3()
    if LB2.curselection() == (4,):
        maze = dfs_maze.generate_maze_special(int(E1.get()), int(E2.get()))
    if show_maze.get():
        plt.figure(figsize=(10, 10))
        plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
        plt.show()


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
LB1.insert(Tkinter.END, "Koboi")
LB1.insert(Tkinter.END, "Holly")
LB1.bind('<<ListboxSelect>>', LB1onSelect)

T1 = Tkinter.Text(top, height=14, width=150)
T1.grid(row=6,column=0, columnspan=10)
#T1.tag_config('n',justify=Tkinter.LEFT)
#T1.insert(Tkinter.END, "No coop Q learning")
T1.config(state=Tkinter.DISABLED)

LB2 = Tkinter.Listbox(top, height=7, exportselection=0)
LB2.grid(row=1,column = 1, rowspan=5)
LB2.insert(Tkinter.END, "Static maze 1")
LB2.insert(Tkinter.END, "Depth-first search maze")
LB2.insert(Tkinter.END, "Random maze")
LB2.insert(Tkinter.END, "Static maze 3")
LB2.insert(Tkinter.END, "DFS special")
LB2.bind('<<ListboxSelect>>', LB2onSelect)

Tkinter.Label(top, text="Height").grid(row=1, column = 2)
E1 = Tkinter.Entry(top, bd =2,width = 3)
E1.config(justify=Tkinter.CENTER)
E1.insert(3,'10')
E1.grid(row = 1, column = 3)

Tkinter.Label(top, text="Width").grid(row=2, column = 2)
E2 = Tkinter.Entry(top, bd =2,width = 3)
E2.config(justify=Tkinter.CENTER)
E2.insert(3,'10')
E2.grid(row = 2, column = 3)

Tkinter.Label(top, text="Density").grid(row=3, column = 2)
E3 = Tkinter.Entry(top, bd =2,width = 3)
E3.config(justify=Tkinter.CENTER)
E3.insert(4,'0.75')
E3.grid(row = 3, column = 3)

Tkinter.Label(top, text="Complexity").grid(row=4, column = 2)
E4 = Tkinter.Entry(top, bd =2,width = 3)
E4.config(justify=Tkinter.CENTER)
E4.insert(4,'0.75')
E4.grid(row = 4, column = 3)

""" Simulation settings """

Tkinter.Label(top, text="Number robots").grid(row=1, column = 4)
E5 = Tkinter.Entry(top, bd =2,width = 3)
E5.config(justify=Tkinter.CENTER)
E5.insert(3,'10')
E5.grid(row = 1, column = 5)

do_plot = Tkinter.IntVar()
Tkinter.Label(top, text="Visualization").grid(row=2, column = 4)
C1 = Tkinter.Checkbutton(top,variable=do_plot)
C1.grid(row = 2, column = 5)

show_maze = Tkinter.IntVar()
Tkinter.Label(top, text="Show maze").grid(row=3, column = 4)
C2 = Tkinter.Checkbutton(top,variable=show_maze)
C2.select()
C2.grid(row = 3, column = 5)

Tkinter.Label(top, text="Iterations").grid(row=4, column = 4)
E6 = Tkinter.Entry(top, bd =2,width = 3)
E6.config(justify=Tkinter.CENTER)
E6.insert(4,'50')
E6.grid(row = 4, column = 5)

""" Q learning settings """

Tkinter.Label(top, text="Learn rate").grid(row=1, column = 6)
E7 = Tkinter.Entry(top, bd =2,width = 3)
E7.config(justify=Tkinter.CENTER)
E7.insert(3,'0.2')
E7.grid(row = 1, column = 7)

Tkinter.Label(top, text="Discount").grid(row=2, column = 6)
E8 = Tkinter.Entry(top, bd =2,width = 3)
E8.config(justify=Tkinter.CENTER)
E8.insert(3,'0.9')
E8.grid(row = 2, column = 7)

Tkinter.Label(top, text="Reward goal").grid(row=3, column = 6)
E9 = Tkinter.Entry(top, bd =2,width = 3)
E9.config(justify=Tkinter.CENTER)
E9.insert(3,'100')
E9.grid(row = 3, column = 7)

Tkinter.Label(top, text="Reward wall").grid(row=4, column = 6)
E10 = Tkinter.Entry(top, bd =2,width = 3)
E10.config(justify=Tkinter.CENTER)
E10.insert(3,'-10')
E10.grid(row = 4, column = 7)

Tkinter.Label(top, text="Reward robot").grid(row=1, column = 8)
E11 = Tkinter.Entry(top, bd =2,width = 4)
E11.config(justify=Tkinter.CENTER)
E11.insert(3,'-0.01')
E11.grid(row = 1, column = 9)

Tkinter.Label(top, text="Reward step").grid(row=2, column = 8)
E12 = Tkinter.Entry(top, bd =2,width = 4)
E12.config(justify=Tkinter.CENTER)
E12.insert(3,'-0.01')
E12.grid(row = 2, column = 9)

""" Cooperative learning settings """
Tkinter.Label(top, text="Cooperation time").grid(row=1, column = 10)
E13 = Tkinter.Entry(top, bd =2,width = 4)
E13.config(justify=Tkinter.CENTER)
E13.insert(3,'50')
E13.grid(row = 1, column = 11)

PB1 = ttk.Progressbar(top, orient="horizontal", length=120, mode="determinate")
PB1.grid(row=3, column=12)
PB1["value"] = 0
PB1["maximum"] = int(E6.get())

B1 = Tkinter.Button(top, text ="Start simulation", command = startSim)
B1.grid(row=2, column=12)
B2 = Tkinter.Button(top, text ="Generate maze", command = generate_maze)
B2.grid(row=1, column=12)
# start_button = Tkinter.Button(top, text ="Start simulation", command = startSim)
# stop_button = Tkinter.Button(top, text ="Stop simulation", command = stopSim)
#C = Tkinter.Button(top, text ="Hello", command = helloCallBack)


#start_button.pack()
#stop_button.pack()
top.mainloop()