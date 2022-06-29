import numpy as np
from scipy.integrate import dblquad
import matplotlib.pyplot as plt
from math import log, e

f1 = lambda x: e ** (-x ** 2) * log(x) ** 2
f2 = lambda x: 1 / (x ** 3 - 2 * x - 5)
f3 = lambda x: x ** 5 * e ** (-x) * np.sin(x)
f4 = lambda x, y: 1 / ((x + y) ** (1 / 2) * (1 + x + y))
f5 = lambda x, y: x**2 + y**2


def dbl(f, low, high, gfun, hfun):
    return dblquad(f, low, high, gfun, hfun)


# print(dbl(f4, 0, 1, lambda x: 0, lambda x: 1 - x))
# print(dbl(f5, -3, 3, lambda x: -5, lambda x: 5))
