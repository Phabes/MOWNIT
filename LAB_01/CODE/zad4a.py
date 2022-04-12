import numpy
from matplotlib import pyplot


def zad4():
  def logic():
    return numpy.single(r * numpy.single(x) * numpy.single(1 - x))

  x0s = [numpy.single(0.2), numpy.single(0.345), numpy.single(0.52), numpy.single(0.89324)]
  for x0 in x0s:
    r = 0
    X = []
    Y = []
    for i in range(21):
      x = x0
      for j in range(1000):
        x = logic()
        if (j >= 800):
          X.append(r)
          Y.append(x)
      r += 0.2
    pyplot.clf()
    pyplot.plot(X, Y, marker=".", markersize=2, linestyle='None', label=str(x0))
    pyplot.legend()
    pyplot.show()

zad4()