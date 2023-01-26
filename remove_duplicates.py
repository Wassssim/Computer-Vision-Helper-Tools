from os import listdir
from os.path import isfile, join, getsize
from os import remove
import shutil

PATH = "C:\\Users\\Wass\\Documents\\PFE\\videos\\ch01_00000000042000000"
#BACKUP_PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\backup_plates"
#file_names = [f for f in listdir(PATH) if isfile(join(PATH, f))]
#images = [f for f in file_names if ".jpg" in f]
remove_files = True

#remove annotations with no content
#empty_files = [f for f in file_names if getsize(join(PATH, f)) == 0]
annotations = [f for f in listdir(PATH) if isfile(join(PATH, f)) and ".txt" in f]
#images = [f.replace() for f in annotations]
for i in range(len(annotations) - 1):
    f = annotations[i]
    f1 = annotations[i+1]
    with open(join(PATH, f), 'r') as file1:
        with open(join(PATH, f1), 'r') as file2:
            same = set(file1).intersection(file2)
    if len(same) > 0:
        remove(join(PATH,f))
        remove(join(PATH,f.replace(".txt", ".jpg")))
