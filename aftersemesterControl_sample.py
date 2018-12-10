#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:44:01 2018

based on the data, select a random control sample based on the registration date (+-5 days)

@author: Ang
"""

import pandas as pd
import numpy as np
import datetime
from utilities import NearestDate
import random
import pickle

def processAllNames():

    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "allnewusers_2010.txt"
    
    f = open(dir_file+filename) 
    allnewcomers = f.readlines()
    f.close()
    
    newcomers_processed = {}
    
    for line in allnewcomers:
        line = line.strip().split(",")
        userid = str(line[0]).strip()
        register_date = str(line[-3]).strip()
        try:
            newcomers_processed[register_date].append(userid)
        except KeyError:
            newcomers_processed[register_date] = [userid]

    return newcomers_processed



def randomSelection_endSemester(allnewcomers):
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "2015_2016_student_courses_list.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()
    
    #all newcomers register time in datetime
    alldates_key = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in list(allnewcomers.keys())]
    
    finalSelection = []
    for student in students[1::]:
        student = student.strip().split(",")
        student_username = student[0]
        student_courseID = student[2]
        enddate = student[-1].strip()
        #reformat datetime
        enddate_timeobject = datetime.datetime.strptime(enddate, "%m/%d/%y")
        enddate = enddate_timeobject.strftime("%Y-%m-%d")
        #before/after 5 days
        n_day = datetime.timedelta(days=5)
        closestDate = NearestDate(alldates_key, enddate_timeobject)
        time_delta = abs(closestDate - enddate_timeobject)
        #selecting control
        if time_delta <= n_day:
            closestDate_str = closestDate.strftime("%Y-%m-%d")
            control_list = allnewcomers.get(closestDate_str)
            selected_control = random.sample(control_list, 1)
            control_pair = [student_username, student_courseID, enddate, selected_control[0], closestDate_str]
            finalSelection.append(control_pair)
            #update the dictionary for next selection -- avoid the repetition
            control_list_update = list(filter(lambda a: a != selected_control[0], control_list))
            allnewcomers[closestDate_str] = control_list_update
        else:
            finalSelection.append([student_username, student_courseID, enddate,  "-11111", closestDate_str])
    
    return finalSelection            
            
 
def randomSelection_startSemester(allnewcomers):
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "2015_2016_student_courses_list.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()
    
    #all newcomers register time in datetime
    alldates_key = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in list(allnewcomers.keys())]
    
    finalSelection = []
    for student in students[1::]:
        student = student.strip().split(",")
        student_username = student[0]
        student_courseID = student[2]
        startdate = student[-2].strip()
        #reformat datetime
        startdate_timeobject = datetime.datetime.strptime(startdate, "%m/%d/%y")
        startdate = startdate_timeobject.strftime("%Y-%m-%d")
        #before/after 5 days
        n_day = datetime.timedelta(days=5)
        closestDate = NearestDate(alldates_key, startdate_timeobject)
        time_delta = abs(closestDate - startdate_timeobject)
        #selecting control
        if time_delta <= n_day:
            closestDate_str = closestDate.strftime("%Y-%m-%d")
            control_list = allnewcomers.get(closestDate_str)
            selected_control = random.sample(control_list, 1)
            control_pair = [student_username, student_courseID, startdate, selected_control[0], closestDate_str]
            finalSelection.append(control_pair)
            #update the dictionary for next selection -- avoid the repetition
            control_list_update = list(filter(lambda a: a != selected_control[0], control_list))
            allnewcomers[closestDate_str] = control_list_update
        else:
            finalSelection.append([student_username, student_courseID, startdate,  "-11111", closestDate_str])
    
    return finalSelection 

           
if __name__ == "__main__":
    allnewcomers = processAllNames()
    
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"

    control_selection_endSemester = randomSelection_endSemester(allnewcomers)    
    file = "final_control_endSemester.pk"    
    f = open(dir_file+file, 'wb')   
    pickle.dump(control_selection_endSemester, f)          
    f.close() 

    control_selection_startSemester = randomSelection_startSemester(allnewcomers)    
    file = "final_control_startSemester.pk"
    f = open(dir_file+file, 'wb')   
    pickle.dump(control_selection_startSemester, f)          
    f.close() 





