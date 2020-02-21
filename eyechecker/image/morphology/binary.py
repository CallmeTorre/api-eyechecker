import numpy as np
from numba import jit
from scipy import ndimage as ndi
from skimage.morphology import disk


def fill_holes(binary_image):
    return ndi.binary_fill_holes(binary_image).astype(np.bool)


@jit(nopython=True)
def dilatation(img, image_cols, image_rows, mask):
    binary_img = np.zeros(len(img))
    size_of_structure = len(mask)
    for structure_row in range(size_of_structure // 2, image_rows - size_of_structure // 2):
        for structure_col in range(size_of_structure // 2, image_cols - size_of_structure // 2):
            smax = 0.0
            for image_row in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                for image_col in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                    if mask[image_col + size_of_structure // 2][image_row + size_of_structure // 2]:
                        if img[structure_col + image_col + (structure_row + image_row) * image_cols] > smax:
                            smax = img[structure_col + image_col + (structure_row + image_row) * image_cols]
            binary_img[structure_col + structure_row * image_cols] = smax
    return binary_img


@jit(nopython=True)
def erosion(img, image_cols, image_rows, mask):
    binary_img = np.zeros(len(img))
    size_of_structure = len(mask)
    for structure_row in range(size_of_structure // 2, image_rows - size_of_structure // 2):
        for structure_col in range(size_of_structure // 2, image_cols - size_of_structure // 2):
            smin = 255.0
            for image_row in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                for image_col in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                    if mask[image_col + size_of_structure // 2][image_row + size_of_structure // 2]:
                        if img[structure_col + image_col + (structure_row + image_row) * image_cols] < smin:
                            smin = img[structure_col + image_col + (structure_row + image_row) * image_cols]
            binary_img[structure_col + structure_row * image_cols] = smin
    return binary_img


def opening(img):
    mask = disk(1)
    image_rows, image_cols = img.shape
    eroded_img = erosion(img.flatten(), image_cols, image_rows, mask)
    opened_img = dilatation(eroded_img, image_cols, image_rows, mask)
    return np.reshape(opened_img, (-1, image_cols)).astype(np.bool)


def opening_l(img):
    return ndi.binary_opening(img, structure=disk(1))


def remove_border(img, borders):
    return np.bitwise_xor(img, borders)
