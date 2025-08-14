# Create a model of the refractive index of water with frequency
# (and hence wavelength in a vacuum), over the range 405THz to 790THz
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s

def watern(fthz): # frequency in THz
    return math.sqrt(math.sqrt(1/(1.731-(0.261*((fthz/(10**3))**2))))+1)
print(watern(700))
def colour(fthz):
    if (fthz >= 405) and (fthz < 480):
        col = [1, (fthz-405)/150, 0] # G = 0-0.5
    elif (fthz >= 480) and (fthz < 510):
        col = [1, 0.5+((fthz-480)/60), 0] # G = 0.5-1.0
    elif (fthz >= 510) and (fthz < 530):
        col = [1-((fthz-510)/20), 1, 0] # R = 1.0-0.0
    elif (fthz >= 530) and (fthz < 600):
        col = [0, 1, ((fthz-530)/140)] # B = 0.0-0.5
    elif (fthz >= 600) and (fthz < 620):
        col = [0, 1-((fthz-600)/80), 0.5+((fthz-600)/40)] # G = 1.0-0.75, B = 0.5-1.0
    elif (fthz >= 620) and (fthz < 680):
        col = [0, 0.75-((fthz-620)/80), 1] # G = 0.75-0.0
    elif (fthz >= 680) and (fthz <= 790):
        col = [((fthz-680)/220), 0, 1] # R = 0.0-0.5
    return col

for fthz in range(405, 791, 1):
    plt.scatter(np.array([fthz]), np.array([watern(fthz)]), color=colour(fthz))

plt.title("Refractive index of water")
plt.xlabel("Frequency / THz")
plt.ylabel("Refractive index")

plt.xlim(405, 790)
plt.ylim(1.33, 1.342)
plt.grid()

plt.show()