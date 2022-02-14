import os
import sys
from os.path import join

base_dir = sys.argv[1]
files = os.listdir(base_dir)
annotations = [ann for ann in [f.replace(".jpg",".txt") for f in  files if ".jpg" in f] if ann in files]
annotation_map = {
    7:3, # truck
    2:1, # car
    3:0, # motorbike
    5:2 # bus
}

for annotation in annotations:
    with open(join(base_dir, annotation), "r") as f:
        lines = f.readlines()
        mapped_lines = []
        for box in lines:
            box_split = box.split(" ")
            class_id = int(box_split[0])
            if class_id in annotation_map:
                box_split[0] = str(annotation_map[class_id])
            else:
                box_split[0] = "5"
            mapped_lines.append(" ".join(box_split))
    with open(join(base_dir, annotation), "w") as f:
        for mapped_line in mapped_lines:
            f.write(mapped_line)
        