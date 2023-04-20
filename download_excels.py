import os
import sys
import json
import datetime
import requests
from os import listdir
from os.path import join, isdir, exists

api_base_url = "http://ns3089849.ip-54-36-61.eu:3002/api"


def parse_date(dateStr):
    date = datetime.datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
    utc_date = date.astimezone(datetime.timezone.utc)
    iso_date = utc_date.strftime('%Y-%m-%dT%H:%M:%S')
    return iso_date


def prompt_credentials():
    username = input("Username: ")
    password = input("Password: ")
    return {
        "username": username,
        "password": password
    }


def get_token(user_credentials):
    res = requests.post(f"{api_base_url}/user/login", headers={"Accept":"application/json"}, json=user_credentials)
    res.raise_for_status()
    return f"Bearer {res.json()['token']}"


def generate_excel(planning, token, outdir, filename, idx = 0):
    begin_date = parse_date(planning["start_date"])
    end_date = parse_date(planning["end_date"])

    res = requests.get(f"{api_base_url}/sites/{planning['site_id']}/census-report/?beginDate={begin_date}&endDate={end_date}", headers={"Accept":"application/json", "Authorization": token})
    
    excel_filename = f'{filename}.xlsx' if idx == 0 else f'{filename} - {idx}.xlsx'

    with open(join(outdir, excel_filename), 'wb') as f:
        # Write the binary content of the response to the file
        f.write(res.content)


def main():
    input_abspath = sys.argv[1]
    output_abs_path= input_abspath

    sites = [ d for d in listdir(input_abspath) if isdir(join(input_abspath, d))]

    # login
    user_credentials = prompt_credentials()
    token = get_token(user_credentials)

    for site_dir in sites:
        site_dir_abspath = join(input_abspath, site_dir)
        outdir = join(output_abs_path, site_dir)

        site_id = -1
        config_file_abspath = join(site_dir_abspath, "config.json")
        if not (exists(config_file_abspath)):
            print("Skipping", site_dir_abspath)
            continue
        
        with open(config_file_abspath, "r") as cfg:
            config = json.load(cfg)

            planning_id = config.get("planning_id")
            site_id = config.get("site_id")

            if (planning_id):
                res = requests.get(f"{api_base_url}/planning/{planning_id}", headers={"Accept":"application/json", "Authorization": token})
                planning = res.json()["planning"]
                generate_excel(planning, token, outdir, site_dir)
            elif (site_id): 
                res = requests.get(f"{api_base_url}/sites/{site_id}/planning", headers={"Accept":"application/json", "Authorization": token})
                plannings = res.json()["plannings"]

                #if not (os.path.exists(outdir)):
                #    os.mkdir(outdir)
                
                for idx, planning in enumerate(plannings):
                    generate_excel(planning, token, outdir, site_dir, idx)
            else:
                print(f"Error: invalid config file for {site_dir}")

if (__name__ == "__main__"):
    if (len(sys.argv) < 2):
        print("Please provide a site directory")
        sys.exit()
    
    main()