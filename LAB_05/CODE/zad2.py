import numpy as np
import imageio

image = imageio.imread("lenna.gif")
u, s, vh = np.linalg.svd(image)
k_values = [10, 20, 30, 100]
for k in k_values:
    Ia = np.zeros((len(u), len(vh)))
    for i in range(k):
        Ia += s[i] * np.outer(u.T[i], vh[i])
    imageio.imsave("output/out" + str(k) + ".png", Ia)