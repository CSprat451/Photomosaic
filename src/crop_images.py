import glob
from PIL import Image
import os

source_images_link = "Images/*.jpg"
square_size = 20


def crop_source_images():
    source_images = glob.glob(source_images_link)
    # img_thumbs = {}
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

            img_thumb = cropped_img.resize((square_size, square_size), Image.LANCZOS)
            # img_thumbs[source_image] = img_thumb
            name = 'C:/Users/Shane/PycharmProjects/Robert-Heaton-Projects/Photomosaics/Cropped-Images/cropped-' \
                   + str(image_no) + '.jpg'
            img_thumb.save(name, 'JPEG')
            image_no += 1


crop_source_images()
