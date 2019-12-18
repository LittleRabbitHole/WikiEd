#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 11:49:25 2019

@author: jiajunluo
"""

import pickle
import csv
import datetime
import urllib.parse
import json
import csv
import os
import requests
import sys


def returnJsonCheck(response) -> dict:
    try:
        return response.json()
    except:
        print("ERROR")
        print(response)
        print(response.text)
        sys.exit("json error")

if __name__ == "__main__":
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
        
    f = open(dir_file+filename) 
    controls = f.readlines()
    f.close()    
    
    f = open(dir_file+"control_students_all_edits.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['wpid','start_control_wpid','edits','end_control_wpid','edits'])
    
    n=14701
    for control in controls[14701::]:
        n+=1
        if n%100==0: print (n)
        control_lst = control.strip().split(",")
        wpid = str(control_lst[0])
        start_control_wpid = str(control_lst[3])
        end_control_wpid = str(control_lst[6])
        
        start_api_call = "https://en.wikipedia.org/w/api.php?action=query&list=users&ususerids={}&usprop=editcount&format=json".format(start_control_wpid)
        end_api_call = "https://en.wikipedia.org/w/api.php?action=query&list=users&ususerids={}&usprop=editcount&format=json".format(end_control_wpid)
        
        start_response=requests.get(start_api_call)
        start_responsedata = returnJsonCheck(start_response) 
        start_total_edits = start_responsedata['query']['users'][0]['editcount']
        
        end_response=requests.get(end_api_call)
        end_responsedata = returnJsonCheck(end_response) 
        end_total_edits = end_responsedata['query']['users'][0]['editcount']
        
        csv_f.writerow([wpid, start_control_wpid, start_total_edits, end_control_wpid, end_total_edits])
    
    f.close()
        
        