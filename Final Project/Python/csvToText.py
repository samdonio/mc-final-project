from utility import csv_to_image
from imageToText import tesseract
from googleVision import classify_image

count = 0 
for i in range(26):
    currChr = chr(ord('A') + i)
    name = chr(ord('A') + i) + "_01"
    size = (64, 64)

    csv_path = "../Data/Upsampled/" + name + ".csv"
    image = csv_to_image(csv_path, size)
    image.save("../Data/UpsampledImages/Image_" + name + ".png")

    result = classify_image("../Data/UpsampledImages/Image_" + name + ".png")
    # result = tesseract(name)

    if len(result) > 0 and result[0] == currChr:
        count += 1
        print("Correctly identified " + currChr)
    else:
        print("Incorrectly identified " + currChr)

print("Accuracy: ",count, "/", 26)

