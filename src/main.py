from Tkinter import *
import matplotlib.pyplot as plt
import pickle
from src.GUI.GUI import GUI

top = Tk()
top.wm_title('Simulation panel')
plt.ion()

# load configuration file
pkl_file = open('data.pkl', 'rb')
configuration = pickle.load(pkl_file)

print 'Loaded configuration: ' + str(configuration)


GUI = GUI(top, configuration)

top.mainloop()
