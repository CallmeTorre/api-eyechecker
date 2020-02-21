import numpy as np 

def grade_lesion(ma, hr, he):
    total_ma = np.count_nonzero(ma == 1)
    total_he = np.count_nonzero(hr == 1)
    total_hr = np.count_nonzero(he == 1)
    
    if total_ma <= 20:
        total_ma = 0
    if total_he <= 5:
        total_he = 0
    if total_hr <= 5:
        total_hr = 0
        
    all_final_lessions = [total_ma, total_he, total_hr]
    print(all_final_lessions)
    
    #It means has grade 0
    if not np.any(all_final_lessions):
        return "Imagen Sana"
    elif not np.all(all_final_lessions):
        return "Retinopatia Diabetica No Proliferativa Temprana"
    else:
        return "Retinopatia Diabetica No Proliferativa Moderada"
    