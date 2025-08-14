# Use the Sellmeier formula to plot the refractive index of crown glass vs wavelength 
# over the range of visible light (approximately 400nm to 800nm).
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s

# Sellmeier constants for BK7
a = [1.03961212, 0.231792344, 1.01146945]
b = [0.00600069867, 0.0200179144, 103.560653] # um^2

def sellmeier(wlnm, a, b): # wavelength, a, b constants
    wlu = wlnm / (10**3) # convert nanometres to micrometres
    dispersion = 0
    for k in range(len(a)):
        dispersion += (a[k]*(wlu**2))/((wlu**2)-b[k])
    n = math.sqrt(1+dispersion)
    return n

values = []
for wlnm in range(400, 801, 1):
    values.append(sellmeier(wlnm, a, b))

xpoints = np.array(list(range(400, 801, 1)))
ypoints = np.array(values)

plt.title("Refractive index of BK7 crown glass")
plt.xlabel("λ / nm")
plt.ylabel("n")

plt.xlim(400, 800)
plt.ylim(1.51, 1.535)
plt.grid()

plt.plot(xpoints, ypoints)
plt.show()