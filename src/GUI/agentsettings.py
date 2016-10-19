from Tkinter import *


def init_frame(top, vMOV, vEXP, vExpertness, vWeighting, vExplorationRate):
    # Label
    Label(top, text="Agent settings",font = "Helvetica 14 bold italic").grid(row=0, column = 0, sticky=W)

    # Frame
    frameAgentCreator = Frame(bd=2, relief=GROOVE)
    frameAgentCreator.grid(row=1, column=0, sticky=EW)

    # Objects
    Label(frameAgentCreator, text="Movement model").grid(row=1, column = 0)
    vMOV.set("North East South West")  # default value
    OM1 = OptionMenu(frameAgentCreator, vMOV, "North East South West", "Forward Backward Turn", "Forward Right Backward Left")
    OM1.grid(row=1,column = 1, sticky=EW)
    OM1.config(justify=LEFT)

    Label(frameAgentCreator, text="Exploration model").grid(row=2, column = 0)
    vEXP.set("Random") # default value
    OM2 = OptionMenu(frameAgentCreator, vEXP, "Random", "Smart Random", "Decreasing Exploration Rate")
    OM2.grid(row=2,column = 1, sticky=EW)
    OM2.config(justify=LEFT)

    Label(frameAgentCreator, text="Expertness model").grid(row=1, column = 2)
    vExpertness.set("Normal") # default value
    OM3 = OptionMenu(frameAgentCreator, vExpertness, "Normal", "Absolute", "Positive")
    OM3.grid(row=1,column = 3, sticky=EW)
    OM3.config(justify=LEFT)

    Label(frameAgentCreator, text="Weighting model").grid(row=2, column = 2)
    vWeighting.set("Learn From All") # default value
    OM4 = OptionMenu(frameAgentCreator, vWeighting, "Learn From All")
    OM4.grid(row=2, column = 3, sticky=EW)
    OM4.config(justify=LEFT)

    Label(frameAgentCreator, text="Exploration rate").grid(row=1, column = 4)
    vExplorationRate.set("Constant") # default value
    OM5 = OptionMenu(frameAgentCreator, vExplorationRate, "Constant", "Decreasing over steps")
    OM5.grid(row=1, column = 5, sticky=EW)

    variable2 = StringVar(top)
    Label(frameAgentCreator, text="Number goals").grid(row=2, column = 4)
    variable2.set("One Goal") # default value
    OM6 = OptionMenu(frameAgentCreator, variable2, "One Goal", "Multiple Goals")
    OM6.grid(row=2, column = 5, sticky=EW)
