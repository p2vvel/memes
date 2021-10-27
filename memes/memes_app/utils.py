from PIL import Image


def compress_image(img: Image, width: int = 600) -> Image:
    '''Returns resized image with given width, saves original aspect ratio'''
    aspect_ratio = img.width/img.height
    width, height = 600, round(600/aspect_ratio)   #new image size
    return img.resize((width, height))