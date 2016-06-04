import numpy as np
from collections import Counter

a = [0,0,0,-2]
b = [0,1,2,3]
copy = b[0:3]

np.random.shuffle(copy)

b[0:3] = copy
print b
print a.count(0)

