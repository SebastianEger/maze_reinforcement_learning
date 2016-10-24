from Tkinter import *


class AgentSettings:
    def __init__(self, GUI, top, configuration):
        self.GUI = GUI

        self.mov_modul = StringVar(top)
        self.mov_modul.set(configuration.get('mov', 'North East South West'))
        
        self.exp_modul = StringVar(top)
        self.exp_modul.set(configuration.get('exp', 'Random'))
        
        self.expertness = StringVar(top)
        self.expertness.set(configuration.get('expertness', 'Normal'))
        
        self.weighting = StringVar(top)
        self.weighting.set(configuration.get('weighting', 'Learn From All'))
        
        self.exploration_type = StringVar(top)
        self.exploration_type.set(configuration.get('exploration_type', 'Constant'))
        
        self.action_selection = StringVar(top)
        self.action_selection.set(configuration.get('action_selection', 'Greedy'))

        self.agent_speed = StringVar(top)
        self.agent_speed.set(configuration.get('agent_speed', 'All equal'))

        
        Label(top, text="Agent settings",font = "Helvetica 14 bold italic").grid(row=0, column = 0, sticky=W)
    
        # Frame
        self.frame = Frame(bd=2, relief=GROOVE)
        self.frame.grid(row=1, column=0, sticky=EW)
    
        # Objects
        Label(self.frame, text="Movement model").grid(row=1, column = 0)
        OM1 = OptionMenu(self.frame, self.mov_modul, "North East South West", "Forward Backward Turn", "Forward Right Backward Left")
        OM1.config(width=25)
        OM1.grid(row=1,column = 1, sticky=EW)
        OM1.config(justify=LEFT)
    
        Label(self.frame, text="Exploration model").grid(row=2, column = 0)
        OM2 = OptionMenu(self.frame, self.exp_modul, "Random", "Smart Random")
        OM2.grid(row=2,column = 1, sticky=EW)
        OM2.config(justify=LEFT)
    
        Label(self.frame, text="Expertness model").grid(row=1, column = 2)
        OM3 = OptionMenu(self.frame, self.expertness, "Normal", "Absolute", "Positive", "Distance To Goal", 'Needed Steps')
        OM3.config(width=20)
        OM3.grid(row=1,column = 3, sticky=EW)
        OM3.config(justify=LEFT)
    
        Label(self.frame, text="Weighting model").grid(row=2, column = 2)
        OM4 = OptionMenu(self.frame, self.weighting, "Learn From All", "Learn From All Positive")
        OM4.grid(row=2, column = 3, sticky=EW)
        OM4.config(justify=LEFT)
    
        Label(self.frame, text="Exploration rate").grid(row=1, column = 4)
        OM5 = OptionMenu(self.frame, self.exploration_type, "Constant", "1/(trial+1)")
        OM5.config(width=20)
        OM5.grid(row=1, column = 5, sticky=EW)
    
        Label(self.frame, text="Action selection").grid(row=2, column = 4)
        OM6 = OptionMenu(self.frame, self.action_selection, "Greedy", "Probabilistic")
        OM6.grid(row=2, column = 5, sticky=EW)

        Label(self.frame, text="Agent speed").grid(row=1, column = 6)
        OM7 = OptionMenu(self.frame, self.agent_speed, "All Equal", "2 different speeds", "3 different speeds")
        OM7.config(width=20)
        OM7.grid(row=1, column = 7, sticky=EW)

    def get_configuration(self, configuration):
        configuration['mov'] = self.mov_modul.get()
        configuration['exp'] = self.exp_modul.get()
        configuration['expertness'] = self.expertness.get()
        configuration['weighting'] = self.weighting.get()
        configuration['exploration_type'] = self.exploration_type.get()
        configuration['action_selection'] = self.action_selection.get()
        configuration['agent_speed'] = self.agent_speed.get()
    
    
class SimulationSettings:
    def __init__(self, GUI, top, configuration):
        self.GUI = GUI

        self.cooperation_type = StringVar(top)
        self.cooperation_type.set(configuration.get('cooperation_type', 'Trials'))


        # Label
        Label(top, text="Simulation settings",font = "Helvetica 14 bold italic").grid(row=2, column = 0, sticky=W)
        
        # Frame
        frameSettings = Frame(bd=2, relief=GROOVE)
        frameSettings.grid(row=4, column=0)
        
        # Objects
        """ Maze selection """
        Label(frameSettings, text="Maze",font = "Helvetica 14 bold italic", width=15).grid(row=0, column = 0)
        self.LB2 = Listbox(frameSettings, exportselection=0)
        self.LB2.grid(row=1,column = 0, rowspan = 5)
        self.LB2.insert(END, "Static maze 1")
        self.LB2.insert(END, "Static maze 3")
        self.LB2.insert(END, "Static maze 4")
        self.LB2.insert(END, "URMG")
        self.LB2.insert(END, "Depth-first search")
        self.LB2.insert(END, "DFS special")
        # LB2.select_set(configuration.get('maze', 0))
        self.LB2.select_set(0)
        self.LB2.bind('<<ListboxSelect>>', self.LB2onSelect)
        
        # Maze settings
        Label(frameSettings, text="Random maze settings", font = "Helvetica 14 bold italic", width=20).grid(row=0, column = 1, columnspan=2)
        
        startColumn = 1
        startRow = 1
        Label(frameSettings, text="Height").grid(row=startRow, column = startColumn)
        self.E11 = Entry(frameSettings, bd =2,width = 5)
        self.E11.config(justify=CENTER)
        self.E11.insert(3,'10')
        self.E11.grid(row = startRow, column = startColumn+1)
        
        Label(frameSettings, text="Width").grid(row=startRow+1, column = startColumn)
        self.E12 = Entry(frameSettings, bd =2,width = 5)
        self.E12.config(justify=CENTER)
        self.E12.insert(3,'10')
        self.E12.grid(row = startRow+1, column = startColumn+1)
        
        Label(frameSettings, text="Density").grid(row=startRow+2, column = startColumn)
        self.E13 = Entry(frameSettings, bd =2,width = 5)
        self.E13.config(justify=CENTER)
        self.E13.insert(4,'0.75')
        self.E13.grid(row = startRow+2, column = startColumn+1)
        
        Label(frameSettings, text="Complexity").grid(row=startRow+3, column = startColumn)
        self.E14 = Entry(frameSettings, bd =2,width = 5)
        self.E14.config(justify=CENTER)
        self.E14.insert(4,'0.75')
        self.E14.grid(row = startRow+3, column = startColumn+1)
        
        # Simulation settings
        Label(frameSettings, text="Simulation settings", font = "Helvetica 14 bold italic", width = 20).grid(row=0, column = 3, columnspan=2)
        
        startColumn = 3
        startRow = 1
        
        Label(frameSettings, text="Number agents").grid(row=startRow, column = startColumn)
        self.E21 = Entry(frameSettings, bd =2,width = 5)
        self.E21.config(justify=CENTER)
        self.E21.insert(3, configuration.get('number_agents', 5))
        self.E21.grid(row = startRow, column = startColumn+1)
        
        Label(frameSettings, text="Iterations").grid(row=startRow+1, column = startColumn)
        self.E22 = Entry(frameSettings, bd =2,width = 5)
        self.E22.config(justify=CENTER)
        self.E22.insert(4, configuration.get('iterations', 50))
        self.E22.grid(row = startRow+1, column = startColumn+1)
        
        Label(frameSettings, text="Max steps").grid(row=startRow+2, column = startColumn)
        self.E23 = Entry(frameSettings, bd =2, width = 5)
        self.E23.config(justify=CENTER)
        self.E23.insert(3, configuration.get('max_steps', 5000))
        self.E23.grid(row=startRow+2, column=startColumn+1)
        
        Label(frameSettings, text="Repetitions").grid(row=startRow+3, column = startColumn)
        self.E24 = Entry(frameSettings, bd =2, width = 5)
        self.E24.config(justify=CENTER)
        self.E24.insert(3, configuration.get('repetitions', 1))
        self.E24.grid(row=startRow+3, column=startColumn+1)
        
        
        # Q learning settings
        Label(frameSettings, text="Q-learning settings", font = "Helvetica 14 bold italic", width = 50).grid(row=0, column = 5, columnspan=4)
        
        
        startColumn = 5
        startRow = 1
        
        Label(frameSettings, text="Learn rate").grid(row=startRow, column = startColumn)
        self.E31 = Entry(frameSettings, bd =2,width = 5)
        self.E31.config(justify=CENTER)
        self.E31.insert(3, configuration.get('learn_rate', 1))
        self.E31.grid(row = startRow, column = startColumn+1)
        
        Label(frameSettings, text="Discount").grid(row=startRow+1, column = startColumn)
        self.E32 = Entry(frameSettings, bd =2,width = 5)
        self.E32.config(justify=CENTER)
        self.E32.insert(3, configuration.get('discount', 0.9))
        self.E32.grid(row = startRow+1, column = startColumn+1)
        
        Label(frameSettings, text="Reward goal").grid(row=startRow+2, column = startColumn)
        self.E33 = Entry(frameSettings, bd =2,width = 5)
        self.E33.config(justify=CENTER)
        self.E33.insert(3, configuration.get('reward_goal', 100))
        self.E33.grid(row = startRow+2, column = startColumn+1)
        
        Label(frameSettings, text="Reward wall").grid(row=startRow+3, column = startColumn)
        self.E34 = Entry(frameSettings, bd =2,width = 5)
        self.E34.config(justify=CENTER)
        self.E34.insert(3, configuration.get('reward_wall', -10))
        self.E34.grid(row = startRow+3, column = startColumn+1)
        
        Label(frameSettings, text="Reward step").grid(row=startRow, column = startColumn+2)
        self.E35 = Entry(frameSettings, bd =2,width = 5)
        self.E35.config(justify=CENTER)
        self.E35.insert(3, configuration.get('reward_step', -0.01))
        self.E35.grid(row = startRow, column = startColumn+3)
        
        Label(frameSettings, text="Tau").grid(row=startRow+1, column = startColumn+2)
        self.E36 = Entry(frameSettings, bd =2,width = 5)
        self.E36.config(justify=CENTER)
        self.E36.insert(3, configuration.get('tau', 0.1))
        self.E36.grid(row = startRow+1, column = startColumn+3)
        
        Label(frameSettings, text="Exploration rate").grid(row=startRow+2, column = startColumn+2)
        self.E37 = Entry(frameSettings, bd =2,width = 5)
        self.E37.config(justify=CENTER)
        self.E37.insert(3, configuration.get('exploration_rate', 0.1))
        self.E37.grid(row = startRow+2, column = startColumn+3)
        
        Label(frameSettings, text="Cooperation time").grid(row=startRow+3, column = startColumn+2)
        self.E41 = Entry(frameSettings, bd =2,width = 5)
        self.E41.config(justify=CENTER)
        self.E41.insert(3, configuration.get('cooperation_time', -1))
        self.E41.grid(row = startRow+3, column = startColumn+3)
        
        # Additional options
        Label(frameSettings, text="Additional Options", font = "Helvetica 14 bold italic", width=25).grid(row=0, column = 9, columnspan=2)
        
        self.use_shared_Q = IntVar()
        self.use_shared_Q.set(configuration.get('use_shared_Q', 0))
        Label(frameSettings, text="Use shared Q matrix").grid(row=1, column = 9)
        C31 = Checkbutton(frameSettings,variable=self.use_shared_Q)
        C31.grid(row = 1, column = 10)

        Label(frameSettings, text="Cooperation type").grid(row=2, column = 9)
        OM1 = OptionMenu(frameSettings, self.cooperation_type, 'Trials', "Steps")
        OM1.config(width=10)
        OM1.grid(row=2, column = 10, sticky=EW)

        self.frame = frameSettings

    def get_configuration(self, configuration):
        configuration['number_agents'] = int(self.E21.get())
        configuration['use_shared_Q'] = self.use_shared_Q.get()
        configuration['learn_rate'] = float(self.E31.get())
        configuration['discount'] = float(self.E32.get())
        configuration['reward_goal'] = float(self.E33.get())
        configuration['reward_wall'] = float(self.E34.get())
        # configuration['reward_robot'] = float(self.E35.get())
        configuration['tau'] = float(self.E36.get())
        configuration['reward_step'] = float(self.E35.get())
        configuration['exploration_rate'] = float(self.E37.get())
        configuration['cooperation_time'] = float(self.E41.get())
        configuration['maze'] = self.LB2.get(self.LB2.curselection())
        configuration['iterations'] = self.E22.get()
        configuration['repetitions'] = int(self.E24.get())
        configuration['max_steps'] = int(self.E23.get())

    def LB2onSelect(self, evt):
        self.GUI.generate_new_maze()
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


class Buttons:
    def __init__(self, GUI, simulation_settings_frame):
        # Buttons
        startColumn = 0
        startRow = 9    
        
        self.B1 = Button(simulation_settings_frame, text ="Start simulation", command = GUI.start_simulation)
        self.B1.grid(row=startRow, column=startColumn+3, columnspan=2)
        
        self.B2 = Button(simulation_settings_frame, text ="Generate maze", command = GUI.generate_new_maze)
        self.B2.grid(row=startRow, column=startColumn+1, columnspan=2)
        
        self.B3 = Button(simulation_settings_frame, text ="Restart simulation", command = GUI.restart_simulation)
        self.B3.grid(row=startRow+1, column=startColumn+3, columnspan=2)
        
        self.B4 = Button(simulation_settings_frame, text ="Show maze", command = GUI.show_maze)
        self.B4.grid(row=startRow, column=startColumn)
        
        self.B5 = Button(simulation_settings_frame, text ="Plot data", command = GUI.plotData)
        self.B5.grid(row=startRow, column=startColumn+9, columnspan=2)
        
        self.B6 = Button(simulation_settings_frame, text ="Visualize", command = GUI.visualize)
        self.B6.grid(row=startRow+1, column=startColumn+9, columnspan=2)
        
        self.B7 = Button(simulation_settings_frame, text ="Decision maze (only NESW model)", command = GUI.showDecisionMaze)
        self.B7.grid(row=startRow+2, column=startColumn+9, columnspan=2)
