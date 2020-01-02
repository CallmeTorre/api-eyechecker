import numpy as np


def get_bright_regions(img):
    return (img > 100).astype(np.bool)
