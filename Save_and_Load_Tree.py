######### This is final project of SI 507 #########
############# Uniqname: gavincgl ##################
############# Student ID: 08807131 ################
import json
import numpy as np
import re
import requests
import ast
#####################################################Tree Set up########################################################
def Classfy_By_Price(list_Of_locations):
    """"
    classfy the raw data into four groups by price level
    Parameters
    -----------
    list_Of_locations which is raw data from by caching

    Returns
    -----------
    List sored by price
    """
    List_One_Price =[]
    List_Two_Price =[]
    List_Three_Price = []
    List_None_Price = []
    for i in range(len(list_Of_locations)):
        if list_Of_locations[i].price == None:
           List_None_Price.append(list_Of_locations[i])
        if list_Of_locations[i].price == "$":
            List_One_Price.append(list_Of_locations[i])
        elif list_Of_locations[i].price == "$$":
            List_Two_Price.append(list_Of_locations[i])
        else:
            List_Three_Price.append(list_Of_locations[i])
    Classfied_List =[List_None_Price,List_One_Price,List_Two_Price,List_Three_Price]
    return Classfied_List

def Classfy_By_Rating (list_Of_locations):
    """"
    classfy the yelp searched data in to four different groups by rating levels
    Parameters
    -----------
    list_Of_locations which is raw data from by caching

    Returns
    -----------
    List sored by customer rating
    """
    List_One_Rating =[]
    List_Two_Rating =[]
    List_Three_Rating = []
    List_Four_Rating = []
    for i in range(len(list_Of_locations)):
        if float(list_Of_locations[i].rating) <= 2:
            List_One_Rating.append(list_Of_locations[i])
        elif float(list_Of_locations[i].rating) > 2 and float(list_Of_locations[i].rating) <=3:
            List_Two_Rating.append(list_Of_locations[i])
        elif float(list_Of_locations[i].rating) >3 and float(list_Of_locations[i].rating) <=4:
            List_Three_Rating.append(list_Of_locations[i])
        else:
            List_Four_Rating.append(list_Of_locations[i])
    Classfied_List =[List_One_Rating,List_Two_Rating,List_Three_Rating,List_Four_Rating]
    return Classfied_List
def Trans_Yelp_Data_to_Tree(key,search_list):
    """"
    translate the raw data [list] in to the tree strucutre for further save and load
    Parameters
    -----------
    key : the usered typed keywords
    search_list: raw data stored in a list

    Returns
    -----------
    Designed tree
    the tree type is list
                                ------------None----------------- *  --------$$--------------------- * -------------$$--------------- * -----------------$$$------------
    unit tree structure:['key',[[[[0,2]],[(2,3]],[(3,4]],[(4,5]]]],[[[0,2]],[(2,3]],[(3,4]],[(4,5]]],[[[0,2]],[(2,3]],[(3,4]],[(4,5]],[[[0,2]],[(2,3]],[(3,4]],[(4,5]]]]]
    """
    Stored_Tree_unit = []
    Stored_Tree_unit.append(key)
    Store_search_price_list=[]
    Classfied_Price = Classfy_By_Price(search_list)
    for i in range(len(Classfied_Price)):
        Classfied_Rating = Classfy_By_Rating(Classfied_Price[i])
        Store_search_rating_list = []
        for m in range(len(Classfied_Rating)):
               Readable_Locations = []
               for k in range(len(Classfied_Rating[m])):
                      Readable_Locations.append(Classfied_Rating[m][k].get_print_str())
               Store_search_rating_list.append(Readable_Locations)
               #print(len(Store_search_rating_list))
        Store_search_price_list.append(Store_search_rating_list)
    Stored_Tree_unit.append(Store_search_price_list)
    return Stored_Tree_unit





def Save_Yelp_Data_Tree(treeList,treeFile):
    """
    Parameter
    treeList
    treeFile

    Return
    a json file storing tree
    """
    if isinstance(treeList[0],str):
        print('Node1', file=treeFile)
        print('keywords: ' + str(treeList[0]), file=treeFile)
        print('Node2', file=treeFile)
        print('Sorted by four price levels, None, $, $$ and $$$ or more', file=treeFile)
        for i in range(len(treeList[1])):
            print('Node3', file=treeFile)
            print('Sorted by four rating intervals: [0,2],(2,3],(3,4] and (4,5]', file=treeFile)
            for m in range(len(treeList[1][i])):
                print('Leaf', file=treeFile)
                print(treeList[1][i][m], file=treeFile)
    else:
        for n in range(len(treeList)):
            print('Node1',file=treeFile)
            print('keywords: '+ str(treeList[n][0]),file=treeFile)
            print('Node2',file=treeFile)
            print('Sorted by four price levels, None, $, $$ and $$$ or more', file=treeFile)
            for i in range(len(treeList[n][1])):
                  print('Node3', file=treeFile)
                  print('Sorted by four rating intervals: [0,2],(2,3],(3,4] and (4,5]', file= treeFile)
                  for m in range(len(treeList[n][1][i])):
                         print('Leaf', file=treeFile)
                         print(treeList[n][1][i][m],file=treeFile)

def Load_Yelp_Data_Tree(Yelp_Tree_File):
    """
    Parameter
    a json file storing the tree

    Return:
    list
    """
    Read_Yelp_Tree = Yelp_Tree_File.readline()
    Read_yelp_Tree0= Read_Yelp_Tree.strip()
    if Read_yelp_Tree0 == 'Leaf':
       ReadLeaf = Yelp_Tree_File.readline()
       ReadLeaf = ReadLeaf.strip()
       return ast.literal_eval(ReadLeaf)
    elif Read_yelp_Tree0 =='Node3' or Read_yelp_Tree0 =='Node2':
        Read_Yelp_Tree = Yelp_Tree_File.readline()
        Read_yelp_Tree2 = Read_Yelp_Tree.strip()
        Read_yelp_Tree_TxT1 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        Read_yelp_Tree_TxT2 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        Read_yelp_Tree_TxT3 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        Read_yelp_Tree_TxT4 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        return [Read_yelp_Tree_TxT1,Read_yelp_Tree_TxT2,Read_yelp_Tree_TxT3,Read_yelp_Tree_TxT4]
    elif Read_yelp_Tree0 =='Node1':
        Read_Yelp_Tree = Yelp_Tree_File.readline()
        Read_yelp_Tree2 = Read_Yelp_Tree.strip()
        Read_Yelp_Tree = Yelp_Tree_File.readline()
        Read_yelp_Tree3 = Read_Yelp_Tree.strip()
        Read_Yelp_Tree = Yelp_Tree_File.readline()
        Read_yelp_Tree4 = Read_Yelp_Tree.strip()
        Read_yelp_Tree_TxT1 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        Read_yelp_Tree_TxT2 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        Read_yelp_Tree_TxT3 = Load_Yelp_Data_Tree(Yelp_Tree_File)
        Read_yelp_Tree_TxT4 = Load_Yelp_Data_Tree(Yelp_Tree_File)

        return [Read_yelp_Tree2,[Read_yelp_Tree_TxT1,Read_yelp_Tree_TxT2,Read_yelp_Tree_TxT3,Read_yelp_Tree_TxT4]]