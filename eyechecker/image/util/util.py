import numpy as np
from skimage import io
from skimage.transform import resize
from skimage.viewer import ImageViewer


def open_image(url: str):
    # It returns a numpy array
    return io.imread(url)


def get_green_channel(rgb_image):
    # RGB values, each pixel is stored as 8-bit 3-channel color images (0 to 255)
    return rgb_image[:, :, 1]


def scale_image(img, normalized_height: int, normalized_width: int):
    # Scales the image to (normalized_height, normalized_width) when necessary
    width, height, _ = img.shape
    if height != normalized_height or width != normalized_width:
        img = resize(img, (normalized_height, normalized_width))
    return img


def paint_lesions(img, lesions, coordinates):
    # It paints the lesion in the original image
    binary_img = np.zeros((1152, 1500), dtype=int)
    for i, l in enumerate(lesions):
        if l == 1:
            topaint = coordinates[i]
            for x, y in topaint:
                binary_img[x][y] = 1
    """
    rr, cc = polygon_perimeter(lesions, shape=img.shape, clip=True)
    img[rr, cc] = 1
    """
    return binary_img.astype(bool)


def view_image(image):
    # IO helper method to visualize the image
    viewer = ImageViewer(image)
    viewer.show()
