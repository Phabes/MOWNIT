import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def create_random_graph(n, k, alpha):
    graph = nx.random_k_out_graph(n, k, alpha)
    return graph


def draw_graph(graph, pos):
    nx.draw(graph, pos=pos)
    nx.draw_networkx_labels(graph, pos)
    plt.show()


def draw_graph_with_rank(graph, pos, r):
    mapping = dict(zip(graph, r))
    nx.draw(graph, pos=pos, with_labels=True, labels=mapping)
    plt.show()


def ranking(graph, r):
    mapping = list(zip(graph, r))
    mapping.sort(key=lambda x: x[1], reverse=True)
    return mapping


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


def rank_nodes(graph, d):
    n = graph.number_of_nodes()
    A = np.zeros((n, n))
    for u, v in graph.edges():
        Fu = graph.out_edges(u)
        Nu = len(Fu)
        A[u, v] = 1 / Nu

    iterations = 100
    eps = 1e-10
    r = power_iteration(d * A, iterations, eps)
    for i in range(n):
        r[1][i] = round(r[1][i], 3)
    return r[1]


n = 10
k = n - 7
alpha = 3
graph = create_random_graph(n, k, alpha)
pos = nx.random_layout(graph)
draw_graph(graph, pos)
d = 1
r = rank_nodes(graph, d)
draw_graph_with_rank(graph, pos, r)
rank = ranking(graph, r)
print(rank)
