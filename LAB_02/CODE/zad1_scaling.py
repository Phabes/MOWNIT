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
n = len(A)

solution = [0 for _ in range(n)]
for line in A:
  print(line)
print()

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

for line in A:
  print(line)
print()
print(solution)
