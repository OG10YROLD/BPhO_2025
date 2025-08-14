# Create a dynamic model of the path of a beam of white light through a triangular prism
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

plt.style.use('dark_background')
fig, ax = plt.subplots()

fqs = np.linspace(405, 790, 15) # frequencies
alpha = 45
th_i = 20
l_angle = np.radians(90-(alpha/2))*1 # bottom left angle of the triangle in radians

ax.plot([-1, 0], [-1, -1 + np.tan(l_angle)], color='white', linewidth=1.0)  # left edge
ax.plot([1, 0], [-1, -1 + np.tan(l_angle)], color='white', linewidth=1.0)  # right edge
ax.plot([-1, 1], [-1, -1], color='white', linewidth=1.0)  # base

# --- LEFT SIDE NORMAL ---

# Midpoint of left edge
x_mid = (-1 + 0) / 2
y_mid = (-1 + (-1 + np.tan(l_angle))) / 2

# Slope of left side
left_m = np.tan(l_angle)

# Slope of normal
left_norm_m = -1 / left_m

# Normal length (just for drawing)
norm_len = 0.5
dx = norm_len / np.sqrt(1 + left_norm_m**2)
dy = left_norm_m * dx

# Draw the normal
ax.plot([x_mid - dx, x_mid + dx], [y_mid - dy, y_mid + dy], 'w--')

th_i = np.radians(th_i)
alpha = np.radians(alpha)
th_2 = np.array([])
th_r = np.array([])
for i in range(len(fqs)):
    th_2 = np.append(th_2, np.arcsin(np.sin(th_i)/sellmeier(fqs[i], a, b)))
    th_r = np.append(th_r, np.arcsin(math.sqrt(sellmeier(fqs[i], a, b)**2 - np.sin(th_i)**2)*np.sin(alpha) - np.sin(th_i)*np.cos(alpha)))

white_m = left_norm_m + np.tan(th_i)
white_len = 5
dx = white_len / np.sqrt(1 + white_m**2)
dy = white_m * dx
ax.plot([x_mid - dx, x_mid], [y_mid - dy, y_mid], 'w-', lw=2.0)
for i in range(len(fqs)):
    # Ray slope
    m_ray = (left_norm_m + np.tan(th_2[i])) / (1 - left_norm_m * np.tan(th_2[i]))

    # Right side endpoints
    p1 = np.array([0, -1 + np.tan(l_angle)])
    p2 = np.array([1, -1])
    m_side = (p2[1] - p1[1]) / (p2[0] - p1[0])

    # Intersection
    x_end = (p1[1] - y_mid + m_ray*x_mid - m_side*p1[0]) / (m_ray - m_side)
    y_end = m_ray*(x_end - x_mid) + y_mid

    ax.plot([x_mid, x_end], [y_mid, y_end], color=colour(fqs[i])) # Draw the interior ray

    # Gradient of normal (negative reciprocal)
    m_norm_right = -1 / m_side

    # Length of normal vector to plot
    length_norm = 0.5  # adjust for visibility

    # Calculate dx, dy for the normal line
    dx_norm = length_norm / np.sqrt(1 + m_norm_right**2)
    dy_norm = m_norm_right * dx_norm

    # Normal endpoints
    x_norm_start = x_end - dx_norm
    y_norm_start = y_end - dy_norm
    x_norm_end   = x_end + dx_norm
    y_norm_end   = y_end + dy_norm

    # Plot normal at intersection
    ax.plot([x_norm_start, x_norm_end], [y_norm_start, y_norm_end], 'w--')

    # Slope of leaving ray
    m_ray_exit = (m_norm_right - np.tan(th_r[i])) / (1 + m_norm_right * np.tan(th_r[i]))

    # Length to draw the leaving ray
    length_exit = 3.0

    # Compute end coordinates
    x_exit = x_end + length_exit / np.sqrt(1 + m_ray_exit**2)
    y_exit = y_end + m_ray_exit * (x_exit - x_end)

    # Plot leaving ray
    ax.plot([x_end, x_exit], [y_end, y_exit], color=colour(fqs[i]), lw=3.0)

plt.title(f"White light through a triangular prism, θi = {np.degrees(th_i)}, α = {np.degrees(alpha)}")

plt.xlim(-2, 2)
plt.ylim(-2, 2)
#plt.grid()

plt.show()