import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import cv2
import math


ax1 = None
cap = None
height = 0
width = 0
callback = None
peak_orders = []
g_y = 0
g_windows = True


def mouse_callback(event, ex, ey, flags, param):
    global g_y
    if event == cv2.EVENT_LBUTTONUP:
        g_y = ey


def animate(i):
    global width

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display raw intensity value on the graph
    xs = np.arange(0, width, 1)
    ys = np.zeros(width)
    for i in range(0, width):
        ys[i] = float(gray[g_y][i]) / 255.0
        gray[g_y][i] = 255
    s_w = 25
    for i in range(1, 3):
        ys = smooth(ys, int(s_w / i))
    ys = smooth(ys, 8)

    peaks = get_d_peaks(ys, peak_orders)
    if callback is not None:
        out_arr = []
        for p in peaks:
            out_arr.append((p, ys[p]))
        callback(out_arr)

    if g_windows:
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
    if width <= 1:
        return arr
    a_w = arr.size
    h_width = int(math.floor(width / 2))
    for i in range(0, a_w):
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
            o_arr += get_d_peaks(arr, order[i], max_local)
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
    return o_arr


def derivative(arr, order, pos):
    if order == 0:
        return arr[pos]
    n_arr = []
    for i in range(pos, pos + order + 1):
        n_arr.append(arr[i + 1] - arr[i])
    return derivative(n_arr, order - 1, 0)


def retrieve_peaks(peak_callback, defined_peak_orders, y=-1, interval=50, windows=True):
    global ax1, cap, height, width, callback, peak_orders, g_y, g_windows

    callback = peak_callback
    peak_orders = defined_peak_orders
    g_windows = windows

    if windows:
        # Set up matplotlib for windows
        style.use('fivethirtyeight')
        mpl.rcParams['lines.linewidth'] = 2

        fig = plt.figure("Intensity")
        ax1 = fig.add_subplot(1, 1, 1)

    # Open video feed and set mouse callback
    cap = cv2.VideoCapture(0)
    if windows:
        cv2.namedWindow("Intensity")
        cv2.setMouseCallback("Intensity", mouse_callback)

    # Get width and height of camera
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    if y > -1:
        # Use user defined y value
        g_y = y
    else:
        # Select center y value
        g_y = int(math.floor(height / 2))

    if windows:
        ani = animation.FuncAnimation(fig, animate, interval=interval)
        plt.show()

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
    else:
        while True:
            animate(0)


if __name__ == "__main__":
    retrieve_peaks(None, [1, 2])
