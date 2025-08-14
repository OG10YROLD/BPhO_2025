# Recreate graphs using model of glass refractive index and dispersion in a triangular prism
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s

# Sellmeier constants for BK7
a = [1.03961212, 0.231792344, 1.01146945]
b = [0.00600069867, 0.0200179144, 103.560653] # um^2
def sellmeier(fthz, a, b): # wavelength, a, b constants
    wlu = (c/1000000)/fthz # convert nanometres to micrometres
    dispersion = 0
    for k in range(len(a)):
        dispersion += (a[k]*(wlu**2))/((wlu**2)-b[k])
    n = math.sqrt(1+dispersion)
    return n
def watern(fthz): # frequency in THz
    return math.sqrt(math.sqrt(1/(1.731-(0.261*((fthz/(10**3))**2))))+1)
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

fig, (ax1, ax2) = plt.subplots(2)

ax1.set_title("θt vs θi given α=45°, f=542.5THz, θmax=5.787°")
ax1.set_xlim(0, 90)
ax1.set_ylim(0, 100)
ax1.set_xlabel("Angle of incidence /deg")
ax1.set_ylabel("Transmission angle θt /deg")

aoi = np.linspace(0, 90, 180)
ta = np.array([])
alpha = np.linspace(10, 80, 17)
da = []
for i in range(len(alpha)):
    da.append(np.array([]))
for i in range(len(aoi)):
    taval = np.degrees(np.arcsin(np.sqrt(sellmeier(542.5, a, b)**2 - np.sin(np.radians(aoi[i]))**2)*np.sin(np.radians(45)) - np.sin(np.radians(aoi[i]))*np.cos(np.radians(45))))
    ta = np.append(ta, taval)
    for j in range(len(alpha)):
        da[j] = np.append(da[j], aoi[i] + np.degrees(np.arcsin(np.sqrt(sellmeier(542.5, a, b)**2 - np.sin(np.radians(aoi[i]))**2)*np.sin(np.radians(alpha[j])) - np.sin(np.radians(aoi[i]))*np.cos(np.radians(alpha[j])))) - alpha[j])
ax1.plot(aoi[12:], ta[12:], color='b')
ax1.plot([5.787, 5.787], [-10, 120], color='r')

ax2.set_title("Deflection angle δ /deg using f=542.5THz")
ax2.set_xlim(0, 90)
ax2.set_ylim(0, 90)
ax2.set_xlabel("Angle of incidence /deg")
ax2.set_ylabel("Deflection angle δ /deg")

for i in range(len(alpha)):
    ax2.plot(aoi, da[i], color=colour(alpha[i]*5+355))

#plt.grid()

plt.show()