import mpmath
import numpy as np


def euler(f, a, b, eps):
  if np.sign(f(a)) == np.sign(f(b)):
    print("WRONG PARAMS")
    return "ARG"
  x1, x2 = a, b
  f1, f2 = f(x1), f(x2)
  n = 500
  for i in range(n):
    xi = x1 - f1 * (x1 - x2) / (f1 - f2)
    fi = f(xi)
    if abs(fi) < eps or abs(x1 - x2) < eps:
      return xi, i
    x2, f2 = x1, f1
    x1, f1 = xi, fi
  return "ARG"

eps = 1e-10

f = lambda x: 2 * x - 2
print(euler(f, 1 / 5, 10, eps))

f = lambda x: mpmath.cos(x) * mpmath.cosh(x) - 1
print(euler(f, 3 / 2 * mpmath.pi, 2 * mpmath.pi, eps))

f = lambda x: 1 / x - mpmath.tan(x)
print(euler(f, 0 + 0.000001, mpmath.pi / 2 - 0.000001, eps))

f = lambda x: 2 ** (-x) + mpmath.e ** x + 2 * mpmath.cos(x) - 6
print(euler(f, 1, 3, eps))
