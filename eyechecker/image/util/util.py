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


def view_image(image):
    # IO helper method to visualize the image
    viewer = ImageViewer(image)
    viewer.show()


def paint_lesions(img, lesions):
    # It paints the lesion in the original image
    for l in lesions:
        if l == 1:
            print("Something")
    print("Finished")
    """
    rr, cc = polygon_perimeter(lesions, shape=img.shape, clip=True)
    img[rr, cc] = 1
    """
    return img
