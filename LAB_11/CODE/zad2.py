import numpy as np
import matplotlib.pyplot as plt

xs = np.arange(-5, 6, 1, dtype="float64")
ys = np.array([2, 7, 9, 12, 13, 14, 14, 13, 10, 8, 4], dtype="float64")
f = lambda x, alphas: alphas[0] + alphas[1] * x + alphas[2] * x ** 2


def backward_substitution(A_original, B_original):
    n = B_original.shape[0]
    A = np.copy(A_original)
    B = np.copy(B_original)
    for i in range(n - 1, -1, -1):
        divisor = A[i, i]
        for j in range(i - 1, -1, -1):
            tmp = A[j, i] / divisor
            A[j] -= tmp * A[i]
            B[j] -= tmp * B[i]
            A[j, i] = 0.0
        B[i] /= divisor

    return B


def gram_schmidt_factorization(A):
    n = len(A)
    Q = np.zeros((n, n))
    R = np.zeros((n, n))
    Q[:, 0] = A[:, 0] / np.linalg.norm(A[:, 0])
    for k in range(1, n):
        current_a = A[:, k]
        Q[:, k] = current_a
        for i in range(k):
            current_u = Q[:, i]
            Q[:, k] -= np.dot(current_u, current_a) * current_u
        Q[:, k] /= np.linalg.norm(Q[:, k])
    for i in range(n):
        for j in range(i, n):
            R[i, j] = np.dot(Q[:, i], A[:, j])
    return Q, R


def solve_qr(xs, ys):
    # I sp
    # A = np.array([[1, x, x * x] for x in xs])
    # II sp
    A = np.vander(xs, increasing=True)
    A = A[:, :3]

    # I sp
    Q, R = np.linalg.qr(A)
    return backward_substitution(R, Q.T @ ys)  # return np.linalg.solve(R, Q.T @ ys)
    # II sp
    # Q, R = gram_schmidt_factorization(A.T @ A)
    # return backward_substitution(R, Q.T @ A.T @ ys)  # return np.linalg.solve(R, Q.T @ A.T @ ys)
    # III sp
    # return backward_substitution(A.T @ A, A.T @ ys)  # return np.linalg.solve(A.T @ A, A.T @ ys)


print(xs)
print(ys)
a = solve_qr(xs, ys)
print(a)
x_lin = np.linspace(-6, 6, 200)
plt.plot(x_lin, f(x_lin, a), c="#5ccc3d")
plt.scatter(xs, ys, c="#cc3f3d")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
