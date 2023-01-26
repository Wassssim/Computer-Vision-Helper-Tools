import cv2
from os import listdir
from os.path import isfile, join
from time import sleep
from tqdm import tqdm

PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\EL KHADHRA AFTERNOON - Copy"

images = [f for f in listdir(PATH) if isfile(join(PATH,f)) and ".jpg" in f]
#print(join(PATH,"xd.jpg"))
crop_box_h = 0.95 #crop a (crop_size X crop_size) box
crop_box_w = 1

for image in tqdm(images[:]):
    im = cv2.imread(join(PATH, image))
    h, w, _  = im.shape
    im_cropped = im[h - int(crop_box_h*h):, : int(crop_box_w*w)]
    with open(join(PATH,image.replace(".jpg", ".txt")), "r") as f:
        boxes = f.readlines()
    with open(join(PATH,image.replace(".jpg", ".txt")), "w") as f:
        for line in boxes:
            line_arr = line.split(" ")
            if (float(line_arr[1]) + float(line_arr[3])/2 < crop_box_w) and ((float(line_arr[2]) - float(line_arr[4])/2) >= (1 - crop_box_h)):
                line_arr[1] = str((float(line_arr[1])*w)/int(w*crop_box_w))
                line_arr[3] = str((float(line_arr[3])*w)/int(w*crop_box_w))
                #print(line_arr[2])
                line_arr[2] = str((float(line_arr[2]) - (1 - crop_box_h))*h/int(h*crop_box_h))
                #print(line_arr[2])
                #line_arr[2] = str((float(line_arr[2]) - (1 - crop_box_h))*h/int(h*crop_box_h)) 
                line_arr[4] = str(float(line_arr[4])*h/int(h*crop_box_h)) 
                f.write(" ".join(line_arr))

    cv2.imwrite(join(PATH, image), im_cropped)
    cv2.imshow("xd", cv2.resize(im_cropped, (608,608)))
    #cv2.imshow("xd", im_cropped)
    #break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #cv2.imwrite("", im_cropped)