import math
import matplotlib.pyplot as plt
import numpy as np
from random import randint, random
from matplotlib import colors
import time


def generate_binary_image(n, density):
  return np.array([[random() < density for _ in range(n)] for _ in range(n)])


def draw(image):
  n = len(image)
  colormap = colors.ListedColormap(["white", "black"])
  plt.figure(figsize=(7, 7))
  plt.imshow(image, cmap=colormap)
  plt.xlim([0, n - 1])
  plt.ylim([0, n - 1])
  plt.show()


def distance_line(points, i, j):
  n = len(points)
  # p1 = (0, 0)
  # p2 = (n - 1, n - 1)
  # p3 = (j, i)
  # p1 = (23 * (n // 33), n // 10)
  # p2 = (n // 5, 4 * (n // 5))
  # p3 = (j, i)
  # energy = (abs((p2[1] - p1[1]) * (p2[0] - p3[0]) - (p2[1] - p3[1]) * (p2[0] - p1[0])) / np.sqrt(
  #   np.square(p2[1] - p1[1]) + np.square(p2[0] - p1[0])))
  # energy = abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1))

  energy = abs(2 * (n // 3) - i)

  # energy = abs(n // 5 - j)
  return energy


def distance_point(points, i, j):
  n = len(points)
  p1 = [n // 2, n // 2]
  p2 = [j, i]
  energy = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
  return energy


def f(points):
  energy = 0
  n = len(points)
  for i in range(n):
    for j in range(n):
      if points[i, j]:
        energy += distance_line(points, i, j)
        # energy += distance_point(points, i, j)
  return energy


def f2(points, neighbourhood):
  energy = 0
  n = len(points)
  for i in range(n):
    for j in range(n):
      if points[i, j]:
        energy += neighbourhood_distance(points, i, j, neighbourhood)
  return energy


def neighbourhood_distance(points, i, j, neighbourhood):
  n = len(points)
  energy = 0
  p2 = [j, i]
  for y in range(i - neighbourhood, i + neighbourhood):
    if 0 <= y < n:
      for x in range(j - neighbourhood, j + neighbourhood):
        if 0 <= x < n and points[y, x]:
          p1 = [x, y]
          energy += np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
  return energy


def swap(points, neighbourhood, density):
  n = len(points)
  T = []
  for _ in range(int(n * density)**2):
    p1x = randint(neighbourhood, n - neighbourhood - 1)
    p1y = randint(neighbourhood, n - neighbourhood - 1)
    add_x = randint(-neighbourhood, neighbourhood)
    add_y = randint(-neighbourhood, neighbourhood)
    p2x = p1x + add_x
    p2y = p1y + add_y
    if (points[p1y, p1x] + points[p2y, p2x]) % 2 == 1:
      points[p1y, p1x], points[p2y, p2x] = points[p2y, p2x], points[p1y, p1x]
      T.append(((p1y, p1x), (p2y, p2x)))
  return T


def solution(points, temp_start, temp_end, temp_iter, temp_rate, neighbourhood, density):
  n = len(points)
  # rem = [[points[i, j] for j in range(n)] for i in range(n)]
  best = f(points)
  # best = f2(points, neighbourhood)
  iterations = 0
  x = []
  y = []
  while temp_start > temp_end:
    for i in range(temp_iter):
      T = swap(points, neighbourhood, density)
      possible = f(points)
      # possible = f2(points, neighbourhood)
      if possible < best:
        best = possible
        # rem = [[points[i, j] for j in range(n)] for i in range(n)]
        # for i in range(n):
        #   for j in range(n):
        #     rem[i][j] = points[i, j]
      else:
        prob = math.e ** ((best - possible) / temp_start)
        check_number = random()
        if check_number < prob:
          best = possible
          # rem = [[points[i, j] for j in range(n)] for i in range(n)]
          # for i in range(n):
          #   for j in range(n):
          #     rem[i][j] = points[i, j]
        else:
          for p1, p2 in list(reversed(T)):
            p1y, p1x = p1
            p2y, p2x = p2
            points[p1y, p1x], points[p2y, p2x] = points[p2y, p2x], points[p1y, p1x]

    x.append(iterations)
    y.append(best)
    for i in range(temp_iter):
      temp_start *= temp_rate
      iterations += 1
    # temp_start *= temp_rate
    # iterations += 1
    print(temp_start)
  print(iterations)

  plt.plot(x, y, "c-")
  plt.xlabel("iterations")
  plt.ylabel("f")
  plt.show()


if __name__ == "__main__":
  n = 256
  density = 0.1
  neighbourhood = 50
  image = generate_binary_image(n, density)
  draw(image)

  temp_start = 5230
  temp_end = 0.1
  temp_iter = 20
  temp_rate = 0.99
  start = time.time()
  solution(image, temp_start, temp_end, temp_iter, temp_rate, neighbourhood, density)
  end = time.time()
  print(end - start)
  draw(image)
