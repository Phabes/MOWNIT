import numpy as np
from numpy.fft import fft2, ifft2
from PIL import Image, ImageOps
import matplotlib.pyplot as plt


def prepare_image_data(analyzed_image):
    image = Image.open(analyzed_image)
    image_grey = ImageOps.grayscale(image)
    image_invert = ImageOps.invert(image_grey)
    image_rotated = np.swapaxes(np.asarray(image_invert), 0, 1) # for text
    # image_rotated = np.swapaxes(np.asarray(image_grey), 0, 1)  # for fishes
    return image, image_rotated


def show_amplitude_and_phase(image_dft):
    image_back = np.swapaxes(np.array(image_dft), 0, 1)
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(np.log(abs(image_back)))
    ax[0].set_title('Amplituda')
    ax[1].imshow(np.angle(image_back))
    ax[1].set_title('Faza')
    plt.show()


def show_image_with_patterns(image):
    fig, ax = plt.subplots(1, 1)
    ax.imshow(image)
    ax.set_title("Wzorzec nałożone na obraz")
    plt.show()


def fill_space(image, image_loaded, start_x, start_y, x, y, pattern_width, pattern_height):
    image_loaded[start_x - x, start_y - y] = (255, 0, 0)


def fill_frame(image, image_loaded, start_x, start_y, x, y, pattern_width, pattern_height):
    if x == 0 or y == 0 or x == pattern_width - 1 or y == pattern_height - 1:
        image_loaded[start_x - x, start_y - y] = (255, 0, 0)


def condition_fill_space(image, image_loaded, start_x, start_y, x, y, pattern_width, pattern_height):
    r, g, b = image.getpixel((start_x - x, start_y - y))
    if (r, g, b) != (255, 255, 255):
        image_loaded[start_x - x, start_y - y] = (255, 0, 0)


def image_pattern_solution(analyzed_image, pattern_image, coefficient, fill_strategy):
    image, image_rotated = prepare_image_data(analyzed_image)
    pattern, pattern_rotated = prepare_image_data(pattern_image)
    pattern_width, pattern_height = pattern.size
    image_dft = fft2(image_rotated)
    show_amplitude_and_phase(image_dft)
    c = np.real(ifft2(image_dft * fft2(np.rot90(pattern_rotated, k=2), s=image.size)))
    filter_value = coefficient * np.max(c)
    image_loaded = image.load()
    matches = np.argwhere(c >= filter_value)
    print("Liczba wystąpień wzorca:", len(matches))
    for startX, startY in matches:
        for x in range(pattern_width):
            for y in range(pattern_height):
                fill_strategy(image, image_loaded, startX, startY, x, y, pattern_width, pattern_height)
    show_image_with_patterns(image)


image_pattern_solution("Lab9_galia.png", "Lab9_galia_e.png", 0.9, condition_fill_space)
# image_pattern_solution("Lab9_galia.png", "Lab9_galia_e.png", 0.9, fill_frame)
# image_pattern_solution("Lab9_school.jpg", "Lab9_fish1.png", 0.75, fill_space)
# image_pattern_solution("Lab9_school.jpg", "Lab9_fish1.png", 0.75, fill_frame)
