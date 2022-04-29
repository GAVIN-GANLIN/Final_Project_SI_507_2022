######### This is final project of SI 507 #########
############# Uniqname: gavincgl ##################
############# Student ID: 08807131 ################
import json
import numpy as np
import re
import requests
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px #pip install plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff
import geopandas as gd # pip install geopandas
import googlemaps #pip install googlemaps
import gmplot
import ast
import Save_and_Load_Tree
#import Flask #pip install Flask
github_link= 'https://github.com/GAVIN-GANLIN/Final_Project_SI_507_2022.git'

###########################################Data Collecting##############################################################

#Collecting data from Yelp
Yelp_key ='dmnWf3eh1fIcD3Tqf-mP1plm3MLHF2iE27BhYd3h4FbfXcFMczG5Oy99RXIa4xJ58IP-0DOIuJxr4ZTeLIy6TVlq6gLOwKZXi7ZgjiOVsXf9k5OlYzzNJY18Gq9XYnYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
HEADERS = {'Authorization': 'Bearer %s' % Yelp_key}
#TERM = 'KFC'
#LOCATION = 'New York City, NY'
LIMIT = 50

def get_Yelp_Data (api_host,search_path,headers,term,location,limit,offset):
    """
    This is to fetch data from yelp fusion
    Parameters
    ----------
    api_host
    search_path
    headers
    term
    location
    limit (defalut set 50, which is the maximum number allowed per requested)
    offset (whether use offset to recursion and to get more data, we can get 1000 data in maximum by this method)

    Return
    ----------
    Yelp data directly got from request.get() function
    """
    data_Yelp = requests.get(url = api_host+search_path, headers=headers,params={'term':term,'location':location,'limit':limit,'offset':offset})
    #json_Yelp = json.loads(data_Yelp.text)
    return data_Yelp
def expo_Json(dat_list,filename):
    """
    This is to export the json data in a file the user specified
    Parameters
    ----------
    jsonFile
    filename #this is a string

    Return
    ----------
    json file
    """
    export_json = json.dumps(dat_list)
    txt = open(filename,'w')
    txt.write(export_json)
    txt.close()
def Expo_Large_Yelp_Data (api_host,search_path,headers,term,location,limit,offset):
    """
    Since the default maximum limit for yelp search results is 50. In order to get
    more data, here we use 'offset' which can unrepeatly collect data severl times
    and so in total we can get 1000 results at most.
    Parameters
    ----------
    offset: maximum results user want to get (no exceed 1000)
    filename

    Return
    ----------
    list including all the locations objects
    """

    data = []
    for unit in range (0,offset,50):
        json_test = get_Yelp_Data(api_host,search_path,headers,term,location,limit,offset)
        if json_test.status_code == 200:
           data += json_test.json()['businesses']
        elif json_test.status_code == 400:
           print('400 Bad Request')
           break
    print("total searched results are " + str(len(data)))
    return data

def Trans_data_into_Location(data_list):
    """
    This is to translate dict into location objects

    Parameter
    ----------
    data_list

    Return
    ----------
    transferred_data (list including all the location objects)

    """
    transferred_data = [Location(dict = data_list[i]) for i in range(len(data_list))]
    return transferred_data

#Collect Data from Google Map (Using geocode api to get the latitude anf longtitude of the city the user specified.
Google_Map_API_Key = 'AIzaSyCMskEulSJi2dVdagZIVzl_5h7LHFmiTWQ'

GMAP = googlemaps.Client(key=Google_Map_API_Key)
Geocode_Host_Path = 'https://maps.googleapis.com/maps/api/geocode/json?'

def get_Lat_Long_Paras(key,city):
    """
    This is to get the google search keywords and city user prefer

    Paramter
    ----------
    key (string type)
    city (string type)

    Return
    ----------
    parameter dict including key and city
    """
    Lat_Long_Paras = {'key': key,'address':city}
    return Lat_Long_Paras
def get_Lat_Long_Data(home_url,paras):
    """
    This is to get coordinate information of each result

    Parameter
    _________
    home_url
    paras

    Return
    list include boundary and center coordinate
    """
    Lat_Long =requests.get(home_url,params=paras).json()
    Lat_Long.keys()
    if Lat_Long['status']=='OK':
        geometry = Lat_Long['results'][0]['geometry']
        Lati = geometry['location']['lat']
        Lon = geometry['location']['lng']
        Lati_bound_min = geometry['bounds']['southwest']['lat']
        Lati_bound_max = geometry['bounds']['northeast']['lat']
        Longi_bound_min = geometry['bounds']['southwest']['lng']
        Longi_bound_max = geometry['bounds']['northeast']['lng']
        Catch_Lat_Long =[Lati,Lon,Lati_bound_min,Lati_bound_max,Longi_bound_min,Longi_bound_max]
    return Catch_Lat_Long
#Coordinate_list = get_Lat_Long_Data(Geocode_Host_Path,get_Lat_Long_Paras(Google_Map_API_Key,'New York'))
#print(Coordinate_list)

#Collect Data from census
Code_For_Poverty = 'B10059_002E'
Code_For_Income = 'B19013_001E'
Census_Api_Code ='1e4551d0df6670f7af1bc8cf179d731ee458690a'
Census_TractNum_Host_Path='https://geo.fcc.gov/api/census/area?'
Census_Host_Path='https://api.census.gov/data/2020/acs/acs5?'
def get_Local_TractNum(Tract_Home_Url,Lat,Lon,Year):
    """
    This is to get tractnumber based on coordinate and year
    Parameter
    ---------
    Tract_Home_Url
    Lat
    Lon
    Year

    Return
    ---------
    Tract number
    """
    search = requests.get(Tract_Home_Url,params ={'lat':Lat,'lon':Lon,'censusYear':Year}).json()
    TractNum = search['results'][0]['block_fips']
    return TractNum
def get_Census_Paras(Discovery_Code,Tract_Code,State_Code,County_Code,Api_Key):
    """
    This is to get the parameter dict for census searching
    Parameter
    ----------
    Discovery_Code
    Tract_Code
    State_Code
    County_Code
    Api_Key

    Returns
    dict
    ---------
    """

    Census_Paras = {'get':Discovery_Code,'for=tract':Tract_Code,'in=state':State_Code,'in=county':County_Code,'key':Api_Key}
    return Census_Paras
def get_Census_Data(home_Url,Discovery_Code,Tract_Code,State_Code,County_Code,Api_Key):
    """
    This is to cach the census data

    Parameter
    ----------
    home_Url
    Dict of parameters

    Returns
    json object containing searched census data.
    ----------
    """
    Census_Data = requests.get(home_Url+'get='+Discovery_Code+'&for=tract:'+Tract_Code+'&in=state:'+State_Code+'&in=county:'+County_Code+'&key='+Api_Key)
    Read_census_data = Census_Data.json()
    return Read_census_data


class Location(object):
    def __init__(self, name=None, categories=None,rating=None,Latitude=None, Longitude=None, price=None,city=None,state = None, address=None,
                   phone=None,dict = {}):
        """A class to describe a location
        Parameters
        ----------
        name
        city
        state
        address
        categories
        rating
        Latitude
        Longitude
        price
        phone
        list
        """
        self.name = dict['name']
        self.categories = dict['categories']
        self.rating = dict['rating']
        self.Latitude = dict['coordinates']['latitude']
        self.Longitude = dict['coordinates']['longitude']
        if 'price' in dict.keys():
            self.price = dict['price']
        else:
            self.price = None
        self.city = dict['location']['city']
        self.state = dict['location']['state']
        self.address = dict['location']['display_address']
        self.phone = dict['phone']

    def get_variables_tuple(self, city_id):
        """Gets a tuple for saving to database
        Parameters
        ----------
        city_id

        Returns
        -------
        tuple
        """
        return self.name, self.city, city_id, self.address, self.categories, self.rating,self.Latitude,self.Longitude, self.price, self.phone

    def get_print_str(self):
        """Gets a string for information showing
        Returns
        -------
        str
        """
        cach = []
        #cach.append( f'{self.name} | Rating: {self.rating} | Price: {self.price} | Address: {self.address} | Latitude:{self.Latitude} | Longitude:{self.Longitude}')
        dict = {'name':self.name,'rating':self.rating,'price':self.price,'address':self.address,'latitude':self.Latitude,'longitude':self.Longitude}
        cach.append(dict)
        return cach

    def get_lat_lon_list(self):
        '''
        Get the latitude and longitude of the location object
        Restuns
        --------
        list contains location's latitude and longitude
        '''
        Coordinate_list = []
        Coordinate_list.append(self.Latitude)
        Coordinate_list.append(self.Longitude)
        return Coordinate_list
#----------------------------------------------------------------------------
# #Test Code
# txtTest = open('test.json','r')
# txt = txtTest.read()
# txtJson = json.loads(txt)
# txtTest.close()
# print(len(txtJson))
# print(type(txtJson[0]))
# print(txtJson[0].keys())
# print(type(txtJson[0]['price']))
# print(type('$'))
# print(type(Location(dict=txtJson[0])))
# treeListTest = [Location(dict = txtJson[i]) for i in range(len(txtJson))]
#---------------------------------------------------------------------------

#----------------------------------------------------
#Test Code
#

#Test Code
# txtTest = open('test.json','r')
# txt = txtTest.read()
# txtJson = json.loads(txt)
# txtTest.close()
# print(type(txtJson))
# print(type(txtJson[0]))
# print(txtJson[0].keys())
# print(type(txtJson[0]['price']))
# print(type('$'))
# print(type(Location(dict=txtJson[0])))
# treeListTest = [Location(dict = txtJson[i]) for i in range(len(txtJson))]
# treeListTest = Trans_Yelp_Data_to_Tree('food',treeListTest)
# print(treeListTest)
# print (len(treeListTest))
# print(treeListTest)
# print(type(treeListTest))
# print(len(treeListTest[1]))
# fileName_save = input("Please enter a file name: ")
# treeFile = open(fileName_save, 'w')
# Save_Yelp_Data_Tree(treeListTest,treeFile)
# treeFile = open('6.txt', 'r')


# Tree = Load_Yelp_Data_Tree(treeFile)
# treeFile.close()
# print(Tree)
# print(len(Tree))
# print(type(Tree[1]))
# print(len(Tree[1][1]))
# print(Tree[1][0][0][0][0]['rating'])
# fileName_save = input("Please enter a file name: ")
# treeFile = open(fileName_save, 'w')
# Save_Yelp_Data_Tree(Tree,treeFile)
#----------------------------------------------------

##################################################Dta Interation and Presentation#######################################
def yes(prompt):
    """DOCSTRING!"""
    # This helper function is to decide whether the anwer is yes or no
    '''
       Parameters:
           input text to let the program know yes or no
       returns:
           bool 
    '''
    Ans = input(prompt)
    if Ans[0:1].lower() =='y' or Ans[0:1].lower() =='s':
       return True
    elif Ans[0:1].lower() == 'n':
       return False



# #Test Code
# txtTest = open('test.json','r')
# txt = txtTest.read()
# txtJson = json.loads(txt)
# txtTest.close()
# # print(len(txtJson))
# # print(type(txtJson[0]))
# # print(txtJson[0].keys())
# # print(type(txtJson[0]['price']))
# # print(type('$'))
# # print(type(Location(dict=txtJson[0])))
# treeListTest = [Location(dict = txtJson[i]) for i in range(len(txtJson))]

def Plot_location_in_Maps(lat,longi,treeList,color,html_name):
    """
    This is to plot the locations in a map with the help of Google map api
    Parameters
    -----------
    lat
    longi
    locationList
    color
    html_name

    Returns
    ----------
    html file including the map and sotred in the local forder which the same as the python file.
    """
    Catch_Map = gmplot.GoogleMapPlotter(lat,longi,11.5)
    latitude_list=[]
    longitude_list=[]
    for i in range(len(treeList[1])):
        for m in range(len(treeList[1][i])):
            for k in range(len(treeList[1][i][m])):
                if treeList[1][i][m][k][0] != []:
                    latitude_list.append(float(treeList[1][i][m][k][0]['latitude']))
                    longitude_list.append(float(treeList[1][i][m][k][0]['longitude']))
    Catch_Map.apikey=Google_Map_API_Key
    Catch_Map.scatter(latitude_list,longitude_list,color,size = 40, marker = True)
    Catch_Map.draw(html_name)

def input_user_display_choice():
    """Asks user for display method choice

    Parameters
    ----------
    upper_range

    Returns
    -------
    int
    """
    possible_choice = [str(i) for i in range(1, 7)]
    while True:
        print('1. Average rating of these restaurants')
        print('2. Rating distribution plot')
        print('3. Price pie chart')
        print('4. Distribution in the map')
        print('5. Average Poverty level in selected regions')
        print('6. Average Income level in selected regions')
        display_choice = input(f'Please enter a choice number from 1 to 6 or "back" to choose a new category: ').lower()
        print('-' * 80)
        if display_choice == "back":
            return display_choice
        if display_choice in possible_choice:
            return display_choice
        else:
            print('[Error] Wrong input! You should type number between 1 and 6. Try again!')

def print_average_rating(treeList):
    """Display method two showing the average rating
    Parameters
    ----------
    params

    Returns
    -------

    """
    info_list = []
    for i in range(len(treeList[1])):
        for m in range(len(treeList[1][i])):
            for k in range(len(treeList[1][i][m])):
                if treeList[1][i][m][k][0] != []:
                    info_list.append(float(treeList[1][i][m][k][0]['rating']))
    average = sum(element for element in info_list) / len(info_list)
    print(f'The average rating is {average}')
    print('-' * 80)


def plot_rating_distribution(treeList):
    """Display method three plotting the rating distribution
    Parameters
    ----------
    params

    Returns
    -------

    """
    info_list = []
    for i in range(len(treeList[1])):
        for m in range(len(treeList[1][i])):
            for k in range(len(treeList[1][i][m])):
                if treeList[1][i][m][k][0] != []:
                    info_list.append(float(treeList[1][i][m][k][0]['rating']))
    fig = ff.create_distplot([info_list], ['Rating'], bin_size=0.5)
    fig.layout.update(           title = treeList[0]           )
    print("Plotting")
    print('-' * 80)
    fig.show()


def plot_price_pie_chart(treeList):
    """Display method three plotting the price pie chart
    Parameters
    ----------
    params

    Returns
    -------

    """
    info_list = []
    key=[]
    for i in range(len(treeList[1])):
        for m in range(len(treeList[1][i])):
            for k in range(len(treeList[1][i][m])):
                if treeList[1][i][m][k][0]['price'] == '$':
                    info_list.append(float(1))
                    key.append('Pricing level: $')
                elif treeList[1][i][m][k][0]['price'] == '$$':
                    info_list.append(float(2))
                    key.append('Pricing level: $$')
                elif treeList[1][i][m][k][0]['price'] == '$$$':
                    info_list.append((float(3)))
                    key.append('Pricing level: $$$')
                elif treeList[1][i][m][k][0]['price'] == '$$$$':
                    info_list.append((float(4)))
                    key.append('Pricing level: $$$$')
    print(key)
    print("Plotting")
    print('-' * 80)
    fig = go.Figure(data=[go.Pie(labels=key, values=info_list,title= treeList[0])])
    fig.show()


def Print_average_economy_condition(treeList,Discovery_Code):
    """
    This is to combine the data from Census and explore the income and poverty condition in the selected locations
    Parameters
    ---------------
    treelist (tree in the form of list)
    Discovery_Code (poverty code or income code)

    Return
    int average data
    -----------------
    """

    latitude_list=[]
    longitude_list=[]
    for i in range(len(treeList[1])):
        for m in range(len(treeList[1][i])):
            for k in range(len(treeList[1][i][m])):
                if treeList[1][i][m][k][0] != []:
                    latitude_list.append(float(treeList[1][i][m][k][0]['latitude']))
                    longitude_list.append(float(treeList[1][i][m][k][0]['longitude']))
    TracNum_list = []
    for t in range(len(latitude_list)):
        TracNum_list.append(get_Local_TractNum(Census_TractNum_Host_Path,latitude_list[t],longitude_list[t],2020))
    Economy_list=[]
    for s in range(len(TracNum_list)):
            ecnomy_data = get_Census_Data(Census_Host_Path,Discovery_Code,TracNum_list[s][5:11],TracNum_list[s][0:2],TracNum_list[s][2:5],Census_Api_Code)
            Economy_list.append(float(ecnomy_data[1][0]))
    print(Economy_list)
    average_economy_list = sum(element for element in Economy_list)/len(Economy_list)
    print(f'The average number is {average_economy_list}')
    print(average_economy_list)
    return average_economy_list

#test code
#print_average_rating(Tree)
#plot_price_pie_chart(Tree)
#plot_rating_distribution(Tree)
#Print_average_economy_condition(Tree,Code_For_Income)
#Print_average_economy_condition(Tree,Code_For_Poverty)




if __name__=="__main__":
   print('')
   print('')
   print("##############################welcome to use this program!#############################")
   print('')
   print('')
   Poverty_list=[]
   Income_Condition_list=[]
   Start_Play = True
   while Start_Play:
       load_File = yes('Do you want to load a tree file? ')
       if load_File:
           fileName_load= input('Please input the loaded file name: ')
           load_tree = open(fileName_load, 'r')
           Trans_Data_into_tree = Save_and_Load_Tree.Load_Yelp_Data_Tree(load_tree)
           city = Trans_Data_into_tree[0].split("in",1)[1]
           load_tree.close()
           print('-' * 80)
           print('-------------------------Data preparing----------------------')
       else:
            key = input("Please input your interested location into Yelp Fusion: ")
            city = input("Please narrow down to the city you interested in the USA: ")
            offset = input('Please specify how many results you want to get (should be multiply of 50 and no exceeding 1000: ')
            print('-'* 80)
            print('-------------------------Data preparing----------------------')
            load_data = Expo_Large_Yelp_Data(API_HOST,SEARCH_PATH,HEADERS,key,city,LIMIT,int(offset))
            keywords = key + ' in ' + city
            Transferred_data = Trans_data_into_Location(load_data)
            Trans_Data_into_tree = Save_and_Load_Tree.Trans_Yelp_Data_to_Tree(keywords,Transferred_data)
            save_data_to_json = yes('Do you want to store the raw results into json file? ')
            if save_data_to_json:
                fileName_json = input("Please give the json file a name: ")
                expo_Json(load_data,fileName_json)
       save_data_tree = yes('Do you want to save the data into tree? ')
       if save_data_tree:
           fileName_tree = input('Please give the tree file a name ')
           treeFile = open(fileName_tree, 'w')
           Save_and_Load_Tree.Save_Yelp_Data_Tree(Trans_Data_into_tree,treeFile)
           treeFile.close()
       print('')
       print("########################Now let's do data presentation#################################")
       print('')
       while True:
           answer = input_user_display_choice()
           if answer == "1":
              print_average_rating(Trans_Data_into_tree)
           elif answer == "2":
              plot_rating_distribution(Trans_Data_into_tree)
           elif answer == "3":
              plot_price_pie_chart(Trans_Data_into_tree)
           elif answer == "4":
               COLOR = input('what color do you want to mark the location in the map: ')
               HTML_Name = input('Give a name to html map file(attentiaon it is a html file): ')
               LAT = get_Lat_Long_Data(Geocode_Host_Path,get_Lat_Long_Paras(Google_Map_API_Key,city))[0]
               LONGI = get_Lat_Long_Data(Geocode_Host_Path,get_Lat_Long_Paras(Google_Map_API_Key,city))[1]
               Plot_location_in_Maps(LAT,LONGI,Trans_Data_into_tree,COLOR,HTML_Name)
           elif answer == "5":
               average_data = Print_average_economy_condition(Trans_Data_into_tree,Code_For_Poverty)
               Poverty_unit =[Trans_Data_into_tree[0],average_data]
               Poverty_list.append(Poverty_unit)
           elif answer == "6":
               average_data_Income = Print_average_economy_condition(Trans_Data_into_tree,Code_For_Income)
               Income_unit = [Trans_Data_into_tree[0],average_data_Income]
               Income_Condition_list.append(Income_unit)

           elif answer == 'back':
               break
       play_again= yes('Do you want to play again?')
       if play_again:
           Start_Play == True
       else:
           Start_Play == False
           break
   print('Below is average number of people under poverty in selected areas (return [] if you did not play 5th data display')
   print(Poverty_list)
   print('Below is average income under poverty in selected areas (return [] if you did not play 5th data display')
   print(Income_Condition_list)
   print('#############################Thank you for using! See you again!#########################')




