import numpy
from matplotlib import pyplot


def zad4():
  def logic():
    return numpy.single(r * numpy.single(x) * numpy.single((1 - x)))

  x0 = []
  y0 = []
  r = 4
  for i in range(100):
    x = i * 0.01
    for j in range(1000):
      x = logic()
      if x == 0:
        x0.append(i * 0.01)
        y0.append(j)
        break
  print("x0:", x0)
  print("integrations:", y0)
  pyplot.plot(x0, y0, marker=".", markersize=2, linestyle='None', label=str(x0))
  pyplot.show()

zad4()