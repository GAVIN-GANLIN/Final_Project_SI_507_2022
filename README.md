#                                                         Final_Project_SI_507_2022

# Food recommendation app reflects insights of local racial segregation and urban consumption level (Yelp + Google Map + U.S. Census API)

## Data processing

In this final project, three APIs will be used: Yelp fusion, Google Map, and U.S. census. We try to explore relationship of food style people preferred and urban consumption structure. Also, this relationship should also be consistent with the income level of the region we examined. Take a close look at the project:

•	Gather local restaurant data from Yelp fusion API (how many fast foods in the local? Diversity of food style (Japanese, Chinese, Mexico, American, etc.), What’s the most welcome restaurant and which style it belongs to...)

•	Choose metropolitan as the target location and gather data from Google map (How many gas stations in the local? How many cinemas in the local? How many gyms in the local? Museums? Any other recreation style in the local...)

•	Gather data from US census and get the information about the income level distribution. This branch of data is to confirm if yelp data and diversity of recreations have some connections, then whether we can explore more behind this relationship? Whether this connection can give profound information about lifestyle of people belonging to different income level or cultural difference between different races?

## Data interaction

Part1: Create tree for data from Yelp fusion API. Like 20 questions game, create interface and ask users questions and then give recommendations for the users.
Part2: statistical analyze the percentage of different food style, number of fast foods in the local and the medium restaurant price distribution in the local. Then estimate relationship between diversity of recreations in the local and racial segregation and medium income distribution.

## Information presentation

First plot the map of the area we interest (NYC or Chicago), and then use heatmap or polygon to assign the color based on the medium income. Using Flask app to help user visualize the specific data they interest on the map. Give linear regression plot of any two different data from different branches the users interested (there are three branch of data: food data from Yelp, recreation data from Google map, and income and racial information from Census).

