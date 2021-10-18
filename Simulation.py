import sys
import math
import numpy as np
import matplotlib.pyplot as plt

granularity = 1


class Curve:
    def __init__(self, x, y, k, mkp):
        self.x = x
        self.y = y
        self.k = k
        self.mkp = mkp
        self.a = x-(y/mkp)
        self.w = k*mkp/y**2
        self.next = None

    def get_y(self, x):
        return self.k/self.w/(x-self.a)

    def print(self):
        print("w is: ", self.w, "a is: ", self.a)

    def plot(self, xf):
        x = np.linspace(self.x, xf, 1000)
        y = self.k/self.w/(x-self.a)
        plt.plot(x, y, 'g')
        plt.grid()


def exhaustive(curve, xf, storage, count, params):
    curve.plot(xf)
    print("plottte")
    print("The point after", count, "trades, is: ", curve.x, curve.y)
    storage.append(curve.y)
    count += 1
    if params["policy"] == "greedy":
        intercept = (math.sqrt(curve.mkp*curve.w * (curve.mkp*curve.w*xf**2-2*curve.mkp*curve.a * curve.w *
                                                    xf+3*curve.k+curve.mkp*curve.a**2*curve.w))+curve.mkp*curve.w * (xf+2*curve.a))/(3*curve.mkp*curve.w)
    elif params["policy"] == "arithmetic":
        intercept = curve.x+0.1
    elif params["policy"] == "geometric":
        intercept = curve.x+count**params["params"]
    elif params["policy"] == "exponential":
        intercept = curve.x+2**params["params"]
    if((intercept) >= xf):
        print("The point after", count, "trades, is: ", xf, curve.get_y(xf))
        curve.next = None
        plt.figure()
        print(len(storage))
        x = list(range(0, len(storage)))
        print(len(x))
        plt.plot(x, storage, 'g')
        return count, curve.get_y(xf)
    else:
        curve.next = Curve(intercept, curve.get_y(intercept), k, mkp)
        return exhaustive(curve.next, xf, storage, count, params)


def opt(curve, xf, n):
    storage = []
    if(n == 0):
        return curve.get_y(xf)
    else:
        intercept=curve.x+granularity
        if (intercept>=xf):
            return onetime_trade(curve,xf)
        while(intercept<xf):
            next_trade = Curve(intercept, curve.get_y(intercept), k, mkp)
            intercept+=granularity
            storage.append(opt(next_trade, xf, n-1))
        print(n, ":", storage.index(min(storage)))
        return min(storage)


def onetime_trade(curve, xf):
    optimal = curve.y-curve.mkp*(xf-curve.x)
    return optimal


if __name__ == "__main__":
    sys.setrecursionlimit(15000)
    x0 = 100
    y0 = 100
    xf = 110
    mkp = 5
    k = 10000
    params = [
        {"policy": "greedy", "params": None},
        {"policy": "arithmetic", "params": 0.1},
        {"policy": "geometric", "params": 0.0001},
        {"policy": "exponential", "params": 0.0001},
    ]
    head = Curve(x0, y0, k, mkp)
    #print(plt.figure(),exhaustive(head, xf, [], 0, params[1]))
    print("optimality: ", opt(head, xf, 10))
    onetime_trade(head, xf)
    plt.grid()
    plt.show()