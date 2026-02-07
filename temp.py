import math

PHI = (1 + math.sqrt(5)) / 2
PHIS = 1 / PHI

class D:
    a = (0, PHIS, 1)
    b = (PHI, PHI, PHI)
    c = (1, 0, PHIS)
    d = (-1, 0, PHIS)
    e = (-PHI, PHI, PHI)
    f = (-PHI, PHI, -PHI)
    g = (0, PHIS, -1)
    h = (PHI, PHI, -PHI)
    i = (PHIS, 1, 0)
    j = (PHIS, -1, 0)
    k = (PHI, -PHI, PHI)
    l = (0, -PHIS, 1)
    m = (-PHI, -PHI, PHI)
    n = (-PHIS, -1, 0)
    o = (-PHIS, 1, 0)
    p = (-1, 0, -PHIS)
    q = (1, 0, -PHIS)
    r = (PHI, -PHI, -PHI)
    s = (0, -PHIS, -1)
    t = (-PHI, -PHI, -PHI)

path = [D.t, D.p, D.f, D.o, D.n, D.t, D.s, D.l, D.m, D.n, D.o, D.e, D.d, D.m, D.d, D.c, D.k, D.l, D.k, D.j, D.i, D.b, D.i, D.h, D.g, D.a, D.b, D.a, D.e, D.a, D.g, D.f, D.p, D.q, D.h, D.q, D.r, D.j, D.r, D.s]

def dist(p1, p2):
    return math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))

# Check distances
distances = []
for i in range(len(path) - 1):
    d = dist(path[i], path[i+1])
    distances.append(d)
    
print(f"Unique distances: {set(round(d, 6) for d in distances)}")
print(f"Number of edges in path: {len(distances)}")

for i in range(len(path) - 1):
    d = dist(path[i], path[i+1])
    if abs(d - 2.0) > 0.1:  # Not a proper edge
        print(f"BAD EDGE {i}: {path[i]} -> {path[i+1]}, distance = {d:.3f}")