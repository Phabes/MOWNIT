import mpmath
import numpy as np


def newton(f, dx, a, b, eps):
  if np.sign(f(a)) == np.sign(f(b)):
    print("WRONG PARAMS")
    return "ARG"
  n = 500
  x1 = b
  for i in range(n):
    # h = 1e-10
    # xi = x1 - h * f(x1) / (f(x1 + h) - f(x1))
    xi = x1 - f(x1) / dx(x1)
    fi = f(xi)
    if abs(fi) < eps or abs(xi - x1) < eps:
      return xi, i
    x1 = xi
  return "ARG"


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
