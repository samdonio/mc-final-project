from predictImage import predict_character
import pandas as pd
from PIL import Image
import time
from utility import points_to_image

def class_to_character(class_label):
    if class_label < 0:
        return None 
    elif class_label < 10:
        return str(class_label)
    elif class_label < 36:
        return chr((class_label - 10) + ord('A'))
    else:
        return chr((class_label - 36) + ord('a'))
        
def csv_to_image(position_points, model):
    
    size = (28,28)
    image = points_to_image(position_points, size)
    result = predict_character(image, model)
    return class_to_character(result)

    
    
    