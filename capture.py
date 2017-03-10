import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import cv2
import math
import time

style.use('fivethirtyeight')
mpl.rcParams['lines.linewidth'] = 2

fig = plt.figure("Intensity")
ax1 = fig.add_subplot(1, 1, 1)

# Open video feed and get initial frame
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Get width and height of camera
height, width = frame.shape[:2]

# Select center y value
y = int(math.floor(height / 2))


def animate(i):
    global width
    global ret, frame, gray

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display raw intensity value on the graph
    xs = np.arange(0, width, 1)
    ys = np.zeros(width)
    for i in range(0, width - 2):
        ys[i] = float(gray[y][i]) / 255.0
        gray[y][i] = 255
    s_w = 15
    ys = smooth(ys, s_w)
    ys = smooth(ys, s_w)
    ys = smooth(ys, s_w)
    ys = smooth(ys, s_w)

    peaks = get_d_peaks(ys, [1])

    ax1.clear()
    ax1.plot(xs, ys, '-o', markevery=peaks)

    ax1.set_ylim([0, 1])
    ax1.set_autoscale_on(False)

    # Show camera image
    cv2.imshow('Intensity', gray)


def sign(i):
    if i > 0:
        return 1
    elif i < 0:
        return -1
    else:
        return 0


def smooth(arr, width):
    a_w = arr.size
    h_width = int(math.floor(width / 2))
    for i in range(0, a_w - 1):
        avg = 0
        r_min = max(0, i - h_width)
        r_max = min(i + h_width, a_w - 1)
        for j in range(r_min, r_max):
            avg = avg + arr[j]
        avg = avg / (r_max - r_min)
        arr[i] = avg
    return arr


def get_d_peaks(arr, order, max_local=True):
    o_arr = []
    if isinstance(order, list):
        for i in range(0, len(order)):
            o_arr = o_arr + get_d_peaks(arr, order[i], max_local)
    else:
        a_w = arr.size
        slope = 0.0
        p_slope = derivative(arr, order, 0)
        for i in range(1, a_w - order - 1):
            slope = derivative(arr, order, i)
            if slope == 0:
                o_arr.append(i)
            elif max_local:
                if sign(p_slope) > 0 > sign(slope):
                    o_arr.append(i)
            else:
                if sign(p_slope) < 0 < sign(slope):
                    o_arr.append(i)
            p_slope = slope
    print(arr[width - 1])
    return o_arr


def derivative(arr, order, pos):
    if order == 0:
        return arr[pos]
    n_arr = []
    for i in range(pos, pos + order):
        n_arr.append(arr[i + 1] - arr[i])
    return derivative(n_arr, order - 1, 0)

ani = animation.FuncAnimation(fig, animate, interval=30)
plt.show()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
