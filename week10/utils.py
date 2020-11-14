import numpy as np

def normalizeRads(angle_in_rads, decimals=4):
    return np.around(np.arctan2(np.sin(angle_in_rads), np.cos(angle_in_rads)), decimals=decimals)
    
def normalizeAngle(angle_in_degrees, decimals=4):
    angle_in_rads = angle_in_degrees * np.pi/180.
    normalized_rads = normalizeRads(angle_in_rads, decimals)
    return normalized_rads*180/np.pi

