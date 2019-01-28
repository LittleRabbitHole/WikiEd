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

#########################################
###edit in to students' user talk page
dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
csv_f = csv.writer(open(dir_file+"students_talkpage_contribution.csv", "w", encoding="UTF-8"))
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



##########################################
### collect student contribution in user talk page (edit out)

csv_f = csv.writer(open("studentContri_talkout_2015-2016_0306.csv", "w"))
#write first row
csv_f.writerow(['wpid','SID','course','courseID','oldStudent','article','ns','page_title','talkpage_owner', 'timestamp', 'size','comment'])
#write error
csv_error = csv.writer(open("studentsContri_talkout_errorusers_20152016_0306.csv", "w", encoding="UTF-8"))

#user talk page revisions
#regular expression to match out the username
import re
talkpageowner_re = re.compile(r'User talk:(.*)/|User talk:(.*)', re.DOTALL)#User talk:(.*)/sandbox|User talk:(.*)/

n=0
for line in info[1::]:
    line = line.strip()
    info_lst = line.split('\t')
    #studentID
    SID = info_lst[1]
    #course
    course = info_lst[2]
    #courseID
    courseID = info_lst[3]
    #return Student
    oldStudent = info_lst[4]
    #get name from names list
    wpid =  info_lst[0]
    wpid = wpid.strip()
    #print (rawID)
    wpid_nospace = wpid.replace(" ","_")
    #decode student's name into ascii
    decode_wpid = urllib.parse.quote(wpid_nospace)
    #quarter time window
    starttime = info_lst[-2]+"T00:00:00Z"
    endtime = info_lst[-1]+"T11:59:59Z"
    
    #API https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User_talk:Averysf&rvuser=Poetries&rvdir=newer&rvprop=timestamp|user|size|comment&rvdir=newer&rvlimit=500
    api_call = ("https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser={}&ucnamespace=3&ucdir=newer&ucstart={}&ucend={}&ucprop=timestamp|title|sizediff|comment&uclimit=500&format=json").format(decode_wpid,starttime,endtime)#Kingsleyta
    response=urllib.request.urlopen(api_call)
    str_response=response.read().decode('utf-8')
    responsedata = json.loads(str_response)
    try: 
        revision_data_lst=responsedata["query"]["usercontribs"]#list
        for feature in revision_data_lst:
            talk_page_title = feature.get('title')
            talk_page_owner1 = re.match(talkpageowner_re, talk_page_title).group(1)
            talk_page_owner2 = re.match(talkpageowner_re, talk_page_title).group(2)
            talk_page_owner_lst=list(set([talk_page_owner1,talk_page_owner2]))
            talk_page_owner = [x for x in talk_page_owner_lst if x is not None][0]
            if wpid != talk_page_owner: #not edit in their own talk page
                csv_f.writerow([wpid, SID,course,courseID,oldStudent,"user_talk", 3, talk_page_title, talk_page_owner, feature['timestamp'], feature.get('sizediff'), feature.get('comment')])
    except KeyError:
        #pass
        csv_error.writerow([wpid, SID,course,courseID,oldStudent,"user_talk", 3, page_title, "no user talk", "no user talk","no user talk","no user talk"])
    n+=1    
    if n%100==0:
        print (n) 


#https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser=Kingsleyta&ucdir=newer&ucnamespace=3&ucprop=title|timestamp|comment|size|sizediff|flags&uclimit=500

#####after manually remove sandbox title
studentContri_talk = pd.read_csv("studentContri_talkout_2015-2016_0306.csv", encoding = "ISO-8859-1")
studentContri_talk.columns.values
drop_index = []
for index, row in studentContri_talk.iterrows():
    if row['wpid'] == row['talkpage_owner']:
        drop_index.append(index)

#drop self editing    
studentContri_talk = studentContri_talk.drop(studentContri_talk.index[drop_index])

#reset index
studentContri_talk = studentContri_talk.reset_index(drop=True)

#drop edit classmates
#leave only wikipedian
drop_index = []
for index, row in studentContri_talk.iterrows():
    if row['talkpage_owner'] in studentList:
        drop_index.append(index)

studentContri_talk = studentContri_talk.drop(studentContri_talk.index[drop_index])
studentContri_talk = studentContri_talk.reset_index(drop=True)

studentContri_talk.to_csv("StudentContri_talkout_Wiki_2015-2016_0306.csv",index=False)

#wikipedians students talked to
wiki_list = list(set(list(studentContri_talk['talkpage_owner'])))
len(wiki_list) #740 student contribute to 740 wikipedians' talk page






##useless
###########################################################
#during semester
students_talk = pd.read_csv("students_talk_2015-2016_0306.csv", encoding = "ISO-8859-1")
students_talk.columns.values

#wikipedians talked to
talk_pair = students_talk[["wpid","talkpage_user"]]#.drop_duplicates()
students_rowindex = []
for i, row in talk_pair.iterrows():
    if row["talkpage_user"] in studentList:
        students_rowindex.append(i)
        
talk_pair = talk_pair.drop(talk_pair.index[students_rowindex])  
talk_pair = talk_pair.drop_duplicates() #talk pair of student and wikipedians     

wiki_list = talk_pair["talkpage_user"].tolist() #Wikipedian list student talked to
user_list = talk_pair["wpid"].tolist() #corresponded student list

#collect the wikipedian talk page edited by students
#Check the user talk page
csv_f = csv.writer(open("wiki_talk_2015-2016_0306.csv", "w"))
#write first row
csv_f.writerow(['wpid_original', 'wikipedian','article','ns','page_title','students', 'timestamp', 'size','comment'])

#user talk page revisions

n=0
for i in range(len(wiki_list)):
    wpid_original =  wiki_list[i]
    sdutent_original = user_list[i]
    #Wikipedians
    wpid = wpid_original.strip()
    wpid_nospace = wpid.replace(" ","_")
    #article = articles[i]
    #decode student's name into ascii
    decode_wpid = urllib.parse.quote(wpid_nospace)
    #Students
    studentid = sdutent_original.strip()
    sid_nospace = studentid .replace(" ","_")
    #article = articles[i]
    #decode student's name into ascii
    decode_sid = urllib.parse.quote(sid_nospace)
    #API https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User_talk:Averysf&rvuser=Poetries&rvdir=newer&rvprop=timestamp|user|size|comment&rvdir=newer&rvlimit=500
    api_call = ("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=User_talk:{}&rvuser={}&rvdir=newer&rvprop=timestamp|user|size|comment&rvlimit=500&format=json").format(decode_wpid,decode_sid)#Kingsleyta
    response=urllib.request.urlopen(api_call)
    str_response=response.read().decode('utf-8')
    responsedata = json.loads(str_response)
    page_id = list(responsedata["query"]["pages"].keys())[0]
    page_title = responsedata['query']['pages'][page_id].get("title")
    try: 
        revision_data_lst=responsedata['query']['pages'][page_id]['revisions']
        for feature in revision_data_lst:
            csv_f.writerow([wpid_original, wpid, "user_talk", 3, page_title, feature.get('user'), feature['timestamp'], feature.get('size'), feature.get('comment')])
    except KeyError:
        pass
        #csv_f.writerow([wpid_original, wpid, "user_talk", 3, page_title, "no user talk", "no user talk","no user talk","no user talk"])
    n+=1    
    if n%100==0:
        print (n) 




















