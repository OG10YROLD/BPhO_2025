# Plot graphs of rainbow elevation ε vs angle of incidence θ
import matplotlib.pyplot as plt
import numpy as np
import math

c = 299792458 #m/s

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

th = np.linspace(0, 90, 500)
fqs = np.linspace(405, 790, 15)

e1 = []
for i in range(len(fqs)):
    e1.append(np.array([]))
    for j in range(len(th)):
        e1[i] = np.append(e1[i], 4*np.degrees(np.arcsin(np.sin(np.radians(th[j]))/watern(fqs[i]))) - 2*th[j])

ep = []
for i in range(len(fqs)):
    ep.append(np.array([]))
    thp = np.arcsin(np.sqrt((4-(watern(fqs[i])**2))/3)) # radians
    for j in range(len(th)):
        ep[i] = np.append(ep[i], 4*np.degrees(np.arcsin(np.sin(thp)/watern(fqs[i]))) - 2*np.degrees(thp))

e2 = []
for i in range(len(fqs)):
    e2.append(np.array([]))
    for j in range(len(th)):
        e2[i] = np.append(e2[i], np.degrees(np.pi - 6*np.arcsin(np.sin(np.radians(th[j]))/watern(fqs[i]))) + 2*th[j])

es = []
for i in range(len(fqs)):
    es.append(np.array([]))
    ths = np.arcsin(np.sqrt((9-(watern(fqs[i])**2))/8)) # radians
    for j in range(len(th)):
        es[i] = np.append(es[i], np.degrees(np.pi - 6*np.arcsin(np.sin(ths)/watern(fqs[i])) + 2*ths))

for i in range(len(e1)):
    plt.plot(th, e1[i], color=colour(fqs[i]), linewidth=2.0)
    plt.plot(th, ep[i], color=colour(fqs[i]), linewidth=2.0)
    plt.plot(th, e2[i], color=colour(fqs[i]), linewidth=2.0)
    plt.plot(th, es[i], color=colour(fqs[i]), linewidth=2.0)

plt.title(f"Elevation of deflected beam /deg\nPrimary ε = {round(np.min(ep), 3)}°-{round(np.max(ep), 3)}°, Secondary ε = {round(np.min(es), 3)}°-{round(np.min(es), 3)}°")
plt.xlabel("θ /deg")
plt.ylabel("ε /deg")

plt.xlim(0, 90)
plt.ylim(0, 180)
plt.grid()

plt.show()