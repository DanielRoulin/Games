import numpy as np
from renderer import HUSCIIRenderer

r = HUSCIIRenderer(40, 20)

P = np.array([20, 10])
# r.point(P[0][0], P[1][0], "I")

# Translation
T = np.array([-10, 5])
P = P + T
print(P)
# r.point(P[0][0], P[1][0], "T")

# Rotation
a = 0
a = np.radians(a)
R = np.array([[np.cos(a),  np.sin(a)],
              [-np.sin(a), np.cos(a)]])

print(P[0][0], P[1][0])
P = P * R
print(P[0][0], P[1][0])
r.point(P[0][0], P[1][0], "R")

# r.draw()