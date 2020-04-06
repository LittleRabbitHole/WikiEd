#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 13:04:04 2019
this is to collect the students contribution
@author: angli
"""

from utilities import getUserContributions
import datetime
import csv


def collectionSemester():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()    
    
    #colnames = students[0].strip().split(",")

    #collecting while writing out
    f = open(dir_file+"students_contributes_semester.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['student_username','student_userid','student_courseID','startdate','enddate','timestamp', 'ns',  'title', 'size', 'sizediff'])

    n=0
    for student in students[1::]:
        n+=1
        if n%100==0: print (n)
        student = student.strip().split(",")
        student_username = student[0]
        student_courseID = student[1]
        #starttime
        startdate = student[2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = student[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={}&ucstart={}&ucend={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(student_username), str(starttime), str(endtime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([student_username, feature['userid'], student_courseID, startdate, enddate, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([student_username, "", student_courseID, startdate, enddate, "", "", "",0,0])
    f.close()
    
collectionSemester()   



def collectionSemester_survival():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()    
    
    #colnames = students[0].strip().split(",")

    #collecting while writing out
    f = open(dir_file+"students_contributes_semester_survival.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['student_username','student_userid','student_courseID','startdate','enddate','timestamp', 'ns',  'title', 'size', 'sizediff'])

    n=0
    for student in students[1::]:
        n+=1
        if n%100==0: print (n)
        student = student.strip().split(",")
        student_username = student[0]
        student_courseID = student[1]
        #starttime
        startdate = student[2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = student[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={}&ucstart={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(student_username), str(starttime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([student_username, feature['userid'], student_courseID, startdate, enddate, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([student_username, "", student_courseID, startdate, enddate, "", "", "",0,0])
    f.close()
    
collectionSemester_survival()    
    
def collectionAfterSemester():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()    
    
    #colnames = students[0].strip().split(",")

    #collecting while writing out
    f = open(dir_file+"students_contributes_aftersemester.csv", "w", encoding="UTF-8")
    csv_f = csv.writer(f)
    csv_f.writerow(['student_username','student_userid','student_courseID','startdate','enddate','timestamp', 'ns',  'title', 'size', 'sizediff'])

    n=0
    for student in students[1::]:
        n+=1
        if n%100==0: print (n)
        student = student.strip().split(",")
        student_username = student[0]
        student_courseID = student[1]
        #starttime
        startdate = student[2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        starttime = startdate+"T00:00:00Z"
        
        #endtime
        enddate = student[-3].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        endtime = enddate+"T11:59:59Z"
       
        api_call = "https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={}&ucstart={}&ucdir=newer&ucprop=title|timestamp|comment|size|sizediff&uclimit=500&format=json".format(str(student_username), str(endtime))
        contributes = getUserContributions(api_call)
        if contributes != []:
            for feature in contributes:
                csv_f.writerow([student_username, feature['userid'], student_courseID, startdate, enddate, feature['timestamp'], str(feature['ns']),feature['title'],
                               feature.get('size'),feature.get('sizediff')])
        else:
            csv_f.writerow([student_username, "", student_courseID, startdate, enddate, "", "", "",0,0])
    f.close()
      
collectionAfterSemester()    