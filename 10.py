# Create a mapping of pixel coordinates (that are fitted into a unit circle)
# to a sector of a circle with radius Rf, centered at the base of the object
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.patches import Arc
import numpy as np
import cv2
import os
import math

c = 299792458 #m/s
pi = np.pi

with cbook.get_sample_data(os.getcwd() + "/object.jpg") as image_file:
    image = plt.imread(image_file)

fig, ax = plt.subplots()
w = 1.7431510742 # To fit within unit circle
h = w*0.5625
gx = -(w/2)
gy = -(h/2)
w_p = 480
h_p = 270
R = 1
Rf = 3
arc_deg = 160
base = (0, gy)

def lens_project(x, y):
    global R, Rf, arc_deg, w, h, gx, gy
    theta = np.degrees(np.arctan2(y, x))  # Angle in degrees (-180, 180)

    # Map theta to the arc's angular bounds
    theta = ((((x-gx)/w)-0.5)*360) * (arc_deg/360) - 90

    # Scale radius based on vertical position (y)
    r_scaled = 1 + ((y-gy)/h) * Rf

    # Convert back to Cartesian coordinates
    theta_rad = np.radians(theta)
    X = np.cos(theta_rad) * r_scaled
    Y = np.sin(theta_rad) * r_scaled
    
    return X, Y

def show():
    global gx, gy, w, h, R, image, fig, ax
    ax.cla() # Clear the axes

    ax.imshow(image, extent=(gx, gx+w, gy, gy+h)) # Draw the original image

    H, W = image.shape[:2]  # Original image dimensions

    # Make coordinate grids for pixel positions in output
    j, i = np.meshgrid(np.arange(W), np.arange(H))  # j=cols (x), i=rows (y)

    # Convert pixel positions to world coords (xw, yw)
    xw = gx + (j / (W - 1)) * w
    yw = gy + (i / (H - 1)) * h

    # Apply lens projection to every coordinate
    Xp = np.zeros_like(xw, dtype=np.float32)
    Yp = np.zeros_like(yw, dtype=np.float32)
    for row in range(H):
        for col in range(W):
            Xp[row, col], Yp[row, col] = lens_project(xw[(H-1) - row, col], yw[(H-1) - row, col])
            # Offset from H and W necessary due to difference between OpenCV and matplotlib coordinates

    # Draws edges of projected image
    # ax.scatter(Xp[0], Yp[0])
    # ax.scatter(Xp[-1], Yp[-1])
    # ax.scatter(Xp[:,0], Yp[:,0])
    # ax.scatter(Xp[:,-1], Yp[:,-1])

    # Draws construction lines

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
    alpha = (np.any(warped != 0, axis=-1)).astype(np.float32) * 1.0 # The alpha channel
    warped = np.dstack((warped, alpha)) # Combine the alpha channel
    
    # Show projected image
    ax.imshow(warped, extent=(min_x+base[0], max_x-+base[0], min_y+base[1], max_y+base[1]), interpolation=None)
    
    # Draw the circle
    ax.add_patch(Arc((0, 0), 2, 2, angle=0.0, theta1=0.0, theta2=360.0))
    ax.scatter(np.array([base[0]]), np.array([base[1]]), marker="x", color='b')

    plt.xlim(-6, 6)
    plt.ylim(-7, 2)
    plt.grid()
    fig.canvas.draw()

def on_press(event): # For moving the image with the keyboard
    global gx, gy, w, h, R, image, fig, ax
    print('press', event.key)
    match event.key:
        case "left":
            gx -= 0.02
        case "right":
            gx += 0.02
        case "up":
            gy += 0.02
        case "down":
            gy -= 0.02
    show()

#fig.canvas.mpl_connect('key_press_event', on_press)
show()
plt.show()