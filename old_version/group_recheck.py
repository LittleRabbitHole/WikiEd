#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 20:00:22 2019

@author: jiajunluo
"""

import pandas as pd
from collections import Counter

dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
file = "students_contributes_semester.csv"
coureseInfofile = "2015_2016_student_courses_list.csv"


f = open(dir_file+coureseInfofile, 'r')
courseinfo = f.readlines()
f.close()

course_dict = {}
for line in courseinfo[1::]:
    lst = line.split(",")
    wikied = lst[0]
    courseID = lst[2]
    if wikied in course_dict.keys():
        course_dict[wikied].append(courseID)
    else:
        course_dict[wikied] = [courseID]
    

file = "controlgroup_contributes_afterSemester.csv"
file = "controlgroup_contributes_semester.csv"

data = pd.read_csv(dir_file+file)

###check teahouse
check_data = data[['control_wpid', 'control_userid']].loc[data['title'].str.contains("Wikipedia:Teahouse|Wikipedia talk:Teahouse")==True].drop_duplicates()
#Wikipedia:Teahouse; Wikipedia talk:Teahouse

check_data = data[['control_wpid', 'control_userid']].loc[data['title'].str.contains("Wikipedia:Teahouse|Wikipedia talk:Teahouse")==True].drop_duplicates()

article_data = data[['student_username', 'student_userid', 'student_courseID', 'ns', 'title']].loc[data['ns']==0]
article_data = article_data.drop_duplicates()

article_dict = {}
n=0
for ind, row in article_data.iterrows():
    n+=1
    title = row['title']
    wikied = row['student_username']
    if title in article_dict.keys():
        article_dict[title].append(wikied)
    else:
        article_dict[title] = [wikied]
    

def countThresh(count_dict, n=1):
    for k in count_dict.items():
        if k[1] <= 1:
            print (k)
            del count_dict[k]
    return count_dict

from itertools import dropwhile

def cutthreshold(main_dict, n):
    for key, count in dropwhile(lambda key_count: key_count[1] > n, main_dict.most_common()):
        del main_dict[key]
    return main_dict

def returnIDX(groupcourse, courseid):
    IDX = []
    for i in range(len(courseid)):
        item = courseid[i]
        if len(list(set(item) & set(groupcourse))) > 0:
            #print (item)
            IDX.append(i)
    return IDX    

wikied_group = {}
n=0
for title, wikied_lst in article_dict.items():
    n+=1
    if n==2: break
    if len(list(set(wikied_lst))) > 1:
        courseid = [course_dict.get(wikied) for wikied in  wikied_lst]
        count_dict = Counter([t for cell in courseid for t in cell])
        groupcourse = list(cutthreshold(count_dict, n=1).keys())
        groupWikiedIDX = returnIDX(groupcourse, courseid)
        wikied_lst_group = [wikied_lst[i] for i in groupWikiedIDX]
        for wikied in wikied_lst_group:
            wikied_group[wikied] = 1
    else:
        for wikied in wikied_lst:
            if wikied in wikied_group.keys():
                pass
            else:
                wikied_group[wikied] = -1

                
studentdata = pd.read_csv(dir_file+"fullstudentset_group.csv")
studentdata["group_recheck"] = 0
for ind, row in studentdata.iterrows():
    wikied = row['student_wpid']
    try:
        groupinfo = wikied_group[wikied]
        studentdata.at[ind, 'group_recheck'] = groupinfo
    except:
        studentdata.at[ind, 'group_recheck'] = row['indiv_group']
    
studentdata.to_csv(dir_file+"fullstudentset_updatedgroup.csv", index=False)



















       