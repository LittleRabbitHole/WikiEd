#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:34:35 2018

startsemester control group contribution collection [within semester contrib]

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
    f = open(dir_file+"controlgroup_contributes_semester.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['control_wpid','control_userid','register_date','timestamp','ns','title','size','sizediff'])

    n=0
    for control in controls[1::]:
        n+=1
        if n%100==0: print (n)
        control_start = control.strip().split(",")
        control_wpid = control_start[3]
        register_date = control_start[4]
        #starttime
        startdate = control_start[2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = control_start[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuserids={}&ucstart={}&ucend={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(control_wpid), str(starttime), str(endtime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([control_wpid, feature['userid'], register_date, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([control_wpid, control_wpid, register_date, "", "", "",0,0])
    f.close()

def collectionControlSemester_survival():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    #dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    controls = f.readlines()
    f.close()    
    
    #colnames = controls[0].strip().split(",")

    #collecting while writing out
    f = open(dir_file+"controlgroup_contributes_semester_survival.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['control_wpid','control_userid','register_date','timestamp','ns','title','size','sizediff'])

    n=0
    for control in controls[1::]:
        n+=1
        if n%100==0: print (n)
        control_start = control.strip().split(",")
        control_wpid = control_start[3]
        register_date = control_start[4]
        #starttime
        startdate = control_start[2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = control_start[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuserids={}&ucstart={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(control_wpid), str(starttime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([control_wpid, feature['userid'], register_date, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([control_wpid, control_wpid, register_date, "", "", "",0,0])
    f.close()



def collectionArticleTitleControlSemester():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    #dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    controls = f.readlines()
    f.close()    
    
    #colnames = controls[0].strip().split(",")

    #collecting while writing out
    f = open(dir_file+"controlgroup_articles_semester.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['control_wpid','control_userid','starttime','endtime','timestamp','ns','pageid','title'])
    
    contributes = []
    n=0
    for control in controls[1::]:
        n+=1
        if n%100==0: print (n)
        control_start = control.strip().split(",")
        student_wpname = control_start[0]
        control_wpid = control_start[3]
        register_date = control_start[4]
        #starttime
        startdate = control_start[2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = control_start[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuserids={}&ucstart={}&ucend={}&ucdir=newer&ucnamespace=0&ucprop=ids|title|timestamp|size|sizediff&uclimit=500&format=json".format(str(control_wpid), str(starttime), str(endtime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([control_wpid, feature['userid'], starttime, endtime, feature['timestamp'], str(feature['ns']), str(feature['pageid']), feature['title']])
        else:
            csv_f.writerow([control_wpid, control_wpid, starttime, endtime, "", "", "",""])
    f.close()



#def collectionSemesterStart():
#    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
#    file = "final_control_startSemester.pk"
#    f = open(dir_file+file, 'rb')   # 'r' for reading; can be omitted
#    students_controls = pickle.load(f)          # load file content as mydict
#    f.close() 
#    
#    csv_f = csv.writer(open(dir_file+"controlgroup_semesterstarts.csv", "w", encoding="UTF-8"))
#    #write first row
#    for lst in students_controls:
#        csv_f.writerow(lst)
#    
#    
#    f = open(dir_file+"startemester_controlgroup_contributes.csv", "w", encoding="UTF-8")
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