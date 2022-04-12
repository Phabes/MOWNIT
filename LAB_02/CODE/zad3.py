import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def create_directed_graph(resistors, stE):
  graph = nx.DiGraph()
  for a, b, resistance in resistors:
    graph.add_edge(a, b, weight=resistance)
  s, t, E = stE
  if (s, t) not in graph.edges() and (t, s) not in graph.edges():
    graph.add_edge(s, t, weight=0)
  return graph


def create_system_of_equations(graph, stE):
  s, t, E = stE
  n = graph.number_of_edges()
  A = [[0 for _ in range(n)] for _ in range(n)]
  B = [0 for _ in range(n)]
  # Przyporządkowanie kolejnym krawędziom numerów identyfikacyjnych
  edges = {x: i for i, x in enumerate(graph.edges())}
  equation_row = 0

  # Drugie Prawo Kirchhoffa
  for cycle in nx.cycle_basis(graph.to_undirected()):
    if equation_row >= n:
      break
    for j in range(len(cycle)):
      v1, v2 = cycle[j - 1], cycle[j]
      # Wpisanie oporów elektrycznych do macierzy na podstawie identyfikatorów krawędzi
      if (v1, v2) in edges:
        A[equation_row][edges[v1, v2]] = graph[v1][v2]['weight']
      else:
        A[equation_row][edges[v2, v1]] = -graph[v2][v1]['weight']
      # Sprawdzenie czy siła elektromotoryczne zawarta jest dostarczana przez krawedź
      if (v1, v2) == (s, t):
        B[equation_row] = E
      elif (v2, v1) == (s, t):
        B[equation_row] = -E
    equation_row += 1

  # Pierwsze Prawo Kirchhoffa
  for v1 in graph.nodes():
    if equation_row >= n:
      break
    # Wychodzace krawedzie
    for v2 in graph[v1]:
      A[equation_row][edges[v1, v2]] = 1
    # Wchodzace krawedzie
    for v2, w in graph.in_edges(v1):
      # print(v1, v2, row, edges[v2, v1])
      A[equation_row][edges[v2, v1]] = -1
    equation_row += 1

  return A, B, edges


def create_amperage_flow_graph(solution, edges):
  solution_graph = nx.DiGraph()
  for edge, i in edges.items():
    a, b = edge[0], edge[1]
    if solution[i] < 0:
      a, b = edge[1], edge[0]
    solution_graph.add_edge(a, b, weight=round(abs(solution[i]), 2))
  return solution_graph


def getData(file_name):
  directed_edges = []
  f = open(file_name, "r")
  for line in f:
    a = line.strip().split(",")
    for i in range(len(a)):
      a[i] = int(a[i])
    directed_edges.append(a)
  f.close()
  return directed_edges


def amperage_flow(file_name, stE):
  directed_edges = getData(file_name)
  solve_and_test(directed_edges, stE, draw_graph)


def check_solution(graph, solution_graph, stE, eps):
  s, t, E = stE
  # Należy przekonwertować na graf nieskierowany, żeby nie było problemów
  graph = graph.to_undirected()
  # Przyporządkowanie kolejnym krawędziom numerów identyfikacyjnych
  edges = {x: i for i, x in enumerate(solution_graph.edges())}

  # Drugie Prawo Kirchhoffa
  for cycle in nx.cycle_basis(graph):
    voltage = 0
    for j in range(len(cycle)):
      v1, v2 = cycle[j - 1], cycle[j]
      if (v1, v2) in edges:
        voltage += solution_graph[v1][v2]["weight"] * graph[v1][v2]["weight"]
      else:
        voltage -= solution_graph[v2][v1]["weight"] * graph[v1][v2]["weight"]
      # Sprawdzenie czy siła elektromotoryczne zawarta jest dostarczana przez krawedź
      if (v1, v2) == (s, t):
        voltage -= E
      elif (v2, v1) == (s, t):
        voltage += E
    if abs(voltage) > eps:
      return False

  # Pierwsze Prawo Kirchhoffa
  for v1 in solution_graph.nodes():
    amperage = 0
    # Wychodzace krawedzie
    for v2 in solution_graph[v1]:
      amperage -= solution_graph[v1][v2]["weight"]
    # Wchodzace krawedzie
    for v2, w in solution_graph.in_edges(v1):
      amperage += solution_graph[v2][v1]["weight"]
    if abs(amperage) > eps:
      return False

  return True


def amperage_flow_random(n):
  directed_edges = create_random_graph(n)
  s, t, _ = directed_edges[randint(0, len(directed_edges) - 1)]
  stE = (s, t, randint(10, 20))
  solve_and_test(directed_edges, stE, draw_graph)


def create_random_graph(n):
  edges = []
  for i, j in nx.gnm_random_graph(n, 2 * n).edges():
    edges.append((i, j, randint(1, 10)))
  return edges


def draw_graph(graph):
  plt.figure(figsize=(12, 6))
  labels = nx.get_edge_attributes(graph, 'weight')
  edges, weights = zip(*labels.items())
  pos = nx.spring_layout(graph)
  nx.draw(graph, pos, with_labels=True, node_color='r', edgelist=edges, edge_color=weights, width=2.0,
          edge_cmap=plt.cm.Blues)
  nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels)
  plt.show()


def amperage_flow_cubical():
  directed_edges = create_cubical_graph()
  s, t, _ = directed_edges[randint(0, len(directed_edges) - 1)]
  stE = (s, t, randint(100, 500))
  solve_and_test(directed_edges, stE, draw_cubical_graph)


def create_cubical_graph():
  edges = []
  for i, j in nx.generators.small.cubical_graph().edges():
    edges.append((i, j, randint(2, 20)))
  return edges


def draw_cubical_graph(graph):
  plt.figure(figsize=(12, 6))
  labels = nx.get_edge_attributes(graph, 'weight')
  edges, weights = zip(*labels.items())
  pos = {0: (0, 0), 1: (0, 2), 2: (2, 2), 3: (2, 0), 4: (3, 1), 5: (5, 1), 6: (5, 3), 7: (3, 3)}
  nx.draw(graph, pos, with_labels=True, node_color='r', edgelist=edges, edge_color=weights, width=2.0,
          edge_cmap=plt.cm.Blues)
  nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels)
  plt.show()


def amperage_flow_bridge(n):
  s = randint(0, n - 2)
  t = randint(s + 1, n - 1)
  stE = (s, t, randint(10, 20))
  directed_edges = create_bridge_graph(n)
  solve_and_test(directed_edges, stE, draw_graph)


def create_bridge_graph(n):
  edges = []
  for i, j in nx.gnm_random_graph(n, 2 * n).edges():
    edges.append((i, j, randint(1, 10)))
  for i, j in nx.gnm_random_graph(n, 2 * n).edges():
    edges.append((i + n, j + n, randint(1, 10)))
  edges.append((n - 1, n, randint(1, 10)))
  return edges


def amperage_flow_net(n, k):
  directed_edges = create_net_graph(n, k)
  stE = (directed_edges[0][0], directed_edges[0][1], randint(100, 500))
  solve_and_test(directed_edges, stE, draw_net_graph)


def create_net_graph(n, k):
  edges = []
  for i, j in nx.generators.lattice.grid_2d_graph(n, k).edges():
    edges.append((i, j, randint(1, 10)))
  return edges


def draw_net_graph(graph):
  n = int(math.sqrt(graph.number_of_edges()))
  plt.figure(figsize=(12, 6))
  labels = nx.get_edge_attributes(graph, 'weight')
  edges, weights = zip(*labels.items())
  pos = {(i, j): (i, j) for i in range(n) for j in range(n)}
  nx.draw(graph, pos, with_labels=True, node_color='r', edgelist=edges, edge_color=weights, width=2.0,
          edge_cmap=plt.cm.Blues)
  nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels)
  plt.show()


def amperage_flow_small_world(n, k, p):
  directed_edges = create_small_world_graph(n, k, p)
  s, t, _ = directed_edges[randint(0, len(directed_edges) - 1)]
  stE = (s, t, randint(100, 500))
  solve_and_test(directed_edges, stE, draw_small_world_graph)


def create_small_world_graph(n, k, p):
  edges = []
  for i, j in nx.watts_strogatz_graph(n=n, k=k, p=p).edges():
    edges.append((i, j, randint(1, 10)))
  return edges


def draw_small_world_graph(graph):
  plt.figure(figsize=(12, 6))
  labels = nx.get_edge_attributes(graph, 'weight')
  edges, weights = zip(*labels.items())
  pos = nx.circular_layout(graph)
  nx.draw(graph, pos, with_labels=True, node_color='r', edgelist=edges, edge_color=weights, width=2.0,
          edge_cmap=plt.cm.Blues)
  nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels)
  plt.show()


def solve_and_test(directed_edges, stE, drawing):
  graph = create_directed_graph(directed_edges, stE)
  A, B, edges = create_system_of_equations(graph, stE)
  solution = np.linalg.solve(A, B)
  solution_graph = create_amperage_flow_graph(solution, edges)
  drawing(solution_graph)
  eps = 0.5
  correct = check_solution(graph, solution_graph, stE, eps)
  print("CORRECT:", correct)


amperage_flow_random(100)
amperage_flow_cubical()
amperage_flow_bridge(3)
amperage_flow_net(5, 7)
amperage_flow_small_world(200, 4, 0.5)
file_name = "graph.txt"
stE = (6, 5, 122)
amperage_flow(file_name, stE)
