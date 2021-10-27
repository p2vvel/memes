from PIL import Image


def compress_image(img: Image, width: int = 600) -> Image:
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