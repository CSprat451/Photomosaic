from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import glob


def split_image(pixels, corner, square_size):
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


def crop_source_images():
    source_images = glob.glob(source_images_link)
    img_thumbs = {}
    for source_image in source_images:
        with open(source_image, 'rb') as file:
            img = Image.open(file)

            img_thumb = img.resize((square_size, square_size), Image.LANCZOS)

            img_thumbs[source_image] = img_thumb
    return img_thumbs


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


source_images_link = "10pxCropped-Images/*.jpg"
square_size = 10
input_image = Image.open('fireworks.jpeg')
target_image_width, target_image_height = input_image.size
pixels = get_pixel_matrix(input_image)
img_thumbnails = crop_source_images()
img_thumbs_mean_color = get_mean_rgb_source(img_thumbnails)
grid = split_image(pixels, (0, 0), square_size)


mosaic_image = Image.new('RGB', (target_image_width, target_image_height), (255, 255, 255))

for x in range(0, target_image_width, square_size):
    for y in range(0, target_image_height, square_size):
        grid = split_image(pixels, (y, x), square_size)
        avg_color = get_color_average(grid)
        best_match_thumbnail = pythagoras_nearest_rgb(avg_color, img_thumbs_mean_color)
        img_thumb_value = img_thumbnails.get(best_match_thumbnail)
        mosaic_image.paste(img_thumb_value, (x, y))

mosaic_image.save("mosaic.jpg")
mosaic_image.show()
