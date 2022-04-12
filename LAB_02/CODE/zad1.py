import random
import numpy as np
import time
import matplotlib.pyplot as plt
import scipy.linalg


def complete(A):
  n = len(A)
  solution = [0 for _ in range(n)]
  T = []

  def findBiggestVal(A, start):
    n = len(A)
    y, x = start, start
    for i in range(start, n):
      for j in range(start, n):
        if abs(A[i][j]) > abs(A[y][x]):
          y, x = i, j
    return y, x

  for i in range(n):
    y, x = findBiggestVal(A, i)
    if x != i:
      T.append((x, i))
    for j in range(n + 1):
      A[i][j], A[y][j] = A[y][j], A[i][j]
    for j in range(n):
      A[j][x], A[j][i] = A[j][i], A[j][x]
    if A[i][i] == 0:
      print("Nie dzielimy przez 0")
      break
    for j in range(i + 1, n):
      factor = A[j][i] / A[i][i]
      for k in range(n + 1):
        A[j][k] -= (A[i][k] * factor)
    for j in range(i - 1, -1, -1):
      factor = A[j][i] / A[i][i]
      for k in range(n + 1):
        A[j][k] -= (A[i][k] * factor)

  for i in range(n):
    solution[i] = A[i][n] / A[i][i]
    A[i][n] = solution[i]
    A[i][i] = 1

  for i in range(len(T) - 1, -1, -1):
    y, x = T[i]
    A[y][n], A[x][n] = A[x][n], A[y][n]
    solution[y], solution[x] = solution[x], solution[y]

  print(T)
  print(solution)


def partial(A):
  n = len(A)
  solution = [0 for _ in range(n)]

  def findBestRow(A, start, column):
    n = len(A)
    best = start
    for i in range(start + 1, n):
      if abs(A[i][column]) > A[best][column]:
        best = i
    return best

  for i in range(n):
    index = findBestRow(A, i, i)
    for j in range(n + 1):
      A[i][j], A[index][j] = A[index][j], A[i][j]
    if A[i][i] == 0:
      print("Nie dzielimy przez 0")
      break
    for j in range(i + 1, n):
      factor = A[j][i] / A[i][i]
      for k in range(n + 1):
        A[j][k] -= (A[i][k] * factor)
    for j in range(i - 1, -1, -1):
      factor = A[j][i] / A[i][i]
      for k in range(n + 1):
        A[j][k] -= (A[i][k] * factor)

  for i in range(n):
    solution[i] = A[i][n] / A[i][i]
    A[i][n] = solution[i]
    A[i][i] = 1

  return solution


def scaling(A):
  n = len(A)
  solution = [0 for _ in range(n)]
  for i in range(n):
    if A[i][i] == 0:
      print("Nie dzielimy przez 0")
      break
    for j in range(i + 1, n):
      factor = A[j][i] / A[i][i]
      for k in range(n + 1):
        A[j][k] -= (A[i][k] * factor)
    for j in range(i - 1, -1, -1):
      factor = A[j][i] / A[i][i]
      for k in range(n + 1):
        A[j][k] -= (A[i][k] * factor)

  for i in range(n):
    solution[i] = A[i][n] / A[i][i]
    A[i][n] = solution[i]
    A[i][i] = 1
  return solution


def test(n):
  print(n)
  A = [[random.randint(-1000, 1000) for _ in range(n)] for _ in range(n)]
  B = [random.randint(-1000, 1000) for _ in range(n)]

  C = [[0 for _ in range(n + 1)] for _ in range(n)]
  for i in range(n):
    for j in range(n):
      C[i][j] = A[i][j]
  for i in range(n):
    C[i][n] = B[i]

  start = time.time()
  npSolution = np.linalg.solve(A, B)
  end = time.time()
  diff = end - start
  print("Numpy:", diff)
  npTimes.append(diff)

  start = time.time()
  scSolution = scipy.linalg.solve(A, B)
  end = time.time()
  diff = end - start
  print("Scipy:", diff)
  scTimes.append(diff)

  start = time.time()
  # implementedSolution = scaling(C)
  implementedSolution = partial(C)
  # implementedSolution = complete(C)
  end = time.time()
  diff = end - start
  print("Implemented:", diff)
  implementedTimes.append(diff)
  print("Close numpy scipy: ", np.allclose(npSolution, scSolution))
  print("Close numpy implemented: ", np.allclose(npSolution, implementedSolution))
  print("Close scipy implemented: ", np.allclose(scSolution, implementedSolution))
  matrixSizes.append(n)


npTimes = []
scTimes = []
implementedTimes = []
matrixSizes = []

for n in range(500, 600, 10):
  test(n)

plt.plot(matrixSizes, npTimes, label='numpy', color='darksalmon', marker='o', linewidth=2)
plt.plot(matrixSizes, scTimes, label='scipy', color='skyblue', marker='o', linewidth=2)
plt.legend()
plt.show()
plt.plot(matrixSizes, implementedTimes, label='gauss-jordan', color='red', marker='o', linewidth=2)
plt.legend()
plt.show()
