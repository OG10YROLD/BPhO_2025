# Plot t vs x and confirm the travel time is minimized when x = L/2, which
# implies the angle of incidence θ equals the angle of reflection φ
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s

y = 1
L = 2
n = 1

def time(x):
    global y, L, n
    return ((math.sqrt(x**2 + y**2))/(c/n))+((math.sqrt((L - x)**2 + y**2))/(c/n))

times = []
for x in [x / 100.0 for x in range(0, 201, 1)]:
    times.append(time(x))

xpoints = np.array([x / 100.0 for x in range(0, 201, 1)])
ypoints = np.array(times)
plt.plot(xpoints, ypoints)

plt.scatter(np.array([xpoints[ypoints.argmin()]]), np.array([ypoints.min()]), color='r', marker='x', s=100)

plt.title("Law of reflection")
plt.xlabel("x /m")
plt.ylabel("Time of flight /s")

plt.xlim(0, 2)
plt.ylim(0.0000000090, 0.0000000110)
plt.grid()

plt.show()