import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve, diff, nsolve, Heaviside, Min, Abs

granularity = 0.01
sys.setrecursionlimit(15000)


class Curve:
    def __init__(self, x, y, k, mkp):
        self.x = x
        self.y = y
        self.k = k
        self.mkp = mkp
        self.a = x-(y/mkp)
        self.w = k*mkp/y**2
        self.next = []

    def get_y(self, x):
        return self.k/self.w/(x-self.a)

    def print(self):
        print("w is: ", self.w, "a is: ", self.a)

    def plot(self, xf, color):
        x = np.linspace(self.x, xf, 1000)
        y = self.k/self.w/(x-self.a)
        plt.plot(x, y, color)
        plt.grid()

    def onetime_trade(self, xf):
        return (self.y-self.mkp*(xf-self.x))


def exhaustive(curve, xf, storage, count, params):
    curve.plot(xf, "g")
    print("The point after", count, "trades, is: ", curve.x, curve.y)
    storage.append(curve.y)
    count += 1
    if params["policy"] == "greedy":
        intercept = (math.sqrt(xf**2-2*curve.a*xf+3*curve.k /
                     curve.mkp/curve.w+curve.a**2)+xf+2*curve.a)/3
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
        curve.next.append(Curve(intercept, curve.get_y(intercept), k, mkp))
        return exhaustive(curve.next[0], xf, storage, count, params)


def optimal(curve, xf, n):
    storage = []
    if(n == 1):
        curve.next = None
        return curve.get_y(xf)
    else:
        intercept = curve.x+granularity
        if (intercept >= xf):
            return curve.onetime_trade(xf)
        else:
            while (intercept < xf):
                next_trade = Curve(intercept, curve.get_y(intercept), k, mkp)
                curve.next.append(next_trade)
                intercept += granularity
                storage.append(optimal(next_trade, xf, n-1))
        index = storage.index(min(storage))
        curve.next = curve.next[index]
        return min(storage)


def plot_optimal(curve, xf, n):
    plt.figure()
    plt.title('Trade History')
    temp = curve
    storage = []
    while(temp != None):
        temp.plot(xf, "y")
        print(temp.x)
        storage.append(temp.x)
        temp = temp.next
    plt.figure()
    x = list(range(0, n))
    plt.plot(x, storage, 'y')
    plt.title('x VS n')


def set_LaGrange_vector(n):
    storage = []
    for i in range(n):
        storage.append("n"+str(i+1))
    return storage


def formulate_equation(curve, xf, n, list, storage):
    u = symbols(list[len(list)-n])
    storage.append(u)
    if(n == 1):
        return curve.get_y(u), storage
    else:
        next = Curve(u, curve.get_y(u), curve.k, curve.mkp)
        return formulate_equation(next, xf, n-1, list, storage)


def LaGrange(curve, xf, n):
    result = formulate_equation(curve, xf, n, set_LaGrange_vector(n), [])
    exp = result[1][-1]-xf
    lbd = symbols("lbd")
    exp = result[0]-lbd*exp
    equations = []
    result[1].insert(0, lbd)
    for i in result[1]:
        print(diff(exp, i))
        equations.append(diff(exp, i))
    if n == 1:
        return [0, xf]
    else:
        guess = list(LaGrange(curve, xf, n-1))
        guess.insert(1, curve.x)
        return nsolve(equations, result[1], guess)


def OPT(curve, xf, n):
    set = {}
    count = 1
    while(len(set.keys()) < n):
        u = curve.x+granularity
        if count == 1:
            temp = {}
            while(u <= xf):
                temp[u] = curve.y-curve.get_y(u)
                u += granularity
            set[count] = temp
        else:
            temp = {}
            while(u <= xf):
                storage = []
                for i in set[count-1]:
                    prev = Curve(
                        i, curve.y-set[count - 1][i], curve.k, curve.mkp)
                    storage.append(curve.y-prev.get_y(u))
                temp[u] = max(storage)
                u += granularity
            set[count] = temp
        count += 1
    key = max(set[n], key=set[n].get)
    return curve.y-set[n][key]


if __name__ == "__main__":
    x0 = 100
    y0 = 100
    xf = 110
    mkp = 5
    k = 10000
    trade_limit = 10
    params = [
        {"policy": "greedy", "params": None},
        {"policy": "arithmetic", "params": 0.1},
        {"policy": "geometric", "params": 0.0001},
        {"policy": "exponential", "params": 0.0001},
    ]
    curve = Curve(x0, y0, k, mkp)
    print("Optimal yf is:", OPT(curve, xf, trade_limit))

    print("optimality: ", optimal(curve, xf, trade_limit))
    plot_optimal(curve, xf, trade_limit)
    print(LaGrange(curve, xf, trade_limit))
    print(plt.figure(), exhaustive(curve, xf, [], 0, params[0]))
    curve.onetime_trade(xf)
    plt.grid()
    plt.show()
