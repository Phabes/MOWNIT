import numpy as np
import matplotlib.pyplot as plt

x = lambda s, t: np.cos(s) * np.sin(t)

y = lambda s, t: np.sin(s) * np.sin(t)

z = lambda t: np.cos(t)


def create_sphere(n):
    s_points = np.linspace(0, 2 * np.pi, n)
    t_points = np.linspace(0, np.pi, n)
    sphere_points = np.array([[x(s, t), y(s, t), z(t)] for s in s_points for t in t_points])
    return sphere_points


def draw(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=points[:, 2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


def draw_with_semiaxes(s, vh, points):
    axes = np.diag(s) @ vh
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=points[:, 2])
    ax.quiver(0, 0, 0, axes[:, 0], axes[:, 1], axes[:, 2], color="red")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


def generate_random_matrixes(n, size):
    matrixes = [generate_random_matrix(size) for _ in range(n)]
    return matrixes


def generate_random_matrix(size):
    return np.random.randint(1, 10, (size, size))
    # return np.random.rand(size,size)


# 1.
points = create_sphere(30)
draw(points)
# 2.
matrixes = generate_random_matrixes(3, 3)
for matrix in matrixes:
    draw(points @ matrix)
# 3.
for matrix in matrixes:
    u, s, vh = np.linalg.svd(matrix)
    draw_with_semiaxes(s, vh, points @ matrix)
# 4.
matrix = generate_random_matrix(3)
draw(points @ matrix)
u, s, vh = np.linalg.svd(matrix)
ratio = s[0] / s[-1]
s[0] *= 100 / ratio
matrix_bad_cond = u @ np.diag(s) @ vh
draw(points @ matrix_bad_cond)
# 5.
matrix = generate_random_matrix(3)
u, s, vh = np.linalg.svd(matrix)
draw(points @ vh)
draw(points @ np.diag(s) @ vh)
draw(points @ u @ np.diag(s) @ vh)
print(np.allclose(matrix, u @ np.diag(s) @ vh))