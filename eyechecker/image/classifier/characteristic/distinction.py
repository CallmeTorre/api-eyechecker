import numpy as np

def distinct_between_ma_ha(coordinates):
    hemorrages = dict()
    micro = dict()
    counter_micro = 0
    counter_hr = 0
    for key, value in coordinates.items():
        is_hemo = False
        is_micro = False
        min_x, min_y = value.min(axis=0)
        max_x, max_y = value.max(axis=0)
        area = len(value)
        roundness = 0.0
        
        if area >= 52:
            is_hemo = True
        else:
            if max_x > max_y: #x-axis roundness 
                roundness = (4*area)/(np.pi*(max_x-min_x+1)**2)
            else:
                roundness = (4*area)/(np.pi*(max_y-min_y+1)**2)
            
            if roundness >= 0.5:
                is_micro = True
            else:
                is_hemo = True

        if is_hemo:
            hemorrages[counter_hr] = value
            counter_hr += 1
        elif is_micro:
            micro[counter_micro] = value
            counter_micro += 1
            
    return micro, hemorrages

def distinct_betwen_disc_and_exudate(coordinates):
    hexudates = dict()
    counter_hexu = 0
    for key, value in coordinates.items():
        hexudates[counter_hexu] = value
        counter_hexu += 1
    return hexudates
