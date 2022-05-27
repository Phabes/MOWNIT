import numpy as np
from random import randint
import time
import matplotlib.pyplot as plt


def create_matrix(n):
  return np.array([[randint(1, 20) for _ in range(n)] for _ in range(n)])


def power_iteration(A, iterations, eps):
  n = A.shape[0]
  prev = np.ones(n)
  x = A @ prev
  # max_x = np.linalg.norm(x)
  max_x = max(abs(x))
  x /= max(x)
  i = 1
  while i < iterations and np.linalg.norm(np.subtract(x, prev)) > eps:
    x, prev = A @ x, x
    # max_x = np.linalg.norm(x)
    max_x = max(abs(x))
    x /= max(x)
    i += 1

  return max_x, x / np.linalg.norm(x)


# n = 3
# A = create_matrix(n)
# print(A)
iterations = 100
eps = 1e-10
# my_val, my_vec = power_iteration(A, iterations, eps)
#
# print(np.linalg.eig(A))
# np_val, np_vec = max(np.linalg.eig(A)[0]), np.linalg.eig(A)[1][:, 0]
# print(my_val)
# print(my_vec)
# print(np_val)
# print(np_vec)

# print("VAL", np.isclose(my_val, np_val))
# print("VEC", np.allclose(my_vec, np_vec) or np.allclose(my_vec, -np_vec))

sizes = [100, 500, 1000, 2000, 5000]
X = []
Y = []
for size in sizes:
  print(size)
  A = create_matrix(size)
  start = time.time()
  my_val, my_vec = power_iteration(A, iterations, eps)
  end = time.time()
  np_val, np_vec = max(np.linalg.eig(A)[0]), np.linalg.eig(A)[1][:, 0]
  print("VAL", np.isclose(my_val, np_val))
  print("VEC", np.allclose(my_vec, np_vec) or np.allclose(my_vec, -np_vec))
  X.append(size)
  Y.append(end-start)
plt.plot(X, Y, 'ro')
plt.show()