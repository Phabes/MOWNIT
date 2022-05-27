import random
import numpy as np


def F(n):
    ksi = np.exp(-2 * np.pi * 1j / n)
    return np.array([[ksi ** (j * k) for j in range(n)] for k in range(n)], dtype=complex)


def dft(x):
    n = len(x)
    return F(n) @ x


def idft(y):
    n = len(y)
    return np.conjugate(F(n)) @ y / n


def fft(x):
    n = len(x)
    if n == 1:
        return x

    evens = []
    odds = []
    for i in range(n):
        if i % 2 == 0:
            evens.append(x[i])
        else:
            odds.append(x[i])

    part1 = fft(evens)
    part2 = fft(odds)

    length = len(part1)  # = len(part2) = n // 2
    for k in range(length):
        p = part1[k]
        q = np.exp(-2 * np.pi * 1j * k / n) * part2[k]
        part1[k] = p + q
        part2[k] = p - q

    return np.concatenate((part1, part2))


r = 4
x = [random.randint(1, 20) for _ in range(2 ** r)]  # x length must be power of 2
y_impl = dft(x)
y_libl = np.fft.fft(x)
x_impl = idft(y_impl)
x_libl = np.fft.ifft(y_libl)
print("IMPLEMENTATION X RESULTS ARE OK:", np.allclose(x, x_impl))
print("LIBRARY X RESULTS ARE OK:", np.allclose(x, x_libl))
print("Y DFT RESULTS ARE OK:", np.allclose(y_impl, y_libl))
y_fft = fft(x)
print("Y FFT RESULTS ARE OK:", np.allclose(y_fft, y_libl))
