import numpy as np
import copy
import random


def printMatrix(M):
  for line in M:
    print(line)
  print()


def factorization(LU):
  n = len(LU)
  for i in range(n):
    if LU[i][i] == 0:
      print("Nie dzielimy przez 0")
      break
    for j in range(i + 1, n):
      factor = LU[j][i] / LU[i][i]
      for k in range(i + 1, n):
        LU[j][k] -= (LU[i][k] * factor)
      LU[j][i] = factor


def checkCorrectness(A, LU, eps):
  n = len(A)
  for i in range(n):
    for j in range(n):
      total = 0
      for k in range(n):
        if k <= j and k <= i:
          if k == i:
            total += LU[k][j]
          else:
            total += (LU[i][k] * LU[k][j])
      if abs(A[i][j] - total) > eps:
        return False
  return True


def test(n):
  A = [[random.randint(-1000, 1000) for _ in range(n)] for _ in range(n)]
  A = np.array(A, dtype=float)
  LU = copy.deepcopy(A)
  factorization(LU)
  print("SIZE:", n)
  print("CORRECT:", checkCorrectness(A, LU, 1e-5))


test(5)
test(100)
test(200)
