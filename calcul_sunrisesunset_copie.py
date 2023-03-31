import datetime
from suntime import Sun
from geopy.geocoders import Nominatim
from moviepy.editor import *
import glob
import os
import subprocess
import argparse
import json
import os, json
import pandas as pd
import shutil
from datetime import datetime, timedelta
from os.path import basename
import mysql.connector
from pandas import DataFrame
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='splitting videos into day and night directories')
    parser.add_argument('-t', help='date of the day ')
    parser.add_argument('-d', help='videos directory')
    #parser.add_argument('--set_generic', help='sets the generic models', nargs='?', type=int, default=0, const=0)

    args = parser.parse_args()

    return args

params = parse_args()
#time_zone = datetime.date(params.t)
time_zone = datetime.strptime(params.t,'%Y%m%d').date()
dir = params.d
 
# Nominatim API to get latitude and longitude
geolocator = Nominatim(user_agent="geoapiExercises")
 
# input place
place = "tunis"
location = geolocator.geocode(place)
 
# latitude and longitude fetch
latitude = location.latitude
longitude = location.longitude
sun = Sun(latitude, longitude)
 
# date in your machine's local time zone
#time_zone = datetime.date(2022,11,16)
sun_rise = sun.get_local_sunrise_time(time_zone)
sun_dusk = sun.get_local_sunset_time(time_zone)
sun_rise_iso= sun_rise.isoformat()
sun_dusk_iso= sun_dusk.isoformat()
print(sun_rise_iso)
c=[]
d=[]


    
c.append(sun_rise_iso[11])
c.append(sun_rise_iso[12])
print( "sunrise",c)
res1 = int("".join(c))
print(res1)

d.append(sun_dusk_iso[11])
d.append(sun_dusk_iso[12])
print( "sunset",d)
res2 = int("".join(d))
print(res2)
            
      
#print(sun_dusk_iso)




dir='D:/P05 NABEUL R42 PK 22.5 SECTION 42004'
######################################################################
os.chdir(dir)
files= os.listdir(dir)
print("1",files[0])
with open(files[0], 'r') as f:
                data = json.load(f)
print("2",(data["start_date"][0:10]))
#########################################
tata=[]
tata.append(data["start_date"][0:10])
print(tata)



new_path = dir+"/"+"Day"
print(new_path)
os.mkdir(new_path)

new_path1 = dir+"/"+"Night"+"/"
print(new_path1)
os.mkdir(new_path1)

new_path2 = dir+"/"+"config"+"/"
print(new_path2)
os.mkdir(new_path2)



for i in range (len(files)):
       # print(files[i])
        if (files[i].endswith(".json")):
            #print(files[i])
            
            
            with open(files[i], 'r') as f:
                data = json.load(f)
            print("3",data["start_date"][0:10])
            
            break
     





os.chdir(dir)
files= os.listdir(dir)
for i in range (len(files)):
       # print(files[i])
        if (files[i].endswith(".json")):
            #print(files[i])
            
            
            with open(files[i], 'r') as f:
                data = json.load(f)
            print(data["start_date"])
            print(data["start_date"][12])
            a=[]
            a.append(data["start_date"][11])
            a.append(data["start_date"][12])
            print(a)
            res = int("".join(a))
            print(res)
            if res <= res1: 
                print ("night") 
                print(files[i])
                shutil.move(files[i],new_path1)
                
                
            elif  res1<res<res2:
                print("day")
                print(files[i])
                shutil.move(files[i],new_path)
              
                
            elif res>=res2:
                print("night")
                print(files[i])
                shutil.move(files[i],new_path1)

for i in range (len(files)):
    if (files[i].endswith(".mp4")):
         #print(files[i])
                 
         #shutil.move(files[i],new_path)
         #index =files[i].rfind(".")
         #in2=files[i][:index]
         os.chdir(new_path1)
         files1= os.listdir(new_path1)
         for j in range (len(files1)):
           # print(files1[j])
            if (files1[j].split('.')[0] == files[i].split('.')[0]):
                print("hello")
                
                shutil.move("D:/P05 NABEUL R42 PK 22.5 SECTION 42004"+"/"+files[i],new_path1)
        
         os.chdir(new_path)
         files1= os.listdir(new_path)
         for j in range (len(files1)):
            # print(files1[j])
            
            if (files1[j].split('.')[0] == files[i].split('.')[0]):
                print("hello")
                shutil.move("D:/P05 NABEUL R42 PK 22.5 SECTION 42004"+"/"+files[i],new_path)
            #index1 =files1[j].rfind(".")
            #in1=files1[j][:index]
            #print(in1)
            #if in1==in2:
                #print(files[i])

            
         
         #new_string = files[i].replace(".mp4", ".json" )
         #print(new_string)

#connexion base de données


print(dir)
last = dir.rsplit(' ', 1)[-1]




db=mysql.connector.connect(
   host="ns3089849.ip-54-36-61.eu",
   port="3306",
   user="root",
   passwd="example",
   database="census_2022_prod",
   
)
cursor = db.cursor()
find = """SELECT id   FROM  `sites` WHERE  id>999 AND   n_sections  =%s"""
cursor.execute(find , (last,))
data = cursor.fetchall()
data1=data[0][0]
print(data1)
#query = ("SELECT id   FROM  `census_plannings` WHERE   n_sections  =? " %last)
#query = """SELECT id   FROM  `census_plannings` WHERE   n_sections  =%s"""
#cursor.execute(sql_Delete_query, (empId,))
#df = pd.read_sql(query, con = db)
#print(df)


find1 = """SELECT id , start_date   FROM  `census_plannings` WHERE     site_id  =%s""" 
cursor.execute(find1 , (data1,))
data2 = cursor.fetchall()
print(data2)
for lettre in data2:
    print(lettre[1].strftime("%Y-%m-%d"))

    if (lettre[1].strftime("%Y-%m-%d")==tata[0]):
        aDict = {"site_id":data1, "plannig_id":lettre[0]}
        jsonString = json.dumps(aDict)
        jsonFile = open("D:/P05 NABEUL R42 PK 22.5 SECTION 42004/config/data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
#data5=data2[0][1]

#print(data5.strftime("%Y-%m-%d"))

