import numpy as np
import PIL.Image
import PIL.ImageDraw
import scipy.sparse.linalg
from numpy.fft import fft2, ifft2
from PIL import Image, ImageOps, ImageFont
import matplotlib.pyplot as plt

from angle import repair_image

chars = "abcdefghijklmnopqrstuvwxyz0123456789.,?!"
special = {
    "z": 1,
    ".": 1,
    ",": 1,
    "?": 1,
    "!": 1
}


def load_letter(letter, font, font_height):
    letter_im = PIL.Image.new('L', (font.getsize(letter)[0], font_height), 0)
    letter_draw = PIL.ImageDraw.Draw(letter_im)
    letter_draw.text((0, 0), letter, font=font, fill=255)
    return np.asarray(letter_im)


def reduce_noise(data):
    height, width = data.shape
    u, s, vh = scipy.sparse.linalg.svds(scipy.sparse.linalg.aslinearoperator(np.array(data, dtype="float32")),
                                        k=min(height - int(height * 0.9) - 1, width - int(width * 0.9) - 1))
    return u @ np.diag(s) @ vh


def prepare_image_data(analyzed_image):
    image = Image.open(analyzed_image)
    image_grey = ImageOps.grayscale(image)
    image_invert = ImageOps.invert(image_grey)
    image_rotated = np.swapaxes(np.asarray(image_invert), 0, 1)
    image_rotated = reduce_noise(image_rotated)  # comment this line if you dont want to reduce noise
    return image, image_rotated


def fill_frame(image_loaded, start_x, start_y, x, y, pattern_width, pattern_height):
    if x == 0 or y == 0 or x == pattern_width - 1 or y == pattern_height - 1:
        image_loaded[start_x - x, start_y - y] = (255, 0, 0)


def do_overlap(l1, r1, l2, r2):
    # If one rectangle is on left side of other
    if l1[1] >= r2[1] or l2[1] >= r1[1]:
        return False
    # If one rectangle is above other
    if l2[0] >= r1[0] or l1[0] >= r2[0]:
        return False
    return True


def surface(l1, r1):
    width = r1[1] - l1[1]
    height = r1[0] - l1[0]
    return width * height


def check_better_new_letter(old_letter, new_letter, font, font_height):
    old_letter_array = load_letter(old_letter, font, font_height)
    old_letter_similar = np.argwhere(old_letter_array > 0)
    new_letter_array = load_letter(new_letter, font, font_height)
    new_letter_similar = np.argwhere(new_letter_array > 0)
    return len(new_letter_similar) > len(old_letter_similar)


def find_height_levels(considerable_matches):
    height_levels = []
    for match in considerable_matches:
        if match[0][0] not in height_levels:
            height_levels.append(match[0][0])
    return height_levels


def reduce_height_levels(detected_height_levels, serif_font_height):
    height_levels = [detected_height_levels[0]]
    for i in range(1, len(detected_height_levels)):
        if detected_height_levels[i] - height_levels[-1] <= serif_font_height / 2:
            height_levels[-1] = detected_height_levels[i]
        else:
            height_levels.append(detected_height_levels[i])
    return height_levels


def change_letters_levels(height_levels, considerable_matches):
    for i, match in enumerate(considerable_matches):
        best_height = height_levels[find_closest(match[0][0], height_levels)]
        if best_height != match[0][0]:
            new_match = ((best_height, match[0][1]), match[1], match[2], match[3])
            considerable_matches[i] = new_match


def find_closest(value, heights):
    best = abs(value - heights[0])
    index = 0
    for i in range(1, len(heights)):
        possible = abs(value - heights[i])
        if possible < best:
            best = possible
            index = i
    return index


def show_image_with_patterns(image):
    fig, ax = plt.subplots(1, 1)
    ax.imshow(image)
    ax.set_title("Wzorzec nałożone na obraz")
    plt.show()


def image_pattern_solution(analyzed_image, fontname, coefficient, fill_strategy, size):
    font = ImageFont.truetype("fonts/" + fontname, size)
    space_width = font.getsize(" ")[0] * 0.9
    font_height = font.getsize(chars)[1]
    image, image_rotated = prepare_image_data(analyzed_image)
    all_matches = []
    for letter in chars:
        print("Checking char " + letter + " from font " + fontname)
        letter_array = load_letter(letter, font, font_height)
        # cannot delete columns filled with zeros because better to leave it
        # letter_array = letter_array[:, ~np.all(letter_array == 0, axis=0)]
        # cannot delete rows filled with zeros because all letters has to have the same height
        # letter_array = letter_array[~np.all(letter_array == 0, axis=1)]
        pattern_height, pattern_width = letter_array.shape
        pattern_rotated = np.swapaxes(np.asarray(letter_array), 0, 1)
        c = np.real(ifft2(fft2(image_rotated) * fft2(np.rot90(pattern_rotated, k=2), s=image.size)))
        maxi = np.max(c)
        possible_coefficient = special.get(letter, -1)
        if possible_coefficient != -1:
            coefficient = possible_coefficient
        filter_value = coefficient * maxi
        matches = np.argwhere(c >= filter_value)
        for start_x, start_y in matches:
            ratio = c[start_x, start_y] / maxi
            if start_y - pattern_height > 0 and start_x - pattern_width > 0:
                # ((y_start, x_start), (height, width), ratio, letter)
                all_matches.append(((start_y, start_x), letter_array.shape, ratio, letter))
    all_matches.sort(key=lambda tup: tup[2], reverse=True)
    considerable_matches = []
    for i in range(len(all_matches)):
        ok = True
        r1 = all_matches[i][0]
        l1 = (r1[0] - all_matches[i][1][0] + 1, r1[1] - all_matches[i][1][1] + 1)
        for j in range(len(considerable_matches)):
            r2 = considerable_matches[j][0]
            l2 = (r2[0] - considerable_matches[j][1][0] + 1, r2[1] - considerable_matches[j][1][1] + 1)
            if do_overlap(l1, r1, l2, r2):
                common_surface = surface((max(l1[0], l2[0]), max(l1[1], l2[1])), (min(r1[0], r2[0]), min(r1[1], r2[1])))
                rect1_surface = surface(l1, r1)
                rect2_surface = surface(l2, r2)
                total_surface = rect1_surface + rect2_surface - common_surface
                ratio = common_surface / total_surface
                if ratio > 0.1:
                    if all_matches[i][2] == considerable_matches[j][2]:
                        if check_better_new_letter(considerable_matches[j][3], all_matches[i][3], font, font_height):
                            considerable_matches[j] = all_matches[i]
                    ok = False
                    break
        if ok:
            considerable_matches.append(all_matches[i])
    detected_height_levels = find_height_levels(considerable_matches)
    detected_height_levels.sort()
    height_levels = reduce_height_levels(detected_height_levels, font_height)
    change_letters_levels(height_levels, considerable_matches)
    considerable_matches.sort(key=lambda tup: tup[0][1] - tup[1][1])  # x sort
    considerable_matches.sort(key=lambda tup: tup[0][0] - tup[1][0])  # y sort
    print()
    chars_occur = {}
    for letter in chars:
        chars_occur[letter] = 0
    for i in range(len(considerable_matches)):
        current_char = considerable_matches[i][3]
        occurs = chars_occur.get(current_char, -1)
        chars_occur[current_char] = occurs + 1
    for letter, occurs in chars_occur.items():
        print(letter, ":", occurs)
    print()
    image_loaded = image.load()
    for i in range(len(considerable_matches)):
        current_char = considerable_matches[i][3]
        start_y, start_x = considerable_matches[i][0]
        pattern_height, pattern_width = considerable_matches[i][1]
        for x in range(pattern_width):
            for y in range(pattern_height):
                fill_strategy(image_loaded, start_x, start_y, x, y, pattern_width, pattern_height)
        if considerable_matches[i][0][0] - considerable_matches[i - 1][0][0] > font_height / 2:
            print("")
        space_between_chars = (considerable_matches[i][0][1] - considerable_matches[i][1][1]) - \
                              considerable_matches[i - 1][0][1]
        if space_between_chars > space_width:
            step = space_width
            while space_between_chars > step:
                print(" ", end="")
                step += space_width
        print(current_char, end="")
    print()
    show_image_with_patterns(image)


image_name = "serif.png"
font_name = "LiberationSerif-Regular.ttf"
# image_name = "sans2.png"
# font_name = "LiberationSans-Regular.ttf"
start_size = 60
image_pattern_solution(repair_image(image_name), font_name, 0.94, fill_frame, start_size)
