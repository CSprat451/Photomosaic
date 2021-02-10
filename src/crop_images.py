import glob
from PIL import Image
import os

SOURCE_IMAGES_PATH = "images/*.jpeg"
SQUARE_SIZE = 20


def crop_source_images():
    """
    Takes a file folder of images, then resizes and crops the images
    down to SQUARE_SIZE pixels. A new results/source-images directory will
    be created if it is not already present.
    """
    source_images = glob.glob(SOURCE_IMAGES_PATH)
    img_thumbs = {}
    image_no = 1
    for source_image in source_images:
        with open(source_image, 'rb') as file:
            img = Image.open(file)
            width, height = img.size
            new_width, new_height = min(img.size), min(img.size)

            left = round((width - new_width) / 2)
            top = round((height - new_height) / 2)
            x_right = round(width - new_width) - left
            x_bottom = round(height - new_height) - top
            right = width - x_right
            bottom = height - x_bottom

            cropped_img = img.crop((left, top, right, bottom))

            img_thumb = cropped_img.resize((SQUARE_SIZE, SQUARE_SIZE), Image.ANTIALIAS)

            img_thumbs[source_image] = img_thumb

            path = os.path.dirname(os.getcwd())
            directory = os.path.join(path, "results", "source-images")

            if not os.path.exists(directory):
                os.makedirs(directory)

            source_image_filenames = os.path.join(path, "results", "source-images", str(image_no) + ".jpg")
            img_thumb.save(source_image_filenames, "JPEG")
            image_no += 1

    return img_thumbs


crop_source_images()
