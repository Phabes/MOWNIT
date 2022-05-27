import numpy as np
import matplotlib.pyplot as plt


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


def test_gram_schmidt_factorization(sizes):
    for size in sizes:
        A = np.random.rand(size, size)
        Q, R = gram_schmidt_factorization(A)
        Q_lib, R2_lib = np.linalg.qr(A)
        print("Array size:", size, "x", size)
        print("close:", np.allclose(Q @ R, Q_lib @ R2_lib))


def condition_number(n):
    conds = []
    vals = []
    while len(conds) < n:
        A = np.random.rand(8, 8)
        U, S, Vh = np.linalg.svd(A)
        cond = S[0] / S[-1]
        if cond not in conds:
            conds.append(cond)
            Q, R = gram_schmidt_factorization(A)
            val = np.linalg.norm(np.identity(8) - Q.transpose() @ Q)
            vals.append(val)
    plt.ylabel("I-QtQ")
    plt.xlabel("conds")
    plt.plot(conds, vals, 'o')
    plt.show()


sizes = [5, 25, 50, 100, 500]
test_gram_schmidt_factorization(sizes)
n = 50
condition_number(n)
