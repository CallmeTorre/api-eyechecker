import numpy as np


def get_bright_regions(img):
    return (img > 130).astype(np.bool)
