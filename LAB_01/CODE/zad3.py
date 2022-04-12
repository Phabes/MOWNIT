import numpy

s = [2, 3.6667, 5, 7.2, 10]
n = [50, 100, 200, 500, 1000]
len_s = len(s)
len_n = len(n)


def zad3():
  def dzeta(n, s):
    sumForwardSingle = numpy.single(0)
    sumBackwardSingle = numpy.single(0)
    sumForwardDouble = numpy.double(0)
    sumBackwardDouble = numpy.double(0)
    for k in range(1, n + 1):
      sumForwardSingle += numpy.single(1 / (k ** s))
      sumForwardDouble += numpy.double(1 / (k ** s))
    for k in range(n, 0, -1):
      sumBackwardSingle += numpy.single(1 / (k ** s))
      sumBackwardDouble += numpy.double(1 / (k ** s))
    return sumForwardSingle, sumBackwardSingle, sumForwardDouble, sumBackwardDouble

  def eta(n, s):
    sumForwardSingle = numpy.single(0)
    sumBackwardSingle = numpy.single(0)
    sumForwardDouble = numpy.double(0)
    sumBackwardDouble = numpy.double(0)
    for k in range(1, n + 1):
      sumForwardSingle += numpy.single((-1) ** (k - 1) / (k ** s))
      sumForwardDouble += numpy.double((-1) ** (k - 1) / (k ** s))
    for k in range(n, 0, -1):
      sumBackwardSingle += numpy.single((-1) ** (k - 1) / (k ** s))
      sumBackwardDouble += numpy.double((-1) ** (k - 1) / (k ** s))
    return sumForwardSingle, sumBackwardSingle, sumForwardDouble, sumBackwardDouble

  for i in range(len_n):
    for j in range(len_s):
      print("n:", n[i], "s:", s[j])
      dz = dzeta(n[i], s[j])
      et = eta(n[i], s[j])
      print("dzeta")
      print("forwardSingle backwardSingle forwardDouble backwardDouble")
      print(dz)
      print("Difference single:", dz[1] - dz[0])
      print("Difference double:", dz[3] - dz[2])
      print("eta")
      print("forwardSingle backwardSingle forwardDouble backwardDouble")
      print(et)
      print("Difference single:", et[1] - et[0])
      print("Difference double:", et[3] - et[2])
      print()

zad3()