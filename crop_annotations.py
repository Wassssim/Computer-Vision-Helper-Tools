from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import cv2

PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\FB_scraper_data"
OUT_PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\backup_plates"
file_names = [f for f in listdir(PATH) if isfile(join(PATH, f))]
images = [f for f in file_names if ".jpg" in f]

for im in tqdm(images[:]):
    im_mat = cv2.imread(join(PATH, im))
    h, w, _ = im_mat.shape
    with open(join(PATH, im.replace(".jpg", ".txt")), "r") as f:
        lines = f.readlines()
        index = 0
        for line in lines:
            index += 1
            bbox = line.strip().split(" ")[1:]
            bbox_h = int(float(bbox[3]) * h)
            bbox_w = int(float(bbox[2]) * w)
            bbox_x = int(float(bbox[0]) * w) - int(bbox_w/2)
            bbox_y = int(float(bbox[1]) * h) - int(bbox_h/2)
            
            plate = im_mat[bbox_y: bbox_y + bbox_h, bbox_x:bbox_x + bbox_w]
            #cv2.imshow("original", im_mat)
            #cv2.imshow("xd", plate)
            cv2.imwrite(join(OUT_PATH, im.replace(".jpg", str(index) + ".jpg")), plate)
            cv2.waitKey(0)

