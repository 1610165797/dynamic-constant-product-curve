import numpy as np
import math
import matplotlib.pyplot as plt


class Curve:
    def __init__(self, x, y, k, mkp, count):
        self.x = x
        self.y = y
        self.k = k
        self.mkp = mkp
        self.a = x-(y/mkp)
        self.w = k*mkp/y**2
        self.next = None
        self.count = count

    def get_y(self, x):
        return self.k/self.w/(x-self.a)

    def plot(self, xf):
        x = np.linspace(self.x, xf, 1000)
        y = self.k/self.w/(x-self.a)
        plt.plot(x, y, 'g')
        plt.grid()


def dynamic(curve, xf, sensitivity, storage):
    curve.plot(xf)
    if((xf-curve.x) < sensitivity):
        x = range(0, curve.count)
        plt.figure()
        plt.plot(x, storage)
        return
    else:
        storage.append(curve.y)
        print("Point on", curve.count, "th trade is: ", curve.x, curve.y)
        intercept = (math.sqrt(curve.mkp*curve.w * (curve.mkp*curve.w*xf**2-2*curve.mkp*curve.a * curve.w *
                     xf+3*curve.k+curve.mkp*curve.a**2*curve.w))+curve.mkp*curve.w * (xf+2*curve.a))/(3*curve.mkp*curve.w)
        curve.next = Curve(intercept, curve.get_y(
            intercept), k, mkp, curve.count+1)
        dynamic(curve.next, xf, sensitivity, storage)


def onetime_trade(curve, xf):
    optimal = curve.y-curve.mkp*(xf-curve.x)
    print("The optimal point: ", xf, optimal)


if __name__ == "__main__":
    x0 = 1000
    y0 = 1000
    xf = 1100
    mkp = 5
    k = 1000000
    sensitivity = 0.01
    head = Curve(x0, y0, k, mkp, 0)
    plt.figure()
    dynamic(head, xf, sensitivity, [])
    onetime_trade(head, xf)
    plt.grid()
    plt.show()
