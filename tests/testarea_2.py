
import numpy


mat = numpy.zeros((5,5))
mat[3, 3] = 3

mat[1,4] = 5.5

print mat/mat.max()
