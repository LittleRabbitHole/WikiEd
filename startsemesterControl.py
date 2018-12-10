#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:34:35 2018

startsemester control group contribution collection

@author: angli
"""

from utilities import getUserContributions
import pickle
import csv

if __name__ == "__main__":
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "final_control_startSemester.pk"
    f = open(dir_file+file, 'rb')   # 'r' for reading; can be omitted
    students_controls = pickle.load(f)          # load file content as mydict
    f.close() 
    
    csv_f = csv.writer(open(dir_file+"controlgroup_semesterstarts.csv", "w", encoding="UTF-8"))
    #write first row
    for lst in students_controls:
        csv_f.writerow(lst)
    
    
    f = open(dir_file+"startemester_controlgroup_contributes.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['control_wpid','control_userid', 'register_date', 'timestamp', 'ns',  'title', 'size', 'sizediff'])
    
    n=0
    for pair in students_controls:
        n+=1
        if n%100==0: print (n)
        control_id = str(pair[3]) 
        student = str(pair[0])
        register_date = str(pair[-1])
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuserids={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(control_id))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([control_id, feature['userid'], register_date, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([control_id, control_id, register_date, "", "", "",0,0])
    f.close()