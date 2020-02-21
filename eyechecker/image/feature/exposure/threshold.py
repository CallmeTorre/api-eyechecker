import numpy as np
from scipy import stats
from skimage.util import img_as_ubyte

def get_bright_regions(img_hue, green_channel):

    green_channel_u = img_as_ubyte(green_channel)
    all_values = img_hue.ravel()
    
    tr_values = all_values[np.logical_and(all_values >= 0.045,all_values < 0.15)]
    all_zscores = stats.zscore(tr_values)
    look_up_table_z = dict(zip(tr_values, all_zscores))
    look_up_table_z[-10] = -1
    
    values_in_hue_range = np.where(np.logical_and(all_values >= 0.045,all_values < 0.15), 
                                   all_values,
                                   -10)
    values_above_z = np.vectorize(look_up_table_z.get)(values_in_hue_range)
    binary_values = np.where(values_above_z >= 2.0, 
                                   True,
                                   False)
    
    binary_values = binary_values.reshape((1152, 1500)) 
    green_values_above = green_channel_u >= 35
    bright_image = np.logical_and(binary_values, green_values_above)
    
    return bright_image