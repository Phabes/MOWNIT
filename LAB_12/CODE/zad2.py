import numpy as np
import matplotlib.pyplot as plt
from math import log, e

f1 = lambda x: e ** (-x ** 2) * log(x) ** 2
f2 = lambda x: 1 / (x ** 3 - 2 * x - 5)
f3 = lambda x: x ** 5 * e ** (-x) * np.sin(x)


def parable(y1, y2, y3, h):
    return (y1 + 4 * y2 + y3) * h / 3


def simpson(x, y):
    h = x[1] - x[0]
    fields = [0 for _ in range(len(x))]
    for i in range(2, len(x), 2):
        fields[i] = parable(y[i - 2], y[i - 1], y[i], h)
    print(fields)
    field = sum(fields)
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()
    return field


x = np.linspace(-1, 8, 90)
print(simpson(x, f2(x)))
x = np.linspace(-1, 8, 90)
print(simpson(x, f3(x)))
