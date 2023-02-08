import sys
import os
from subprocess import call
from os import listdir
from os.path import isfile, join

if len(sys.argv) < 2:
    print("[ERROR] Please provide an input path")
    sys.exit()

input_path = (sys.argv[1]).replace("\\", "/")
file_name = os.path.splitext( os.path.basename(input_path))[0]

args={
    "input": input_path,
    "output": os.path.join(os.path.join( os.path.dirname(input_path), os.path.splitext( os.path.basename(input_path))[0]).replace("\\", "/"), "converted_vids")
}

print("Video Directory: ", args["input"])
print("Converted videos directory: ",args["output"])

# Check whether the specified path exists or not
isExist = os.path.exists(args["output"])

if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs(args["output"])
  print("The output directory is created")


videofiles = [f for f in listdir(args["input"]) if isfile(join(args["input"], f)) and ".mp4" in f]

for video in videofiles:
    print(join(args["input"], video))
    call(f'ffmpeg -i "{join(args["input"], video)}" -flags +global_header -vcodec copy -acodec copy "{join(args["output"], video)}"')

