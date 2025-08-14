# Write a computer program that imports an image file (the ‘object’) and then computes 
# the locations of the pixel coordinates that constitute a virtual image in a plane mirror.
# Use this information to plot the virtual image.
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np
import os
import math

c = 299792458 #m/s

with cbook.get_sample_data(os.getcwd() + "/object.jpg") as image_file:
    image = plt.imread(image_file)

fig, ax = plt.subplots()
x = 0.5
y = 2
w = 1
h = 0.5625
ax.imshow(image, extent=(x, x+w, y, y+h))

ax.imshow(image, extent=(-x, -x-w, y, y+h))

def on_press(event):
    global x, y, w, h, image, fig, ax
    print('press', event.key)
    match event.key:
        case "left":
            x -= 0.1
        case "right":
            x += 0.1
        case "up":
            y += 0.1
        case "down":
            y -= 0.1
    print(x, y)
    plt.cla()
    plt.plot(np.array([0, 0]), np.array([-10, 10]))
    plt.xlim(-2.5, 2.5)
    plt.ylim(0, 5)
    plt.grid()
    ax.imshow(image, extent=(x, x+w, y, y+h))
    ax.imshow(image, extent=(-x, -x-w, y, y+h))
    plt.show()

fig.canvas.mpl_connect('key_press_event', on_press)

plt.plot(np.array([0, 0]), np.array([-10, 10]))
plt.xlim(-2.5, 2.5)
plt.ylim(0, 5)
plt.grid()
plt.show()