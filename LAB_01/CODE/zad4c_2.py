import numpy
from matplotlib import pyplot


def zad4():
  def logic():
    return numpy.single(r * numpy.single(x) * numpy.single(1 - x))
  def logic2(n, x0):
    if n==0:
      D.append(numpy.single(x0))
      return numpy.single(x0)
    a=logic2(n-1,x0)
    b=numpy.single(r * a * numpy.single(1-a))
    D.append(b)
    return b

  x0 = []
  y0 = []
  D=[]
  r = 4
  # logic2(500,0.03)
  for i in range(100):
    D=[]
    logic2(500,i*0.01)
    if D[499]==0:
      x0.append(i*0.01)
  for i in range(len(x0)):
    D=[]
    logic2(500,x0[i])
    for j in range(500):
      if D[j]==0:
        y0.append(j)
        break
  # for i in range(100):
  #   x = numpy.single(i * 0.01)
  #   for j in range(1000):
  #     x = logic()
  #     if x == 0:
  #       x0.append(i * 0.01)
  #       y0.append(j)
  #       break
  print(x0)
  print(y0)
  # print(D)
  pyplot.plot(x0, y0, marker=".", markersize=2, linestyle='None', label=str(x0))
  pyplot.show()


zad4()
