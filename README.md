#                                                                   Final_Project_SI_507_2022

# Food recommendation app reflects insights of local racial segregation and urban consumption level (Yelp + Google Map + U.S. Census API)

## Data processing

In this final project, three APIs will be used: Yelp fusion, Google Map, and U.S. census. We try to explore relationship of food style people preferred and urban consumption structure. Also, this relationship should also be consistent with the income level of the region we examined. Take a close look at the project:

•	Gather local restaurant data from Yelp fusion API (how many fast foods in the local? Diversity of food style (Japanese, Chinese, Mexico, American, etc.), What’s the most welcome restaurant and which style it belongs to...)

•	Choose metropolitan as the target location and gather data from Google map (How many gas stations in the local? How many cinemas in the local? How many gyms in the local? Museums? Any other recreation style in the local...)

•	Gather data from US census and get the information about the income level distribution. This branch of data is to confirm if yelp data and diversity of recreations have some connections, then whether we can explore more behind this relationship? 

## Data interaction

Part1: Create tree for data from Yelp fusion API. Like 20 questions game, create interface and ask users questions and then give recommendations for the users.
Part2: statistical analyze the percentage of different food style, number of fast foods in the local and the medium restaurant price distribution in the local. Then estimate relationship between diversity of recreations in the local and medium income distribution.

## Information presentation

First plot the map of the area we interest (NYC or Chicago), and then use heatmap or polygon to assign the color based on the medium income. Using Flask app to help user visualize the specific data they interest on the map. Give linear regression plot of any two different data from different branches the users interested (there are three branch of data: food data from Yelp, recreation data from Google map, and income and employment information from Census).

## Instructions for code running

Installtion of python packages

$pip install plotly <br />
$pip install googlemaps <br />
$pip install gmplot <br />
$pip install geopandas
<br />
Import package that installed already while is not frequently used
<br />
import ast
<br />
API Application
<br />
Yelp Fusion (Free)<br />
https://www.yelp.com/developers/documentation/v3/authentication <br />
Follow the instructions above, it is free and you simply need to create app and then you can get your personal api key. However, they have limit on daliy search amount threshold <br />
Google Map Api (Not free!!!!!) <br />
https://cloud.google.com/docs/authentication/api-keys <br />
You need to first login in your gamil account, then you need to create your own project. One thing need to notice is that you must linke your project to a billing account and give your personal api key restrictions so that your api key can be successfully activated.<br />
Census Api (Free) <br />
https://geo.fcc.gov/api/census/ (no need for key and we need tract number(in block_fips) from this website,the tract number will help us to query the data from census/acs data. <br />
https://www.census.gov/data/developers/guidance/api-user-guide.What_is_the_API.html <br />
Read the contents in the link above. scroll down to bottom and click the 'Request a Key' button on the left of the webpage.

Once you finish the set up and successflly get all your new personal api keys, please replace the three key variables in the code (see below) with your own keys. 

Yelp_key = 'your key' <br />
Google_Map_API_Key = 'your key' <br />
Census_Api_Code = 'your key' <br />

## Interaction with the code
  As for Yelp Fusion. three parameters you need to input: catgories of location you want to search (e.g. Museum); narrow down the search region to a city(e.g. New York); offset value which means how many results you want to get(should be multiple of 50 and not exceed 1000)<br />
  As for Google Map Api, it needs the first two parameters required for Yelp Fusion, and the program will deliver the two parameters to Google map api automatically once you type them for Yelp Fusion.<br />
  As for Census, you first need to give the latitude and longitude and year(default 20202) information to get_Local_TractNum(Tract_Home_Url,Lat,Lon,Year) function to get corresponding tract number in https://geo.fcc.gov/api/census/  and then use the number to get information you want in the https://www.census.gov/data/developers/data-sets/acs-5year.html. Also, you need the code for the economy data you are interested, you can see detalied code tables here:https://api.census.gov/data/2020/acs/acs5/variables.html<br />
  
## Data Structure: Tree
  
  ![image](https://user-images.githubusercontent.com/58121031/166068492-242df513-3bd6-4c48-8843-bf05337349a0.png)
Below is the illustration of the tree in a list style:
  
![image](https://user-images.githubusercontent.com/58121031/166069151-4601caf4-034d-45b3-8943-e3597f5e11e3.png)
  
$, $$, $$$ and None mean the price level get from the yelp fusion
[0,2],(2,3],(3,4],(4,5] are four different groups for rating values [0,5] got from Yelp API.
