# Create a model of primary and secondary rainbows that you would see at sea level
# (with no topographic obstructions) for different angles of (anti) solar elevation.
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np
import math

c = 299792458 # m/s

def watern(fthz): # frequency in THz
    return math.sqrt(math.sqrt(1/(1.731-(0.261*((fthz/(10**3))**2))))+1)

def colour(fthz):
    if (fthz >= 405) and (fthz < 480):
        col = [1, (fthz-405)/150, 0]
    elif (fthz >= 480) and (fthz < 510):
        col = [1, 0.5+((fthz-480)/60), 0]
    elif (fthz >= 510) and (fthz < 530):
        col = [1-((fthz-510)/20), 1, 0]
    elif (fthz >= 530) and (fthz < 600):
        col = [0, 1, ((fthz-530)/140)]
    elif (fthz >= 600) and (fthz < 620):
        col = [0, 1-((fthz-600)/80), 0.5+((fthz-600)/40)]
    elif (fthz >= 620) and (fthz < 680):
        col = [0, 0.75-((fthz-620)/80), 1]
    elif (fthz >= 680) and (fthz <= 790):
        col = [((fthz-680)/220), 0, 1]
    return col

# Sun elevation
sun_el = 20.0

fig, ax = plt.subplots(figsize=(8, 8))

def show():
    ax.cla()

    # Frequencies for colours
    fqs = np.linspace(405, 790, 50)

    plt.title(f"Rainbow simulation - Solar angle α = {sun_el}°")
    plt.xlabel("Azimuth relative to antisolar point (°)")
    plt.ylabel("Altitude (°)")
    plt.grid(True)
    ax.set_aspect('equal')
    ax.set_xlim(-90, 90)
    ax.set_ylim(0, 90)
    ax.axhline(0, color='k', lw=1)  # horizon

    for f in fqs:
        # Primary radius
        thp = np.arcsin(np.sqrt((4-(watern(f)**2))/3))
        ep = 4*np.degrees(np.arcsin(np.sin(thp)/watern(f))) - 2*np.degrees(thp)
        
        # Secondary radius
        ths = np.arcsin(np.sqrt((9-(watern(f)**2))/8))
        es = np.degrees(np.pi - 6*np.arcsin(np.sin(ths)/watern(f)) + 2*ths)
        
        # Primary arc
        arc_primary = Arc(
            (0, -sun_el),   # center (shift down by Sun elevation)
            width=2*ep, height=2*ep,
            theta1=0, theta2=180,
            color=colour(f), lw=2
        )
        ax.add_patch(arc_primary)

        # Secondary arc
        arc_secondary = Arc(
            (0, -sun_el), 
            width=2*es, height=2*es,
            theta1=0, theta2=180,
            color=colour(f), lw=2, alpha=0.6
        )
        ax.add_patch(arc_secondary)
    
    fig.canvas.draw()

def on_press(event): # For changing the sun elevation with the keyboard
    global fig, ax, sun_el
    print('press', event.key)
    match event.key:
        case "up":
            sun_el += 1
        case "down":
            if (sun_el - 1) >= 0:
                sun_el -= 1
    show()

fig.canvas.mpl_connect('key_press_event', on_press)
show()
plt.show()