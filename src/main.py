from PIL import Image
import crop_images
import numpy as np
import glob
import uuid
import os

SOURCE_IMAGES_PATH = "../results/source-images/*.jpg"
SQUARE_SIZE = 10
INPUT_IMAGE = Image.open('spiderman.jpg')


def split_image(pixels, corner, square_size):
    """
    Splits the original image into equal squares.
    """
    opposite_corner = (corner[0] + square_size, corner[1] + square_size)

    square_rows = pixels[corner[0]:opposite_corner[0]]
    square = []
    for row in square_rows:
        square.append(row[corner[1]:opposite_corner[1]])

    return square


def get_pixel_matrix(image):
    """
    Converts an image into tuples with the R, G, B code in each tuple.
    returns: a 2D array of R, G, B tuples
    """
    pixel_matrix = np.asarray(image)

    return pixel_matrix


def get_color_average(pixels):
    r_total = 0
    g_total = 0
    b_total = 0
    n_pixels = 0
    for row in pixels:
        for p in row:
            r_total += p[0]
            g_total += p[1]
            b_total += p[2]

            n_pixels += 1

    return r_total / n_pixels, g_total / n_pixels, b_total / n_pixels


def get_mean_rgb_source(img_thumbnails):
    rgbs = {}
    for path, img in img_thumbnails.items():
        print("Processed %s" % path)
        thumbnail_pixels = get_pixel_matrix(img)
        rgbs[path] = get_color_average(thumbnail_pixels)
    return rgbs


def pythagoras_nearest_rgb(target_rgb, source_images_mean_rgbs):
    best_match_name = None
    best_match_color_difference = None
    for path, source_rgb in source_images_mean_rgbs.items():
        color_difference = pythagoras_color_difference(target_rgb, source_rgb)
        if best_match_color_difference is None or color_difference < best_match_color_difference:
            best_match_name = path
            best_match_color_difference = color_difference

    return best_match_name


def pythagoras_color_difference(p1, p2):
    tot = 0
    for c1, c2 in zip(p1, p2):
        tot += (c1 - c2) ** 2

    return tot ** 0.5


def save_mosaic():
    """
    Creates the mosaic image using the color information and grid produced from the original image.
    Output is a mosaic image using the resized and cropped source images from the "results/source-images" directory.
    The directory "results/mosaic" will be created if it does not already exist.
    """
    mosaic_image = Image.new('RGB', (target_image_width, target_image_height), (255, 255, 255))
    for x in range(0, target_image_width, SQUARE_SIZE):
        for y in range(0, target_image_height, SQUARE_SIZE):
            grid = split_image(pixels, (y, x), SQUARE_SIZE)
            avg_color = get_color_average(grid)
            best_match_thumbnail = pythagoras_nearest_rgb(avg_color, img_thumbs_mean_color)
            img_thumb_value = img_thumbnails.get(best_match_thumbnail)
            mosaic_image.paste(img_thumb_value, (x, y))

    unique_filename = str(uuid.uuid4()) + ".jpg"
    path = os.path.dirname(os.getcwd())
    directory = os.path.join(path, "results", "mosaic")

    if not os.path.exists(directory):
        os.makedirs(directory)

    mosaic_filepath = os.path.join(path, "results", "mosaic", unique_filename)
    mosaic_image.save(mosaic_filepath)
    mosaic_image.show()


target_image_width, target_image_height = INPUT_IMAGE.size
pixels = get_pixel_matrix(INPUT_IMAGE)

img_thumbnails = {}
if len(SOURCE_IMAGES_PATH) == 0:
    img_thumbnails = crop_images.crop_source_images()
else:
    for filename in glob.glob(SOURCE_IMAGES_PATH):
        image = Image.open(filename)
        img_thumbnails[filename] = image


img_thumbs_mean_color = get_mean_rgb_source(img_thumbnails)
grid = split_image(pixels, (0, 0), SQUARE_SIZE)
save_mosaic()
