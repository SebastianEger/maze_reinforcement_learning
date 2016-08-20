import numpy as np
import matplotlib.pyplot as plt

maze = np.zeros((4,8,5),dtype=np.uint8)
maze[0,:,0] = 1
maze[3,:,0] = 1
maze[:,0,0] = 1
maze[:,7,0] = 1
maze[1,2,0] = 1
maze[1,4,0] = 1
maze[1,5,0] = 1

plt.figure(figsize=(10, 10))
plt.imshow(maze[:,:,0], cmap=plt.cm.binary, interpolation='nearest')
plt.show()