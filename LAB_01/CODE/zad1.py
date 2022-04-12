import random
from datetime import datetime
from matplotlib import pyplot
import numpy

n = 10 ** 7
x = numpy.single(0.369373)
# x = random.uniform(0.1, 0.9)
# x = numpy.single(x)
T = [x for _ in range(n)]


def zad1():
  relativeErrors = []
  X = []

  def sumIter(T):
    suma = numpy.single(0)
    for i in range(n):
      suma += T[i]
      if ((i + 1) % 25000 == 0):
        X.append(i)
        realVal = i * x
        relativeError = abs(realVal - suma) / realVal * 100
        relativeErrors.append(relativeError)
    return suma

  def sumReq(T, start, end):
    middle = (end + start) // 2
    if (start < end):
      return sumReq(T, start, middle) + sumReq(T, middle + 1, end)
    return T[start]

  real = 10 ** 7 * x
  start_time = datetime.now()
  sumaIter = sumIter(T)
  end_time = datetime.now()
  err1 = abs(real - sumaIter)
  err2 = err1 / real
  print("X:", x)
  print("DOKLADNA SUMA:", real)
  print("ITERACYJNIE:")
  print("SUMA:", sumaIter, "BEZWZGLEDNY:", err1, "WZGLEDNY:", err2)
  print('CZAS: {}'.format(end_time - start_time))
  print("%:", err2 * 100)
  start_time = datetime.now()
  sumaReq = sumReq(T, 0, n - 1)
  end_time = datetime.now()
  err1 = abs(real - sumaReq)
  err2 = err1 / real
  print("REKURENCYJNIE:")
  print("SUMA:", sumaReq, "BEZWZGLEDNY:", err1, "WZGLEDNY:", err2)
  print('CZAS: {}'.format(end_time - start_time))
  print("%:", err2 * 100)
  pyplot.plot(X, relativeErrors, marker=".", markersize=1, linestyle='None')
  pyplot.show()

zad1()