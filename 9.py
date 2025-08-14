# Create an interactive model of the virtual image
# of an object in a convex spherical mirror
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.patches import Arc
import numpy as np
import cv2
import os
import math

c = 299792458 #m/s
pi = 3.14159265358979323846

with cbook.get_sample_data(os.getcwd() + "/object.jpg") as image_file:
    image = plt.imread(image_file)

fig, ax = plt.subplots()
x = 0.6
y = -0.3
w = 0.6
h = w*0.5625
R = 0.5
w_p = 480
h_p = 270

def lens_project(x, y, R):
    al = 0.5*math.atan(y/x)
    k = x/math.cos(2*al)
    Y = (k*math.sin(al))/((k/R)-math.cos(al)+((x/y)*math.sin(al)))
    X = x*(Y/y)
    return X, Y

def show():
    global x, y, w, h, R, image, fig, ax
    ax.cla() # Clear the axes

    ax.imshow(image, extent=(x, x+w, y, y+h)) # Draw the original image

    H, W = image.shape[:2]  # Original image dimensions

    # Make coordinate grids for pixel positions in output
    j, i = np.meshgrid(np.arange(W), np.arange(H))  # j=cols (x), i=rows (y)

    # Convert pixel positions to world coords (xw, yw)
    xw = x + (j / (W - 1)) * w
    yw = y + (i / (H - 1)) * h

    # Apply lens projection to every coordinate
    Xp = np.zeros_like(xw, dtype=np.float32)
    Yp = np.zeros_like(yw, dtype=np.float32)
    for row in range(H):
        for col in range(W):
            Xp[row, col], Yp[row, col] = lens_project(xw[(H-1) - row, col], yw[(H-1) - row, col], R)
            # Offset from H and W necessary due to difference between OpenCV and matplotlib coordinates

    # Draws edges of projected image
    # ax.scatter(Xp[0], Yp[0])
    # ax.scatter(Xp[-1], Yp[-1])
    # ax.scatter(Xp[:,0], Yp[:,0])
    # ax.scatter(Xp[:,-1], Yp[:,-1])

    # Draws construction lines
    ax.plot(np.array([0, x]), np.array([0, y+h]), color='r', ls='--')
    ax.plot(np.array([x, math.sqrt(R**2-(y+h)**2)]), np.array([y+h, y+h]), color='r', ls='--')
    ax.plot(np.array([0, 5*math.sqrt(R**2-(y+h)**2)]), np.array([0, 5*(y+h)]), color='b', ls='--')
    poly = np.poly1d(np.polyfit([lens_project(x, y+h, R)[0], math.sqrt(R**2-(y+h)**2)], [lens_project(x, y+h, R)[1], (y+h)], 1))
    x_axis = np.linspace(lens_project(x, y+h, R)[0], 10)
    ax.plot(x_axis, poly(x_axis), color='r', ls='--')

    # Calculate new world-coordinate bounding box from projection
    min_x, max_x = np.min(Xp), np.max(Xp)
    min_y, max_y = np.min(Yp), np.max(Yp)

    # Convert projected coords back to pixel coords
    dest_px = ((Xp - min_x) / (max_x - min_x) * (W - 1)).astype(int)
    dest_py = ((Yp - min_y) / (max_y - min_y) * (H - 1)).astype(int)

    # OpenCV -> matplotlib coordinates
    dest_py = (H - 1) - dest_py

    # Unfortunately cv2.remap() actually does the inverse operation
    # to what we want, so the mapping has to be reversed.

    rXp = np.full_like(Xp, -1, dtype=np.float32)
    rYp = np.full_like(Yp, -1, dtype=np.float32)
    
    # Fill remap arrays (inverse mapping)
    for row in range(H):
        for col in range(W):
            dy = dest_py[row, col]
            dx = dest_px[row, col]
            if 0 <= dy < H and 0 <= dx < W:
                rXp[dy, dx] = col  # source x index
                rYp[dy, dx] = row  # source y index

    # Remap using OpenCV
    warped = cv2.remap(image, rXp, rYp, interpolation=None, borderValue=[0, 0, 0])

    # Add transparency to background
    warped = warped.astype(np.float32) / 255.0 # To have a transparency channel the colours have to be in the range 0-1 rather than 0-255
    alpha = (np.any(warped != 0, axis=-1)).astype(np.float32) * 0.7 # The alpha channel
    warped = np.dstack((warped, alpha)) # Combine the alpha channel
    
    # Show projected image
    ax.imshow(warped, extent=(min_x, max_x, min_y, max_y), interpolation=None)
    
    # Draw the lens
    ax.add_patch(Arc((0, 0), 1, 1, angle=270.0, theta1=0.0, theta2=180.0))
    ax.scatter(np.array([0]), np.array([0]), marker="x", color='b')

    plt.xlim(-0.1, 1.6)
    plt.ylim(-0.6, 0.6)
    plt.grid()
    fig.canvas.draw()

def on_press(event): # For moving the image with the keyboard
    global x, y, w, h, R, image, fig, ax
    print('press', event.key)
    match event.key:
        case "left":
            x -= 0.02
        case "right":
            x += 0.02
        case "up":
            y += 0.02
        case "down":
            y -= 0.02
    show()

fig.canvas.mpl_connect('key_press_event', on_press)
show()
plt.show()