from os import listdir
from os.path import isfile, join, getsize
from os import remove
import shutil

PATH = "C:\\Users\\Wass\\Documents\\Work\\filthy_data\\riadh_andalos\\noon\\1"
#BACKUP_PATH = "C:\\Users\\Wass\\Documents\\PFE\\filthy_data\\backup_plates"
file_names = [f for f in listdir(PATH) if isfile(join(PATH, f))]
images = [f for f in file_names if ".jpg" in f]
remove_files = True

#remove annotations with no content
empty_files = [f for f in file_names if getsize(join(PATH, f)) == 0]
annotations = [f for f in listdir(PATH) if isfile(join(PATH, f)) and ".txt" in f]
for f in empty_files:
    remove(join(PATH,f))

#remove annotations with no images
ghost_annotations = [f for f in annotations if f.replace(".txt", ".jpg") not in images]
annotations = [f for f in listdir(PATH) if isfile(join(PATH, f)) and ".txt" in f]
for f in ghost_annotations:
    remove(join(PATH,f))

#remove images with no annotations
ghost_images = [f for f in images if f.replace(".jpg", ".txt") not in annotations]
for f in ghost_images:
    if remove_files:
        remove(join(PATH,f))
    else:
        shutil.move(join(PATH,f), join(BACKUP_PATH,f))