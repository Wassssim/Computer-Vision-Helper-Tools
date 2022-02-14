from os import listdir
from os.path import isfile, join
from PIL import Image as PImage
from tqdm import tqdm

DATA_PATH = "C:\\Users\\Wass\\Documents\\PFE\\datasets\\tunisian-plates-fb-ifminfo"
ANNOTATION_FILES = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f)) and ".txt" in f]

def deconvert(annbox, w, h):
    ox = float(annbox[0])
    oy = float(annbox[1])
    ow = float(annbox[2])
    oh = float(annbox[3])
    x = ox*w
    y = oy*h
    w = ow*w
    h = oh*h
    xmax = (((2*x)+w)/2)
    xmin = xmax-w
    ymax = (((2*y)+h)/2)
    ymin = ymax-h
    return [int(xmin),int(ymin),int(xmax),int(ymax)]

def arr_sum(arr):
    s = 0
    for elt in arr:
        s += elt
    return s

for filename in tqdm(ANNOTATION_FILES[:]):
    #print(filename)
    img = PImage.open(DATA_PATH + "\\" + filename.replace(".txt", ".jpg"))
    curimg_w, curimg_h = img.size
    with open(DATA_PATH + "\\" + filename) as f:
        lines = f.readlines()
        for line in lines:
            if len(line)==1:
                lines.remove(line)
        for line_index in range(len(lines)):
            lines[line_index] = list(lines[line_index].replace("\n", "").split(" "))
            for j in range(len(lines[line_index])):
                    lines[line_index][j] = float(lines[line_index][j])
            #sum = 0
            #for num in lines[line_index][1:]:
            #    sum += num
            #lines[line_index] = sum*100
        #lines = np.array(lines, np.float)
        #print(lines.shape)
        mins = []
        for i in range(len(lines)):
            line = lines[i]
            #print("-------------------------------------------------------------------------------")
            sum = arr_sum(deconvert(line[1:], curimg_w, curimg_h))
            line[0] = int(line[0])
            min_id = None
            min = None
            for j in range(len(lines)):
                line1 = lines[j]
                sum1 = arr_sum(deconvert(line1[1:], curimg_w, curimg_h))
                diff = abs(sum1 - sum)
                #print(line1)
                if diff < 9 and i!=j:
                    #print (diff, " <---------" )
                    if not min_id or (min_id and diff < min):
                        min_id = j
                        min = diff
                    #lines.remove(line1)
                #else:
                    #print(diff)
            if min_id and min_id > i:
                mins.append(min_id)
        #print("MIN INDEXES: ", mins)
        mins.sort(reverse=True)
        mins = list(dict.fromkeys(mins))
        #print(mins)
        for min in mins:
            lines.remove(lines[min])
        #lines = lines[np.argsort(lines[:, 0])]
        for line_index in range(len(lines)):
            st = " "
            lines[line_index] = st.join(map(str, lines[line_index]))
        #print(lines)
        
    with open(DATA_PATH + "\\" + filename, "w") as f:
        for line in lines:
            f.write(line+"\n")