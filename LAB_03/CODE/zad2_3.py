import mpmath
import numpy as np


def rek(f, xi, eps, i):
  if i > 500:
    return "ARG"
  if abs(f(xi)) < eps:
    return xi, i
  h = 1e-10
  x = xi - h * f(xi) / (f(xi + h) - f(xi))
  return rek(f, x, eps, i + 1)


def newton(f, a, b, eps):
  if np.sign(f(a)) == np.sign(f(b)):
    print("WRONG PARAMS")
    return "ARG"
  return rek(f, b, eps, 0)


f = lambda x: 2 * x - 2
print(newton(f, 1 / 5, 10, 1e-10))

f = lambda x: mpmath.cos(x) * mpmath.cosh(x) - 1
print(newton(f, 3 / 2 * mpmath.pi, 2 * mpmath.pi, 1e-10))

f = lambda x: 1 / x - mpmath.tan(x)
print(newton(f, 0 + 0.000001, mpmath.pi / 2 - 0.000001, 1e-10))

f = lambda x: 2 ** (-x) + np.e ** x + 2 * np.cos(x) - 6
print(newton(f, 1, 3, 1e-10))
