import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import cv2
import math


class Capture():
    def __init__(self, callback, peak_orders, y, interval, windows):
        self.ax1 = None
        self.fig = None
        self.cap = None
        self.height = 0
        self.width = 0
        self.callback = callback
        self.peak_orders = peak_orders
        self.g_y = 0
        self.g_windows = windows
        self.interval = interval

        if windows:
            # Set up matplotlib for windows
            style.use('fivethirtyeight')
            mpl.rcParams['lines.linewidth'] = 2

            self.fig = plt.figure("Intensity")
            self.ax1 = self.fig.add_subplot(1, 1, 1)

        # Open video feed and set mouse callback
        self.cap = cv2.VideoCapture(0)
        if windows:
            cv2.namedWindow("Intensity")
            cv2.setMouseCallback("Intensity", self.mouse_callback)

        # Get width and height of camera
        ret, frame = self.cap.read()
        self.height, self.width = frame.shape[:2]

        if y > -1:
            # Use user defined y value
            self.g_y = y
        else:
            # Select center y value
            self.g_y = int(math.floor(self.height / 2))

    def run(self):
        if self.g_windows:
            ani = animation.FuncAnimation(self.fig, self.animate, interval=self.interval)
            plt.show()

            # When everything done, release the capture
            self.cap.release()
            cv2.destroyAllWindows()
        else:
            while True:
                self.animate(0)

    def mouse_callback(self, event, ex, ey, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.g_y = ey

    def animate(self, i):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display raw intensity value on the graph
        xs = np.arange(0, self.width, 1)
        ys = np.zeros(self.width)
        raw_ys = np.zeros(self.width)
        for i in range(0, self.width):
            ys[i] = float(gray[self.g_y][i]) / 255.0
            raw_ys[i] = float(gray[self.g_y][i]) / 255.0
            frame[self.g_y][i] = 255
        s_w = 25
        for i in range(1, 3):
            ys = smooth(ys, int(s_w / i))
        ys = smooth(ys, 8)

        peaks = get_d_peaks(ys, self.peak_orders)
        if self.callback is not None:
            out_arr = []
            for p in peaks:
                out_arr.append((p, ys[p]))
            self.callback(out_arr, self.width)

        if self.g_windows:
            self.ax1.clear()
            self.ax1.plot(xs, raw_ys)
            self.ax1.plot(xs, ys, '-o', markevery=peaks)

            self.ax1.set_ylim([0, 1])
            self.ax1.set_autoscale_on(False)

            # Show camera image
            cv2.imshow('Intensity', frame)


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
    cap = Capture(peak_callback, defined_peak_orders, y, interval, windows)
    cap.run();


if __name__ == "__main__":
    retrieve_peaks(None, [1])
