import numpy as np
import matplotlib.pyplot as plt


def trapez(x1, y1, x2, y2):
    return (y1 + y2) * (x2 - x1) / 2


def distance(speeds, times):
    times /= 3600
    # field = np.trapz(speeds, x=times)
    distances = [0 for _ in range(len(speeds))]
    for i in range(1, len(distances)):
        distances[i] = trapez(times[i - 1], speeds[i - 1], times[i], speeds[i])
    print(distances)
    field = sum(distances)
    plt.plot(times, speeds)
    plt.xlabel("time [h]")
    plt.ylabel("speed [km/h]")
    plt.show()
    return field


y = np.array([40, 50, 60, 80])
x = np.array([0, 3600, 7200, 10800], dtype="float32")
print(distance(y, x))
