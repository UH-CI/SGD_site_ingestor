#!/usr/bin/env python
# coding: utf-8
import requests
import json
import urllib
import  urllib.parse
import pandas as pd
from subprocess import call
from pyproj import Proj, transform
from requests.auth import HTTPBasicAuth
token = 'APITOKEN'


df1 = pd.read_csv('SGD_sites.csv')
#set static json body values and permsissions
#users needs to exist in agave
body={}
pem1={}
pem1['username']= 'seanbc'
pem1['permission']='ALL'
pem2={}
pem2['username']= 'jgeis'
pem2['permission']='ALL'
pem4={}
pem4['username']= 'ikewai-admin'
pem4['permission']='ALL'
pem5={}
pem5['username']= 'public'
pem5['permission']='READ'

body['name'] = "Site"
#the schemaID value needs to match your Well schema object UUID in Agave
body['schemaId'] = "2206831229666127385-242ac1110-0001-013"

body['permissions']=[pem1,pem2,pem4,pem5]
#should loop through each dataframe row convert to json and modify to fit well schema
i=0

for i in df1.index:
    j = df1.loc[i].to_json()
    js = json.loads(j)
    #This stores a GeoJSON object in the value.loc field - in Ike Wai this has a spatial index on it in mongodb
    js['loc'] = {"type":"Point", "coordinates":[js['longitude'],js['latitude']]}
    body['value'] = js
    body['value']['id'] = js['name']
    body['value']['ikewai_type'] =['SGD']
    body['geospatial']= True;
    #write out our json to a file for use with the CLI command
    with open('sgd_sites/import-site'+str(i)+'.json', 'w') as outfile:
        json.dump(body, outfile)
    #call the CLI to add our well object
    call("./metadata-addupdate -z "+token+" -F sgd_sites/import-site"+str(i)+".json", shell=True)
