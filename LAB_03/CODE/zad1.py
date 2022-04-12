import mpmath
import numpy as np


def bisec(f, a, b, eps):
  if np.sign(f(a)) == np.sign(f(b)):
    print("WRONG PARAMS")
    return "ARG"
  global middle
  left, right = a, b
  i = 0
  while abs(left - right) > eps:
    # middle = (left + right) / 2
    middle = left + (right - left) / 2
    if abs(f(middle)) < eps:
      return middle, i
    if np.sign(f(left)) == np.sign(f(middle)):
      left = middle
    else:
      right = middle
    i += 1
  return middle, i


eps = 1e-10

f = lambda x: 2 * x - 2
print(bisec(f, 1 / 5, 10, eps))

f = lambda x: mpmath.cos(x) * mpmath.cosh(x) - 1
print(bisec(f, 3 / 2 * mpmath.pi, 2 * mpmath.pi, eps))

f = lambda x: 1 / x - mpmath.tan(x)
print(bisec(f, 0 + 0.000001, mpmath.pi / 2 - 0.000001, eps))

f = lambda x: 2 ** (-x) + np.e ** x + 2 * np.cos(x) - 6
print(bisec(f, 1, 3, eps))
