
# PYTESSERACT

from PIL import Image

import pytesseract

# Simple image to string
# -psm 10 is single character
# -oem 3 picks default model type
# -c whitelist gives the characters is can choose
name = "C_01"
result = pytesseract.image_to_string(Image.open("../Data/Image_" + name + ".png"), 
                                     config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOP0123456789')
print(result)


# EASYOCR 

# import easyocr

# reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
# result = reader.readtext('../Data/AImage.png')
# print(result)



# KERAS OCR 

# from PIL import Image 
# import matplotlib.pyplot as plt

# import keras_ocr

# # keras-ocr will automatically download pretrained
# # weights for the detector and recognizer.
# pipeline = keras_ocr.pipeline.Pipeline()

# image = Image.open('../Data/AImage.png')
# print(image)

# # Each list of predictions in prediction_groups is a list of
# # (word, box) tuples.
# prediction_groups = pipeline.recognize(image)

# # Plot the predictions
# fig, axs = plt.subplots(nrows=len(image), figsize=(20, 20))
# for ax, image, predictions in zip(axs, image, prediction_groups):
#     keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)