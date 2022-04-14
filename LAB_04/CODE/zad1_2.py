import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import glob
from random import randint, random, shuffle
from PIL import Image


def save_graph(graph, points, index):
  pos = {i: point[1] for i, point in enumerate(points)}
  node_numbers = {i: point[0] for i, point in enumerate(points)}
  nx.draw(graph, pos, labels=node_numbers, font_size=6, node_size=100)
  plt.title = str(index)
  plt.savefig(str(index) + ".png", format="PNG")
  plt.clf()


def create_gif(text):
  frames = []
  imgs = glob.glob("*.png")
  imgs_array = [(int(img[:len(img) - 4]), img) for img in imgs]
  imgs_array.sort(key=lambda img: img)
  for _, file_name in imgs_array:
    new_frame = Image.open(file_name)
    frames.append(new_frame)
  frames[0].save("tsp_" + text + ".gif", format="GIF",
                 append_images=frames[1:],
                 save_all=True,
                 duration=500, loop=0)
  for _, file_name in imgs_array:
    os.remove(file_name)


def generate_random(n):
  points = []
  while len(points) != n:
    x = randint(0, n)
    y = randint(0, n)
    tup = (x, y)
    if tup not in points:
      points.append(tup)

  points = [(i, point) for i, point in enumerate(points)]
  return points


def generate_uniform(n):
  points = []
  while len(points) != n:
    x = np.random.uniform(n, high=1)
    y = np.random.uniform(n, high=1)
    tup = (x, y)
    if tup not in points:
      points.append(tup)

  points = [(i, point) for i, point in enumerate(points)]
  return points


def generate_normal(n, loc, scale):
  points = []
  while len(points) != n:
    x = np.random.normal(n // loc, scale)
    y = np.random.normal(n // loc, scale)
    tup = (x, y)
    if tup not in points:
      points.append(tup)

  points = [(i, point) for i, point in enumerate(points)]
  return points


def generate_groups(n, k):
  points = []
  addX = 0
  addY = 0
  factor = int(math.sqrt(k))
  while len(points) != n:
    x = (n // k) * random() + addX * factor * (n // k)
    y = (n // k) * random() + addY * factor * (n // k)
    tup = (x, y)
    if tup not in points:
      points.append(tup)
    if len(points) % (n // k) == 0:
      addX += 1
      if addX % (k // factor) == 0:
        addX = 0
        addY += 1
      if addX + factor * addY == k:
        addY = 0

  shuffle(points)
  points = [(i, point) for i, point in enumerate(points)]
  return points


def current_solution_distance(points):
  n = len(points)
  sum = 0
  for i in range(n):
    sum += distance(points[i - 1], points[i])
  return sum


def distance(p1, p2):
  i1, pos1 = p1
  i2, pos2 = p2
  x1, y1 = pos1
  x2, y2 = pos2
  return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def create_directed_graph(points):
  graph = nx.DiGraph()
  n = len(points)
  for i in range(n - 1):
    graph.add_edge(i, i + 1)
  graph.add_edge(n - 1, 0)
  return graph


def draw_graph(graph, points):
  pos = {i: point[1] for i, point in enumerate(points)}
  node_numbers = {i: point[0] for i, point in enumerate(points)}
  nx.draw(graph, pos, labels=node_numbers, font_size=6, node_size=100)
  plt.show()


def solution(points, temp_start, temp_end, temp_iter, temp_rate, arbitrary_swap):
  n = len(points)
  text = "ARBITRARY" if arbitrary_swap else "CONSECUTIVE"
  print(text)
  best = current_solution_distance(points)
  print("START DIST:", best)
  iterations = 0
  x = []
  y = []
  save_graph(graph, points, iterations)
  while temp_start > temp_end:
    for i in range(temp_iter):
      p1 = randint(0, n - 2)
      p2 = randint(p1 + 1, n - 1) if arbitrary_swap else p1 + 1
      points[p1], points[p2] = points[p2], points[p1]
      possible = current_solution_distance(points)
      if possible < best:
        best = possible
      else:
        prob = math.e ** ((best - possible) / temp_start)
        check_number = random()
        if check_number < prob:
          best = possible
        else:
          points[p1], points[p2] = points[p2], points[p1]
    x.append(iterations)
    y.append(best)
    # for i in range(temp_iter):
    #     temp_start *= temp_rate
    temp_start *= temp_rate
    iterations += 1
    if iterations % 100 == 0:
      save_graph(graph, points, iterations)
  print("END DIST:", best)
  save_graph(graph, points, iterations)
  plt.plot(x, y, "c-")
  plt.xlabel("iterations")
  plt.ylabel("f")
  plt.show()
  create_gif(text)


if __name__ == "__main__":
  temps = [0.99, 0.95, 0.8]
  n = 100
  temp_start = 5230
  temp_end = 0.1
  temp_iter = 40
  k = 9
  points = generate_groups(n, k)
  for temp_rate in temps:
    # temp_rate = 0.95
    # points = generate_random(n)
    # points = generate_uniform(n)
    # loc=2
    # scale = 4.3
    # points = generate_normal(n,loc,scale)
    points.sort(key=lambda tup: tup[0])
    graph = create_directed_graph(points)
    draw_graph(graph, points)
    arbitrary_swap = True
    solution(points, temp_start, temp_end, temp_iter, temp_rate, arbitrary_swap)
    print(points)
    draw_graph(graph, points)
    points.sort(key=lambda tup: tup[0])
    arbitrary_swap = False
    solution(points, temp_start, temp_end, temp_iter, temp_rate, arbitrary_swap)
    print(points)
    draw_graph(graph, points)
