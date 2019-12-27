import numpy as np
from numba import jit
from scipy import ndimage as ndi
from skimage.morphology import disk


def fill_holes(binary_image):
    return ndi.binary_fill_holes(binary_image).astype(np.float)


@jit(nopython=True)
def dilatation(DATA, image_cols, image_rows, MASK):
    FILTER = np.zeros(len(DATA))
    size_of_structure = len(MASK)
    for structure_row in range(size_of_structure // 2, image_rows - size_of_structure // 2):
        for structure_col in range(size_of_structure // 2, image_cols - size_of_structure // 2):
            smax = 0.0
            for image_row in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                for image_col in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                    if MASK[image_col + size_of_structure // 2][image_row + size_of_structure // 2]:
                        if DATA[structure_col + image_col + (structure_row + image_row) * image_cols] > smax:
                            smax = DATA[structure_col + image_col + (structure_row + image_row) * image_cols]
            FILTER[structure_col + structure_row * image_cols] = smax
    return FILTER


@jit(nopython=True)
def erosion(DATA, image_cols, image_rows, MASK):
    FILTER = np.zeros(len(DATA))
    size_of_structure = len(MASK)
    for structure_row in range(size_of_structure // 2, image_rows - size_of_structure // 2):
        for structure_col in range(size_of_structure // 2, image_cols - size_of_structure // 2):
            smin = 255.0
            for image_row in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                for image_col in range(-(size_of_structure // 2), size_of_structure // 2 + 1):
                    if MASK[image_col + size_of_structure // 2][image_row + size_of_structure // 2]:
                        if DATA[structure_col + image_col + (structure_row + image_row) * image_cols] < smin:
                            smin = DATA[structure_col + image_col + (structure_row + image_row) * image_cols]
            FILTER[structure_col + structure_row * image_cols] = smin
    return FILTER


def opening(DATA):
    MASK = disk(3)
    image_rows, image_cols = DATA.shape
    DATA = DATA.flatten()
    FILTER = erosion(DATA, image_cols, image_rows, MASK)
    FINAL = dilatation(FILTER, image_cols, image_rows, MASK)
    return np.reshape(FINAL, (-1, image_cols))


def opening2(DATA):
    print("THJIS IS DSAFDS")
    return ndi.binary_opening(DATA, structure=disk(3))
