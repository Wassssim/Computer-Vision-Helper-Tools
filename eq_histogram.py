import cv2
from os import listdir
from os.path import isfile, join
import numpy as np

PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\FB_scraper_data"
image_names = [f for f in listdir(PATH) if isfile(join(PATH, f)) and ".jpg" in f]

for im in image_names:
    print(im)
    image = cv2.imread(join(PATH, im))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    numpy_horizontal_concat = np.concatenate((gray, equalized), axis=1)
    cv2.imshow("normal", image)
    cv2.imshow("equalized", equalized)
    #cv2.imshow("test", numpy_horizontal_concat)
    cv2.waitKey(0)

cv2.destroyAllWindows()