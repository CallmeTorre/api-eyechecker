import numpy as np
from scipy import stats
from skimage.util import img_as_ubyte

def get_bright_regions(img, green_channel):
    green_channel_u = img_as_ubyte(green_channel)
    imagen_to_be_colored = np.zeros_like(img)
    all_values = img.ravel()
    tr_values = all_values[np.logical_and(all_values>=0.045,all_values < 0.14)]
    all_zscores = stats.zscore(tr_values)
    look_up_table_z = dict(zip(tr_values, all_zscores))

    for row in range(len(img)):
        for col in range(len(img[0])):
            hue_val = img[row][col]
            green_value = green_channel_u[row][col]
            if green_value <= 35:
                continue
            if hue_val >= 0.045 and hue_val < 0.15:
                look_val_z = look_up_table_z[hue_val]
                if look_val_z >= 2.0:
                    imagen_to_be_colored[row][col] = 1
                else:
                    imagen_to_be_colored[row][col] = 0
            else:
                imagen_to_be_colored[row][col] = 0
    return imagen_to_be_colored