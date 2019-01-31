#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:19:34 2019

@author: angli
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:52:16 2017
last update: 03/06
This is to collect the user talk page data for year 2015-2016 period
@author: angli

Data is collected following the steps"
1. collect all student talkpage edit history, including both with students and with wikipedians
This step collacted all the students edit in and out, wikipedians edited in students' talk page
2. collect all students edit out to wikipeidans' talk page
This step collacted all the students edit out to wikipedians' talk page


this code is still messy, cannot run directly
"""

import datetime
import urllib.parse
import json
import csv
import os
import pandas as pd
import numpy as np
from utilities import GetPageRevision
from data_processor import LastEdit, Death

# read the list of users

def userList():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()
    
    studentList = []
    for student in students[1::]:
        student = student.strip().split(",")
        student_username = student[0].strip()
        student_startdate = student[2].strip()
        studentList.append([student_username, student_startdate])
    
    return studentList


def usernamesLst():
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    filename = "control_students_all.csv"
    
    f = open(dir_file+filename) 
    students = f.readlines()
    f.close()
    
    studentList = []
    for student in students[1::]:
        student = student.strip().split(",")
        student_username = student[0].strip()
        #student_startdate = student[2].strip()
        studentList.append(student_username)
    
    return studentList

######edit in to students' user talk page

def talkpageRevisions():

    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    csv_f = csv.writer(open(dir_file+"students_talkpage_revisions.csv", "w", encoding="UTF-8"))
    #write first row
    csv_f.writerow(['wpid','startdate','usertalkpage','talkpage_editor', 'timestamp', 'size','comment'])
    #write error
    
    
    #student lists
    studentList = userList()
    
    # read username catch the Wiki data
    n=0
    for student in studentList:
        wpid = student[0]
        startdate = student[1]
        wpid = wpid.strip()
        #print (rawID)
        #wpid_nospace = wpid.replace(" ","_")
        #decode student's name into ascii
        decode_wpid = urllib.parse.quote(wpid)
        #api
        #api_call = ("https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={}&ucdir=newer&ucstart={}&ucend={}&ucprop=title|timestamp|comment|size|sizediff|flags&uclimit=500&format=json").format(decode_wpid,starttime,endtime)#Kingsleyta
        #https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User_talk:Kingsleyta&rvdir=newer&rvend=2015-03-30T13:20:52Z&rvprop=timestamp|user|size|comment&rvdir=newer&rvlimit=500    
        api_call = ("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User talk:{}&rvdir=newer&rvprop=timestamp|user|size|comment&rvdir=newer&rvlimit=500&format=json").format(decode_wpid)#Kingsleyta
        try: 
            talkpage_revisions_lst = GetPageRevision(api_call)
            for feature in talkpage_revisions_lst:
                if feature.get('user') != wpid: #not writeout self editing
                    csv_f.writerow([ wpid, startdate, "user_talk", feature.get('user'), feature['timestamp'], feature.get('size'), feature.get('commet')])
        except KeyError:
            csv_f.writerow([wpid, startdate, "user_talk", "no user talk", "",0,""])
        n+=1
        if n%100==0:
            print (n) 

import math
def LastEdit1(row, last_survivalday, max_timedelta):
    #mark the whether the edit is the last edit made by the editor
    #based on the largest timedelta
    timedelta = row['day_index_timedelta']
    timestamp = row['timestamp']
    if type(timestamp) is str:
        timestamp = pd.to_datetime(timestamp)
        today = pd.to_datetime(timestamp.strftime('%Y-%m-%d'))
        #day_index = row["day_index"] 
        if today == last_survivalday and timedelta == max_timedelta: 
            last_edit_mark=1
        else:
            last_edit_mark=0            
    elif math.isnan(timestamp):
        last_edit_mark = 1
    return  last_edit_mark



def Death1(row, last_survivalday):
    #mark, if the edit row is the last edit, whether it is death or not (no activity >30 days from now)
    timestamp = row['timestamp']
    last_censored = row['last_day_censored']
    last_edit_tillend = (last_censored - last_survivalday).days 
    if type(timestamp) is str:
        timestamp = pd.to_datetime(timestamp)
        #today = pd.to_datetime(timestamp.strftime('%Y-%m-%d'))
        #day_index = row["day_index"] 
        if row["last_edit_mark"] == 1 and last_edit_tillend>30:
            death =1
        else:
            death=0
            
    elif math.isnan(timestamp):
        death = 1
    return  death



def dataProcessor():
    studentscohort = usernamesLst()
    
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "students_talkpage_revisions.csv"
    data = pd.read_csv(dir_file+file, skipinitialspace = True, quotechar = '"')
    
    data['timestamp1'] = pd.to_datetime(data['timestamp'])
    data['register_date'] = pd.to_datetime(data['register_date'])
    data["day_index_timedelta"] = data['timestamp1'] - data['register_date']#as timedelta
    data["day_index"] = data["day_index_timedelta"].dt.days
    data["wiki_msgin"] =  data['talkpage_editor'].apply(lambda x: 0 if x in studentscohort else 1)
    data['last_day_censored'] = pd.to_datetime("2019-01-15")
    data['today'] = pd.to_datetime(data['timestamp1'].dt.strftime('%Y-%m-%d'))
    data = data.loc[data['wiki_msgin'] >0]

    aggre_data=[]
    
    Grouped1 = data.groupby(['wpid', 'register_date'])                              
    n=0
    for group1 in Grouped1:
        n+=1
        if n%100==0: print (n)
        #if n==4: break
        wpid, register_date = group1[0]
        
        day_lst = group1[1][['today','day_index_timedelta']]
        first_survivalday = day_lst['today'].iloc[0]
        last_survivalday = day_lst['today'].iloc[-1]
        max_timedelta = day_lst['day_index_timedelta'].max()#last edit time - register time
        #last edit mark
        group1[1]["last_edit_mark"] = group1[1].apply(LastEdit1, axis=1, last_survivalday = last_survivalday, max_timedelta = max_timedelta)
        group1[1]["death"] = group1[1].apply(Death1, axis=1, last_survivalday = last_survivalday)
        
        #survival elements
        lastedit_row = group1[1].loc[group1[1]['last_edit_mark'] == 1]
        death = list(lastedit_row['death'])[0]
        deathdate = lastedit_row['day_index_timedelta'].iloc[0].days
        
        #group for day index
        subdata = group1[1]
        
        Grouped2 = subdata.groupby(['day_index'])
        #Grouped.ngroups
        m=0
        for group2 in Grouped2:
            m+=1
            #if m%100==0: print (n)
            #if m==4: break

            day_index = group2[0]
            #register_date = register_date.strftime('%Y-%m-%d')
            
            msgin_lst = list(group2[1]["wiki_msgin"])
            from_wiki = sum(msgin_lst)
            from_stu = len(msgin_lst) - from_wiki
            #unit data
            pidgroup_data = [wpid, register_date, death, deathdate, day_index, from_wiki, from_stu]        
            aggre_data.append(pidgroup_data)
    
    #write out
    i = 0
    outString = 'wpid,register_date,death,deathdate,day_index,from_wiki,from_stu'
    for item in aggre_data:
        str_item = [str(i) for i in item]
        i += 1
        outString += '\n'
        outString += ','.join(str_item)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(dir_file+"studentTalkpageWiki_aggre.csv", 'w') as f:
        f.write(outString)
        f.close()




if __name__ == "__main__":
    
    talkpageRevisions()
    dataProcessor()

# =============================================================================
# ##########################################
# ### collect student contribution in user talk page (edit out)
# 
# csv_f = csv.writer(open("studentContri_talkout_2015-2016_0306.csv", "w"))
# #write first row
# csv_f.writerow(['wpid','SID','course','courseID','oldStudent','article','ns','page_title','talkpage_owner', 'timestamp', 'size','comment'])
# #write error
# csv_error = csv.writer(open("studentsContri_talkout_errorusers_20152016_0306.csv", "w", encoding="UTF-8"))
# 
# #user talk page revisions
# #regular expression to match out the username
# import re
# talkpageowner_re = re.compile(r'User talk:(.*)/|User talk:(.*)', re.DOTALL)#User talk:(.*)/sandbox|User talk:(.*)/
# 
# n=0
# for line in info[1::]:
#     line = line.strip()
#     info_lst = line.split('\t')
#     #studentID
#     SID = info_lst[1]
#     #course
#     course = info_lst[2]
#     #courseID
#     courseID = info_lst[3]
#     #return Student
#     oldStudent = info_lst[4]
#     #get name from names list
#     wpid =  info_lst[0]
#     wpid = wpid.strip()
#     #print (rawID)
#     wpid_nospace = wpid.replace(" ","_")
#     #decode student's name into ascii
#     decode_wpid = urllib.parse.quote(wpid_nospace)
#     #quarter time window
#     starttime = info_lst[-2]+"T00:00:00Z"
#     endtime = info_lst[-1]+"T11:59:59Z"
#     
#     #API https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User_talk:Averysf&rvuser=Poetries&rvdir=newer&rvprop=timestamp|user|size|comment&rvdir=newer&rvlimit=500
#     api_call = ("https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={}&ucnamespace=3&ucdir=newer&ucstart={}&ucend={}&ucprop=timestamp|title|sizediff|comment&uclimit=500&format=json").format(decode_wpid,starttime,endtime)#Kingsleyta
#     response=urllib.request.urlopen(api_call)
#     str_response=response.read().decode('utf-8')
#     responsedata = json.loads(str_response)
#     try: 
#         revision_data_lst=responsedata["query"]["usercontribs"]#list
#         for feature in revision_data_lst:
#             talk_page_title = feature.get('title')
#             talk_page_owner1 = re.match(talkpageowner_re, talk_page_title).group(1)
#             talk_page_owner2 = re.match(talkpageowner_re, talk_page_title).group(2)
#             talk_page_owner_lst=list(set([talk_page_owner1,talk_page_owner2]))
#             talk_page_owner = [x for x in talk_page_owner_lst if x is not None][0]
#             if wpid != talk_page_owner: #not edit in their own talk page
#                 csv_f.writerow([wpid, SID,course,courseID,oldStudent,"user_talk", 3, talk_page_title, talk_page_owner, feature['timestamp'], feature.get('sizediff'), feature.get('comment')])
#     except KeyError:
#         #pass
#         csv_error.writerow([wpid, SID,course,courseID,oldStudent,"user_talk", 3, page_title, "no user talk", "no user talk","no user talk","no user talk"])
#     n+=1    
#     if n%100==0:
#         print (n) 
# 
# 
# 
# 
# =============================================================================





















