import numpy
from matplotlib import pyplot


def zad4():
  def logicSingle(x):
    return numpy.single(r * numpy.single(x) * numpy.single(1 - x))

  def logicDouble(x):
    return numpy.double(r * numpy.double(x) * numpy.double(1 - x))

  x0s = [numpy.single(0.2), numpy.single(0.345), numpy.single(0.52), numpy.single(0.89324)]
  x0d = [numpy.double(0.2), numpy.double(0.345), numpy.double(0.52), numpy.double(0.89324)]
  for k in range(len(x0s)):
    r = 3.73
    X = []
    Y = []
    Y2 = []
    for i in range(20):
      x1 = x0s[k]
      x2 = x0d[k]
      for j in range(1000):
        x1 = logicSingle(x1)
        x2 = logicDouble(x2)
        if (j >= 800):
          X.append(r)
          Y.append(x1)
          Y2.append(x2)
      r += 0.01
    pyplot.clf()
    pyplot.plot(X, Y, marker=".", markersize=5, linestyle='None', label=str(x0s[k])+" single")
    pyplot.plot(X, Y2, marker=".", markersize=2, linestyle='None', label=str(x0d[k])+" double")
    pyplot.legend()
    pyplot.show()

zad4()