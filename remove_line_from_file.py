from os import listdir
from os.path import isfile, join
from tqdm import tqdm

PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\riadh_andalos\\morning\\1"
files = [f for f in listdir(PATH) if ".txt" in f and f != "classes.txt"]

for fl in tqdm(files):
    with open(join(PATH, fl), "r") as f:
        lines = f.readlines()

    with open(join(PATH, fl), "w") as f:
        for line in lines:
            x = float(line.split(" ")[1])
            y = float(line.split(" ")[2])
            if not (( x <= 0.03) and ( y <= 0.2)):
                f.write(line)