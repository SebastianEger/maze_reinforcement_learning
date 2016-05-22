import Tkinter
import simulation
import maze_generator
import robot_controller
import thread

top = Tkinter.Tk()


def startSim():
    maze = maze_generator.get_static_maze_1()
    rc = robot_controller.RobotController(int(E1.get()),maze,0)
    rc.set_exploration_mode(int(E3.get()))
    rc.set_exploration_rate(float(E2.get()))
    sim = simulation.Simulation(rc,maze)
    sim.refresh_rate = float(E6.get())
    print int(E4.get())
    for _ in range(1):
        rc.reset_robots()
        sim.run_simulation()
    pass

Tkinter.Label(top, text="Number of robots").grid(row=0)
E1 = Tkinter.Entry(top, bd =2,width = 5)
E1.config(justify=Tkinter.RIGHT)
E1.insert(0,'1')
E1.grid(row = 0, column = 1)

Tkinter.Label(top, text="Exploration rate").grid(row=1)
E2 = Tkinter.Entry(top, bd =2,width = 5)
E2.config(justify=Tkinter.RIGHT)
E2.insert(0,'0.4')
E2.grid(row=1, column = 1)

Tkinter.Label(top, text="Exploration mode").grid(row=2)
E3 = Tkinter.Entry(top, bd =2,width = 5)
E3.config(justify=Tkinter.RIGHT)
E3.insert(0,'1')
E3.grid(row=2, column = 1)

Tkinter.Label(top, text="Number of runs").grid(row=3)
E4 = Tkinter.Entry(top, bd =2,width = 5)
E4.config(justify=Tkinter.RIGHT)
E4.insert(0,'1')
E4.grid(row=3, column = 1)

Tkinter.Label(top, text="Do plot").grid(row=4)
E5 = Tkinter.Entry(top, bd =2,width = 5)
E5.config(justify=Tkinter.RIGHT)
E5.insert(0,'0')
E5.grid(row=4, column = 1)

Tkinter.Label(top, text="Refreshrate").grid(row=5)
E6 = Tkinter.Entry(top, bd =2,width = 5)
E6.config(justify=Tkinter.RIGHT)
E6.insert(0,'0.0')
E6.grid(row=5, column = 1)

start_button = Tkinter.Button(top, text ="Start simulation", command = startSim)
start_button.grid(row=6, column=1)

# start_button = Tkinter.Button(top, text ="Start simulation", command = startSim)
# stop_button = Tkinter.Button(top, text ="Stop simulation", command = stopSim)
#C = Tkinter.Button(top, text ="Hello", command = helloCallBack)


#start_button.pack()
#stop_button.pack()
top.mainloop()