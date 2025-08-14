# Recreate graph of φ
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

fqs = np.linspace(405, 790, 500)

php = np.array([])
for i in range(len(fqs)):
    thp = np.arcsin(np.sqrt((4-(watern(fqs[i])**2))/3)) # radians
    php = np.append(php, np.degrees(np.arcsin(np.sin(thp)/watern(fqs[i]))))

phs = np.array([])
for i in range(len(fqs)):
    ths = np.arcsin(np.sqrt((9-(watern(fqs[i])**2))/8)) # radians
    phs = np.append(phs, np.degrees(np.arcsin(np.sin(ths)/watern(fqs[i]))))

cr = np.array([])
for i in range(len(fqs)):
    cr = np.append(cr, np.degrees(np.arcsin(1/watern(fqs[i]))))

for i in range(len(php)):
    plt.scatter(fqs[i], php[i], color=colour(fqs[i]), linewidth=2.0)
    plt.scatter(fqs[i], phs[i], color=colour(fqs[i]), linewidth=2.0)
plt.plot(fqs, cr, color='black', label="Critical angle")
plt.plot(fqs, php, color='red', label="Primary")
plt.plot(fqs, phs, color='blue', label="Secondary")
plt.legend(loc="upper left")

plt.title("Refraction angle of single and double rainbows")
plt.xlabel("Frequency /THz")
plt.ylabel("φ /deg")

plt.xlim(405, 790)
plt.ylim(39, 49)
plt.grid()

plt.show()