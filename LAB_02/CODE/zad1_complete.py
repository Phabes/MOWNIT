# n = int(input('Enter n: '))
# n = 3
# n = 4

# a = [[0 for _ in range(n + 1)] for _ in range(n)]
# A = [
#   [1, 1, 1, 6],
#   [1, 2, -1, 4],
#   [2, -1, 1, 4]
# ]
A = [
  [2, 2, -1, 1, 7],
  [-1, 1, 2, 3, 3],
  [3, -1, 4, -1, 31],
  [1, 4, -2, 2, 2]
]
# A = [
#   [3, 2, -4, 3],
#   [2, 3, 3, 15],
#   [5, -3, 1, 14]
# ]
n = len(A)

solution = [0 for _ in range(n)]
for line in A:
  print(line)
print()
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
print()
for line in A:
  print(line)
print()
print(solution)
