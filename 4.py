# Plot travel time t vs x and hence demonstrate
# Snell’s Law of refraction. Inputs are wave speeds c1 and c2
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s
n1 = 1
n2 = 1.5

y = 1
Y = 1
L = 2

def time(x):
    global y, Y, L, n1, n2
    return ((math.sqrt(x**2 + y**2))/(c/n1))+((math.sqrt((L - x)**2 + Y**2))/(c/n2))

times = []
for x in [x / 100.0 for x in range(0, 201, 1)]:
    times.append(time(x))

xpoints = np.array([x / 100.0 for x in range(0, 201, 1)])
ypoints = np.array(times)
plt.plot(xpoints, ypoints)

plt.scatter(np.array([xpoints[ypoints.argmin()]]), np.array([ypoints.min()]), color='r', marker='x', s=100)

theta_1 = math.atan(xpoints[ypoints.argmin()]/y)
theta_2 = math.atan((L-xpoints[ypoints.argmin()])/Y)

plt.title("Law of refraction: n1sin(θ1) = " + str(round(n1*math.sin(theta_1), 5)) + " n2sin(θ2) = " + str(round(n2*math.sin(theta_2), 5)))
plt.xlabel("x /m")
plt.ylabel("Time of flight /s")

plt.xlim(0, 2)
plt.ylim(0.0000000110, 0.0000000150)
plt.grid()

plt.show()