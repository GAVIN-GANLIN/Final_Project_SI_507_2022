######### This is final project of SI 507 #########
############# Uniqname: gavincgl ##################
############# Student ID: 08807131 ################
import json
import numpy as np
import re
import requests
import matplotlib
import googlemaps
#Collecting data from Yelp
Yelp_key ='dmnWf3eh1fIcD3Tqf-mP1plm3MLHF2iE27BhYd3h4FbfXcFMczG5Oy99RXIa4xJ58IP-0DOIuJxr4ZTeLIy6TVlq6gLOwKZXi7ZgjiOVsXf9k5OlYzzNJY18Gq9XYnYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
HEADERS = {'Authorization': 'Bearer %s' % Yelp_key}
TERM = 'recreation'
LOCATION = 'New York, NY'
def get_Yelp_Data (api_host,search_path,headers,term,location):
    data_Yelp = requests.request('GET',url = api_host+search_path, headers=headers,params={'term':term,'location':location})
    json_Yelp = json.loads(data_Yelp.text)
    return json_Yelp
def expo_Json(jsonFile,filename):
    export_json = json.dumps(jsonFile)
    txt = open(filename,'w')
    txt.write(export_json)
    txt.close()

json_test = get_Yelp_Data(API_HOST,SEARCH_PATH,HEADERS,TERM,LOCATION)
expo_Json(json_test,'textexpojson.json')
#Collect Data from Google Map
Google_Map_API_Key = 'AIzaSyBrZE5KzQgX6_frs_udyom_s2lMCVUZiPw'
gmap = googlemaps.Client(key=Google_Map_API_Key)
