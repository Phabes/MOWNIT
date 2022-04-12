import mpmath
import numpy as np


def rek(f, dx, xi, eps, i):
  if i > 500:
    return "ARG"
  # h = 1e-10
  # x = xi - h * f(xi) / (f(xi + h) - f(xi))
  x = xi - f(xi) / dx(xi)
  if abs(f(xi)) < eps or abs(x - xi) < eps:
    return xi, i
  return rek(f, dx, x, eps, i + 1)


def newton(f, dx, a, b, eps):
  if np.sign(f(a)) == np.sign(f(b)):
    print("WRONG PARAMS")
    return "ARG"
  return rek(f, dx, b, eps, 0)


eps = 1e-10

f = lambda x: 2 * x - 2
dx = lambda x: 2
print(newton(f, dx, 1 / 5, 10, eps))

f = lambda x: mpmath.cos(x) * mpmath.cosh(x) - 1
dx = lambda x: mpmath.cos(x) * mpmath.sinh(x) - mpmath.sin(x) * mpmath.cosh(x)
print(newton(f, dx, 3 / 2 * mpmath.pi, 2 * mpmath.pi, eps))

f = lambda x: 1 / x - mpmath.tan(x)
dx = lambda x: -1 / x ** 2 - mpmath.sec(x) ** 2
print(newton(f, dx, 0 + 0.000001, mpmath.pi / 2 - 0.000001, eps))

f = lambda x: 2 ** (-x) + mpmath.e ** x + 2 * mpmath.cos(x) - 6
dx = lambda x: mpmath.e ** x - 2 ** (-x) * mpmath.log(2) - 2 * mpmath.sin(x)
print(newton(f, dx, 1, 3, eps))
