import glob
import os
import subprocess
import argparse
import json

from datetime import datetime, timedelta

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


def parse_args():
    parser = argparse.ArgumentParser(description='Create timestamps for an alphabetically ordered set of videos')
    parser.add_argument('-t', help='begin date for the first video')
    parser.add_argument('-d', help='videos directory')
    #parser.add_argument('--set_generic', help='sets the generic models', nargs='?', type=int, default=0, const=0)

    args = parser.parse_args()

    return args


params = parse_args()
start_date = datetime.strptime(params.t, '%m-%d-%Y %a %H:%M:%S')
base_dir = params.d
correction_factor = 0.027

# Get list of all files in a given directory sorted by name
list_of_files = sorted( filter( os.path.isfile,
                        glob.glob(os.path.join(base_dir, '*')) ) )



for file_abspath in list_of_files:
    length = get_length(file_abspath) - correction_factor
    end_date = start_date + timedelta(milliseconds=length*1000)
    print("-"*50)
    print(file_abspath)
    print(length)
    print(f"{int(length)//60}:{int(length)%60}")
    print("Start Date:", start_date)
    print("End Date:", end_date)
    file_name = os.path.basename(file_abspath)
    json_file_name = "".join(list(os.path.splitext(file_name)[:-1]) + [".json"])
    metadata_dict = {
        "video_file_name": file_name,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    
    with open(os.path.join(base_dir, json_file_name), "w") as f:
        json.dump(metadata_dict, f, indent=2)
    
    start_date = end_date