import sys
import math
import numpy as np
import matplotlib.pyplot as plt


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


def dynamic(curve, xf, storage, count, params):
    curve.plot(xf)
    print("The point after", count, "trades, is: ", curve.x, curve.y)
    storage.append(curve.y)
    count += 1
    if params["policy"] == "greedy":
        intercept = (math.sqrt(curve.mkp*curve.w * (curve.mkp*curve.w*xf**2-2*curve.mkp*curve.a * curve.w *
                                                    xf+3*curve.k+curve.mkp*curve.a**2*curve.w))+curve.mkp*curve.w * (xf+2*curve.a))/(3*curve.mkp*curve.w)
    elif params["policy"] == "arithmetic":
        intercept = curve.x+count*params["params"]
    elif params["policy"] == "geometric":
        intercept = curve.x+count**params["params"]
    elif params["policy"] == "exponential":
        intercept = curve.x+2**params["params"]
    if((intercept) >= xf):
        print("The point after", count, "trades, is: ", xf, curve.get_y(xf))
        curve.next=None
        return count, curve.get_y(xf)
    else:
        curve.next = Curve(intercept, curve.get_y(intercept), k, mkp)
        return dynamic(curve.next, xf, storage, count, params)

def onetime_trade(curve, xf):
    optimal = curve.y-curve.mkp*(xf-curve.x)
    print("The optimal point: ", xf, optimal)

if __name__ == "__main__":
    sys.setrecursionlimit(15000)
    x0 = 100
    y0 = 100
    xf = 110
    mkp = 5
    k = 10000
    head = Curve(x0, y0, k, mkp)

    plt.figure()
    params = [
        {"policy": "greedy", "params": None},
        {"policy": "arithmetic", "params": 1},
        {"policy": "geometric", "params": 0.0001},
        {"policy": "exponential", "params": 0.0001},
    ]
    print(dynamic(head, xf, [], 0, params[1]))
    temp=head
    while temp.next!=None:
        temp.print()
        temp=temp.next
    onetime_trade(head, xf)
    plt.grid()
    plt.show()
