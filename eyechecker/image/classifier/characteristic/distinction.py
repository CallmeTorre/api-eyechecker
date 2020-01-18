def distinct_between_ma_ha(coordinates):
    hemorrages = dict()
    micro = dict()
    counter_micro = 0
    counter_hr = 0
    for key, value in coordinates.items():
        if len(value) >= 25:
            hemorrages[counter_hr] = value
            counter_hr += 1
        else:
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