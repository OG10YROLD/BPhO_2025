# Create a spreadsheet with the u,v data and plot 1/v vs 1/u. From a line of best fit, assess
# the veracity of the thin lens equation, and determine the focal length f of the lens (in cm).
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s

u = [20, 25, 30, 35, 40, 45, 50, 55]
v = [65.5, 40, 31, 27, 25, 23.1, 21.5, 20.5]
f = 0

for i in range(len(u)):
    f += 1/((1/u[i]) + (1/v[i]))
f = f/len(u)

plt.text(0.01, 0.02, str(round(f, 5)) + " cm focal length")

xpoints = np.array([1/x for x in u])
ypoints = np.array([1/x for x in v])

plt.scatter(xpoints, ypoints)
plt.plot(np.unique(xpoints), np.poly1d(np.polyfit(xpoints, ypoints, 1))(np.unique(xpoints)), linestyle="dashed")

plt.title("Thin lens")
plt.xlabel("1/u")
plt.ylabel("1/v")

plt.xlim(0, 0.06)
plt.ylim(0, 0.06)
plt.grid()

plt.show()