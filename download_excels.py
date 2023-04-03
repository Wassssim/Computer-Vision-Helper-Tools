import json
import os
import datetime
import requests
from os import listdir
from os.path import join, isdir, exists

input_abspath = "/media/rtxdeepstream/INTENSO1/LOT3/RGC OCTOBRE 2022-SEMAINE 1"
output_abs_path= "/media/rtxdeepstream/INTENSO1/LOT3/RGC OCTOBRE 2022-SEMAINE 1/Excels"
api_base_url = "http://ns3089849.ip-54-36-61.eu:3002/api"

sites = [ d for d in listdir(input_abspath) if isdir(join(input_abspath, d))]

# login
userData = {
    "username": "wassim",
    "password": "12345"
}
res = requests.post(f"{api_base_url}/user/login", headers={"Accept":"application/json"}, json=userData)
token = f"Bearer {res.json()['token']}"

def parse_date(dateStr):
    date = datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
    utc_date = date.astimezone(datetime.timezone.utc)
    iso_date = utc_date.strftime('%Y-%m-%dT%H:%M:%S')
    return iso_date


for site_dir in sites:
    site_dir_abspath = join(input_abspath, site_dir)
    
    site_id = -1
    config_file_abspath = join(site_dir_abspath, "config.json")
    if not (exists(config_file_abspath)):
        print("Skipping", site_dir_abspath)
        continue
    
    with open(config_file_abspath, "r") as cfg:
        site_id = json.load(cfg)["site_id"]
        res = requests.get(f"{api_base_url}/sites/{site_id}/planning", headers={"Accept":"application/json", "Authorization": token})
        plannings = res.json()["plannings"]

        outdir = join(output_abs_path, site_dir)
        if not (os.path.exists(outdir)):
            os.mkdir(outdir)
        
        for idx, planning in enumerate(plannings):
            begin_date = parse_date(planning["start_date"])
            end_date = parse_date(planning["end_date"])

            res = requests.get(f"{api_base_url}/sites/{site_id}/census-report/?beginDate={begin_date}&endDate={end_date}", headers={"Accept":"application/json", "Authorization": token})
            
            excel_filename = f'{site_dir}.xlsx' if idx == 0 else f'{site_dir} - {idx}.xlsx'

            with open(join(outdir, excel_filename), 'wb') as f:
                # Write the binary content of the response to the file
                f.write(res.content)
            
