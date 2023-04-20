import os
import sys
import shutil
from subprocess import run
from os import listdir
from os.path import isdir, isfile, join

def listVideos(videoDir):
    return [f for f in listdir(videoDir) if isfile(join(videoDir, f)) and ".mp4" in f]


def moveVideos(srcDir, destDir):
    videos = listVideos(srcDir)
    for videoFilename in videos:
        videoAbspath = join(srcDir, videoFilename)
        shutil.move(videoAbspath, destDir)


def main():
    if len(sys.argv) < 2:
        print("[ERROR] Please provide an input path")
        sys.exit()

    input_path = (sys.argv[1]).replace("\\", "/")

    args={
        "input": input_path,
    }

    print("Videos Directories: ", args["input"])

    videoDirs = [d for d in listdir(args["input"]) if isdir(join(args["input"], d))]

    for videoDir in videoDirs:
        videoDirAbspath = join(args["input"], videoDir)
        rawDirAbspath = join(videoDirAbspath, "raw")

        # Check whether the specified path exists or not
        isExist = os.path.exists(rawDirAbspath)
        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(rawDirAbspath)
        
        print("The output directory is created")
        print("==> Converting:", join(args["input"], videoDir))
        command = ['python3', 'convert_videos.py', join(args["input"], videoDir)]
        result = run(command)
        if (result.returncode == 0):
            moveVideos(videoDirAbspath, rawDirAbspath)
        else:
            stop = False
            while (True):
                answer = input("ERROR in conversion command, continue? [y/n]")
                if (answer.upper() == "Y"):
                    break 
                elif (answer.upper() == "N"):
                    stop = True
                    break
            if (stop): 
                break



if (__name__ == '__main__'):
    main()