from skimage import io
from skimage.transform import resize


def open_image(url: str):
    """"
    WARNING: This is going to create a temporal file
    """
    return io.imread(url)


def get_green_channel(rgb_image):
    # RGB values, each pixel is stored as 8-bit 3-channel color images (0 to 255)
    return rgb_image[:, :, 1]


def scale_image(image, normalized_height, normalized_width):
    # TODO: Check resize(preserve_range=False) argument
    width, height = image.shape
    if height != normalized_height or width != normalized_width:
        image = resize(image, (normalized_height, normalized_width))
    return image
