from utility import csv_to_image
from imageToText import tesseract

count = 0 
for i in range(26):
    currChr = chr(ord('A') + i)
    name = chr(ord('A') + i) + "_01"
    size = (28, 28)

    csv_path = "../Data/" + name + ".csv"
    image = csv_to_image(csv_path, size)
    image.save("../Data/Image_" + name + ".png")

    result = tesseract(name)
    if len(result) > 0 and result[0] == currChr:
        count += 1
        print("Correctly identified " + currChr)
    else:
        print("Incorrectly identified " + currChr)

print("Accuracy: ",count, "/", 26)

