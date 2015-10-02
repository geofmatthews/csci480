import numpy
import sympy
from sympy.abc import *
sympy.init_printing()

numpy123 = numpy.array([[1,2],
                        [3,4]], dtype=float)
sympyABC = sympy.Matrix([[a,b],
                         [c,d]])
sympy123 = sympy.Matrix([[1,2],
                         [3,4]])

def inverseAndProduct(a, inv, prod):
    print "Array:"
    print a
    print "Inverse:"
    print inv
    print "Product:"
    print prod
    
inverseAndProduct(numpy123,
                  numpy.linalg.inv(numpy123),
                  numpy.dot(numpy123, numpy.linalg.inv(numpy123)))
inverseAndProduct(sympy123,
                  sympy123.inv(),
                  sympy123 * sympy123.inv())
inverseAndProduct(sympyABC,
                  sympyABC.inv(),
                  sympyABC * sympyABC.inv())

prod = sympyABC * sympyABC.inv()

dets = [numpy.linalg.det(numpy123), sympy123.det(), sympyABC.det()]
print dets

aa = sympy.Matrix([[1,0,-x],
                  [0,1,-y],
                  [0,0,1]])

bb = sympy.Matrix([[c,-s,0],
                  [s,c,0],
                  [0,0,1]])

cc = aa.inv()

print aa
print bb
print cc
print aa * bb * cc

s2 = sympy.sqrt(2)
dd = sympy.Matrix([[s2/2, -s2/2, 0],
                  [s2/2, s2/2,0],
                  [0,0,1]])
                  
ee = sympy.Matrix([[-1,0,0],
                  [0,1,0],
                  [0,0,1]])

ff = dd.transpose()


print ff * ee * dd


gg = sympy.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
hh = sympy.Matrix([[-1,0,0],[0,1,0],[0,0,1]])
print hh
print gg
print hh * gg


