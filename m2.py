import math
import numpy as np

PHI = 1.61803398874989484820458683
PHIS = 1/PHI

class Point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def position(self) -> tuple:
        return np.array([self.x,self.y,self.z])

    @staticmethod
    def distance(p1, p2) -> float:
        x = p2.x - p1.x
        y = p2.y - p1.y
        z = p2.z - p1.z
        return (math.sqrt(x**2 + y**2 + z**2))

    @staticmethod
    def rotX(angle, matrix):
        rotation_matrix = np.array([
            [1,     0,                  0               ],
            [0,     math.cos(angle),    -math.sin(angle)],
            [0,     math.sin(angle),    math.cos(angle) ]
        ])
        return matrix @ rotation_matrix.T

    @staticmethod
    def rotY(angle, matrix):
        rotation_matrix = np.array([
            [math.cos(angle),   0,      math.sin(angle) ],
            [0,                 1,      0               ],
            [-math.sin(angle),  0,      math.cos(angle) ]
        ])
        return matrix @ rotation_matrix.T

    @staticmethod
    def rotZ(angle, matrix):
        rotation_matrix = np.array([
            [math.cos(angle),   -math.sin(angle),   0],
            [math.sin(angle),   math.cos(angle),    0],
            [0,                 0,                  1]
        ])
        return matrix @ rotation_matrix.T


class Dodecahedron:
    
    a = Point(0, PHIS, 1)
    b = Point(PHI, PHI, PHI)
    c = Point(1, 0, PHIS)
    d = Point(-1, 0, PHIS)
    e = Point(-PHI, PHI, PHI)
    f = Point(-PHI, PHI, -PHI)
    g = Point(0, PHIS, -1)
    h = Point(PHI, PHI, -PHI)
    i = Point(PHIS, 1, 0)
    j = Point(PHIS, -1, 0)
    k = Point(PHI, -PHI, PHI)
    l = Point(0, -PHIS, 1)
    m = Point(-PHI, -PHI, PHI)
    n = Point(-PHIS, -1, 0)
    o = Point(-PHIS, 1, 0)
    p = Point(-1, 0, -PHIS)
    q = Point(1, 0, -PHIS)
    r = Point(PHI, -PHI, -PHI)
    s = Point(0, -PHIS, -1)
    t = Point(-PHI, -PHI, -PHI)

    def __init__(self):
        self.path = [self.t, self.p, self.f, self.o, self.n, self.t, self.s, self.l, self.m, self.n, self.o, self.e, self.d, self.m, self.d, self.c, self.k, self.l, self.k, self.j, self.i, self.b, self.i, self.h, self.g, self.a, self.b, self.a, self.e, self.a, self.g, self.f, self.p, self.q, self.h, self.q, self.r, self.j, self.r, self.s]
        self.path_positions = np.array([v.position() for v in self.path])


if __name__ == "__main__":
    #.. okay now what lmao
    # i guess we take those points and define a rotate operation as a matrix
    # then for each frame we project that set of points onto a 2d plane 
    # & scale to fit the screen pixel dimensions for the osu playfield

    # then convert each frame into a slider, which I will figure out... later

    dd = Dodecahedron()
    