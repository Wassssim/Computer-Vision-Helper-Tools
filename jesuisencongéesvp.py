import os
from os import listdir
from tqdm import tqdm 
import shutil

params = {
    "input": "/media/rtxdeepstream/ADATA_HD330/label/hiv00072_done/",
    "destination": "/media/rtxdeepstream/ADATA_HD330/label/filtered"
}

KEEP_ALL_CLASSES = True

labels = [ f for f in listdir(params["input"]) if os.path.splitext(f)[-1] == ".txt" and os.path.basename(f) != "classes.txt"]

shutil.copyfile(os.path.join(params["input"], "classes.txt"), os.path.join(params["destination"], "classes.txt"))
print(len(labels))

keep = 0

for label_file in tqdm(labels[:]):
    with open(os.path.join(params["input"], label_file), "r") as f:
        lines = f.readlines()
        for line in lines:
            if ((KEEP_ALL_CLASSES) or (int(line.strip().split()[0]) != 1)):
                # copy
                image_file = label_file.replace(".txt", ".jpg")
                src = os.path.join(params["input"], label_file)
                dest = os.path.join(params["destination"], label_file)
                shutil.copyfile(src, dest)
                src = os.path.join(params["input"], image_file)
                dest = os.path.join(params["destination"], image_file)
                shutil.copyfile(src, dest)
                break

print(keep)


            