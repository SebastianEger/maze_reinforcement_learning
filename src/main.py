import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from Tkinter import *
import pickle
from package.GUI.GUI import GUI

top = Tk()
top.wm_title('Simulation panel')
plt.ion()

# load configuration file
pkl_file = open('configuration.pkl', 'rb')
configuration = pickle.load(pkl_file)

print 'Loaded configuration: ' + str(configuration)


GUI = GUI(top, configuration)

top.mainloop()
