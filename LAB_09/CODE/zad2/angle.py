import numpy as np
import cv2
import math
from scipy import ndimage


def repair_image(filename):
    img_before = cv2.imread(filename)
    img_before = cv2.bitwise_not(img_before)
    # cv2.imshow("Before", img_before)
    # key = cv2.waitKey(0)
    img_gray = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=20, maxLineGap=5)
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        # cv2.line(img_before, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    # cv2.imshow("Detected lines", img_before)
    # key = cv2.waitKey(0)
    median_angle = np.median(angles)
    print("Angle: " + str(median_angle))
    if median_angle == 0:
        print("No need to rotate image")
        return filename
    print("Rotating image...")
    img_rotated = ndimage.rotate(img_before, median_angle)
    img_rotated = cv2.bitwise_not(img_rotated)

    arr = filename.split(".")
    rotated_filename = arr[0] + "_rotated.png"
    cv2.imwrite(rotated_filename, img_rotated)
    return rotated_filename
