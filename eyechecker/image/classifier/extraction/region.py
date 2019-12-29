import numpy as np
from scipy.ndimage import label


def get_coordinates_of_the_regions(binary_img):
    segmented_img_with_regions, num_regions = label(binary_img)
    lesions = np.nonzero(segmented_img_with_regions)
    coords = np.column_stack(lesions)
    non_zero_vals = segmented_img_with_regions[lesions[0], lesions[1]]
    coords_of_each_lesion = {k: coords[non_zero_vals == k] for k in range(1, num_regions + 1)}
    return coords_of_each_lesion
