#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 12:49:56 2018

endsemester control group contribution collection

@author: angli
"""
from utilities import getUserContributions
import pickle
import csv
import datetime

def collectionControlSemester():
    #dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    controls = f.readlines()
    f.close()    
    
    #colnames = controls[0].strip().split(",")

    #collecting while writing out
    f = open(dir_file+"controlgroup_contributes_afterSemester.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['control_wpid','control_userid','register_date','timestamp','ns','title','size','sizediff'])

    n=0
    for control in controls[1::]:
        n+=1
        if n%100==0: print (n)
        control_end = control.strip().split(",")
        control_wpid = control_end[-2]
        register_date = control_end[-1]
        #starttime
#        startdate = control_end[2].strip()
#        #reformat datetime
#        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
#        startdate = startdate_timeobject.strftime("%Y-%m-%d")
#        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = control_end[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuserids={}&ucstart={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(control_wpid),str(endtime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([control_wpid, feature['userid'], register_date, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([control_wpid, control_wpid, register_date, "", "", "",0,0])
    f.close()

collectionControlSemester()



#def collectionSemesterEnd():
#    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
#    file = "final_control_endSemester.pk"
#    f = open(dir_file+file, 'rb')   # 'r' for reading; can be omitted
#    students_controls = pickle.load(f)          # load file content as mydict
#    f.close() 
#    
##    csv_f = csv.writer(open(dir_file+"controlgroup_semesterends.csv", "w", encoding="UTF-8"))
##    #write first row
##    for lst in students_controls:
##        csv_f.writerow(lst)
#    
#    
#    f = open(dir_file+"endsemester_controlgroup_contributes.csv", "w", encoding="UTF-8")
#    csv_f = csv.writer(f)
#    csv_f.writerow(['control_wpid','control_userid', 'register_date', 'timestamp', 'ns',  'title', 'size', 'sizediff'])
#    
#    n=0
#    for pair in students_controls:
#        n+=1
#        if n%100==0: print (n)
#        control_id = str(pair[3]) 
#        student = str(pair[0])
#        register_date = str(pair[-1])
#        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuserids={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(control_id))
#        contributes = getUserContributions(api_call)
#        if contributes != []:
#            for feature in contributes:
#                csv_f.writerow([control_id, feature['userid'], register_date, feature['timestamp'], str(feature['ns']),feature['title'],
#                               feature.get('size'),feature.get('sizediff')])
#        else:
#            csv_f.writerow([control_id, control_id, register_date, "", "", "",0,0])
#    f.close()