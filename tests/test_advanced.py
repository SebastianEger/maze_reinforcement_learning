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
LB2.insert(END, "Depth-first search maze")
LB2.insert(END, "URMG")
LB2.insert(END, "Static maze 3")
LB2.insert(END, "DFS special")
LB2.bind('<<ListboxSelect>>', LB2onSelect)

# Maze settings
Label(frameSettings, text="Random maze settings", font = "Helvetica 14 bold italic", width=20).grid(row=0, column = 1, columnspan=2)

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

# Simulation settings
Label(frameSettings, text="Simulation settings", font = "Helvetica 14 bold italic", width = 20).grid(row=0, column = 3, columnspan=2)

startColumn = 3
startRow = 1

Label(frameSettings, text="Number agentcontroller").grid(row=startRow, column = startColumn)
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
E23.insert(3, '15000')
E23.grid(row=startRow+2, column=startColumn+1)

# Q learning settings
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
E37.insert(3,'0.2')
E37.grid(row = startRow+2, column = startColumn+3)

Label(frameSettings, text="Cooperation time").grid(row=startRow+3, column = startColumn+2)
E41 = Entry(frameSettings, bd =2,width = 4)
E41.config(justify=CENTER)
E41.insert(3,'-1')
E41.grid(row = startRow+3, column = startColumn+3)

# Additional options
Label(frameSettings, text="Additional Options", font = "Helvetica 14 bold italic", width=25).grid(row=0, column = 9, columnspan=2)

useQshared = IntVar()
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
