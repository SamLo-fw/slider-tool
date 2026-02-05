import numpy as np
import matplotlib.pyplot as plt

a, b, c, d = 0.9, -0.6013, 2.0, 0.5

x, y = 0.1, 0.1
burn_in = 1000
steps = 100_000

xs = []
ys = []

for i in range(steps + burn_in):
    x, y = (
        x*x - y*y + a*x + b*y,
        2*x*y + c*x + d*y
    )
    if i >= burn_in:
        xs.append(x)
        ys.append(y)

plt.scatter(xs, ys, s=0.1)
plt.axis('equal')
plt.show()
