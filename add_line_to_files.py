from os import listdir
from os.path import isfile, join
from tqdm import tqdm

PATH = "D:\\Final\\other\\TODO"
files = [f for f in listdir(PATH) if ".txt" in f]

for fl in tqdm(files):
    if "classes" in fl:
        continue
    with open(join(PATH, fl), "r") as f:
        lines = f.readlines()
    with open(join(PATH, fl), "w") as f:
        for line in lines:
            #if line in "\n1 0.133224 0.185673 0.059211 0.073099\n1 0.181743 0.168129 0.041118 0.061404\n1 0.218750 0.149123 0.042763 0.052632\n":
            #    continue
            if line == '\n':
                continue
            if line != '\n':
                f.write(line.strip() + "\n")
        f.write("1 0.164844 0.454167 0.043750 0.050000\n1 0.196094 0.443056 0.034375 0.044444\n1 0.223047 0.434028 0.032031 0.043056\n1 0.247266 0.418056 0.030469 0.047222\n1 0.269922 0.417361 0.016406 0.037500\n1 0.288672 0.409028 0.024219 0.031944\n1 0.312891 0.397917 0.022656 0.031944")