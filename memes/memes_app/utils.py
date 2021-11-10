from io import BytesIO
from PIL import Image, ImageSequence
from django.conf import settings
from django.core.files.base import File
from django.db.models.fields.files import ImageField


#global variable, dont want to load watermark every time that someone uploads meme
watermark = Image.open(settings.BASE_DIR / "static" / "images" / "watermark_small.png")


def resize_image(img: Image, width: int = 600) -> Image:
    '''Returns resized image with given width, saves original aspect ratio'''
    aspect_ratio = img.width/img.height
    width, height = 600, round(600/aspect_ratio)   #new image size
    return img.resize((width, height))


def add_watermark(image: Image, watermark: Image) -> None:
    '''Pastes watermark to the bottom right corner of given image'''
    i_s = image.size
    w_s = watermark.size
    box = (i_s[0]-w_s[0], i_s[1]-w_s[1])
    image.paste(watermark, box, watermark)

def get_normal_image(image: ImageField) -> File:
    '''Resizes original image and adds watermark'''
    img = Image.open(image)
    buffer = BytesIO()

    if img.format in ("PNG", "JPEG"):
        new_image = resize_image(img, 600)
        add_watermark(new_image, watermark) #watermark = global variable
        new_image.save(buffer, format=img.format)
    elif img.format == "GIF":
        frames = [resize_image(k, 600).convert("RGBA") for k in ImageSequence.Iterator(img)]
        for k in frames: add_watermark(k, watermark)
        if len(frames) > 1:
            frames[0].save(buffer, format=img.format, save_all=True, append_images=frames[1:])
        else:
            frames[0].save(buffer, format=img.format)

    return File(buffer, name=image.name)