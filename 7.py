# Create an interactive model of the virtual, enlarged image
# of an object placed inside the focal range of an ideal thin lens.
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np
import cv2
import os
import math

c = 299792458 #m/s
pi = 3.14159265358979323846

with cbook.get_sample_data(os.getcwd() + "/object.jpg") as image_file:
    image = plt.imread(image_file)

fig, ax = plt.subplots()
x = 0.5
y = 0.3
w = 0.5
h = w*0.5625
f = 1.5
w_p = 480
h_p = 270

def lens_project(x, y, f):
    X = -(f / (x - f)) * x
    Y = (y / x) * X
    return X, Y

def show():
    global x, y, w, h, f, w_p, h_p, image, fig, ax
    ax.cla() # Clear the axes

    # The corner coordinates of the image itself
    src_pts = np.float32([
        [0, 0], # top left
        [w_p-1, 0], # top right
        [w_p-1, h_p-1], # bottom right
        [0, h_p-1] # bottom left
    ])

    # The coordinates of the corners of the projected image, derived with the equations, in world coordinates
    dst_pts = np.float32([
        lens_project(x, y+h, f), # top-left
        lens_project(x+w, y+h, f), # top-right
        lens_project(x+w, y, f), # bottom-right
        lens_project(x, y, f) # bottom-left
    ])

    ax.imshow(image, extent=(x, x+w, y, y+h)) # Draw the original image

    # The image cannot be simply drawn to world coordinates and only within a bounded rectangle.
    # Thus, the coordinates must be converted.

    # This calculates the edges of this bounding box in world coordinates.
    min_x, min_y = np.min(dst_pts, axis=0)
    max_x, max_y = np.max(dst_pts, axis=0)

    # The world coordinates in dst_pts have to be offset and scaled so that they fit within the bounding box.
    # I have arbitrarily chosen the bounding box to be w_p units wide and h_p units tall.
    # Thus [min_x, min_y] in world coordinates will become [0,0], and [max_x, max_y] will become [w_p, h_p].

    scale = np.array([w_p / (max_x - min_x), h_p / (max_y - min_y)], dtype=np.float32)
    offset = np.array([min_x, min_y], dtype=np.float32)
    dst_pts_wrp = (dst_pts - offset) * scale

    tform = cv2.getPerspectiveTransform(src_pts, dst_pts_wrp)

    # The third argument is the bounding box size I mentioned earlier.
    # The last argument is the background colour of the bounding box, which is white to blend in.
    warped = cv2.warpPerspective(image, tform, (w_p, h_p), borderMode=cv2.BORDER_CONSTANT)
    warped = np.flipud(warped) # The OpenCV coordinate system is opposite from matplotlib, so it needs to be flipped
    warped = warped.astype(np.float32) / 255.0 # To have a transparency channel the colours have to be in the range 0-1 rather than 0-255
    alpha = (np.any(warped != 0, axis=-1)).astype(np.float32) * 0.7 # The alpha channel
    warped = np.dstack((warped, alpha)) # Combine the alpha channel
    ax.imshow(warped, extent=(min_x, max_x, min_y, max_y), interpolation=None) # Draw the projected image

    #ax.scatter(np.array([i[0] for i in dst_pts]), np.array([i[1] for i in dst_pts])) # Shows the coordinates of the projected image
    
    # Draw the lens
    plt.plot(np.array([-0.05, 0.05]), np.array([1, 1]), color='b')
    plt.plot(np.array([-0.05, 0.05]), np.array([-1, -1]), color='b')
    plt.plot(-0.05 + -0.1 * np.sin(np.linspace(0, pi, 100)), np.linspace(1, -1, 100), color='b')
    plt.plot(0.05 + 0.1 * np.sin(np.linspace(0, pi, 100)), np.linspace(1, -1, 100), color='b')
    ax.scatter(np.array([-f, f]), np.array([0, 0]), marker="x", color='b')

    plt.xlim(-4, 4)
    plt.ylim(-3, 3)
    plt.grid()
    fig.canvas.draw()

def on_press(event): # For moving the image with the keyboard
    global x, y, w, h, f, image, fig, ax
    print('press', event.key)
    match event.key:
        case "left":
            if (x - 0.05) > 0: # Limit to within focal range
                x -= 0.05
        case "right":
            if (x + 0.05) < f: # Limit to within focal range
                x += 0.05
        case "up":
            y += 0.05
        case "down":
            y -= 0.05
    show()

fig.canvas.mpl_connect('key_press_event', on_press)
show()
plt.show()