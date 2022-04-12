import numpy, random
from datetime import datetime

n = 10 ** 7
x = numpy.single(0.53125)
# x = random.uniform(0.1, 0.9)
# x = numpy.single(x)
T = [x for _ in range(n)]


def zad2():
  def sumKahan(T):
    suma = numpy.single(0)
    err = numpy.single(0)
    for add in T:
      y = add - err
      temp = suma + y
      err = (temp - suma) - y
      suma = temp
    return suma

  real = numpy.single(10 ** 7 * x)
  start_time = datetime.now()
  suma = sumKahan(T)
  end_time = datetime.now()
  err1 = abs(real - suma)
  err2 = err1 / real
  print("X:", x)
  print("DOKLADNA SUMA:", real)
  print("KAHAN:")
  print("SUMA:", suma, "BEZWZGLEDNY:", err1, "WZGLEDNY:", err2, 'CZAS: {}'.format(end_time - start_time))
  print("%:", err2 * 100)

zad2()