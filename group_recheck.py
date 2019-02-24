#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 20:00:22 2019

@author: jiajunluo
"""

import pandas as pd

dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
file = "students_contributes_semester.csv"

data = pd.read_csv(dir_file+file)

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
    
wikied_group = {}
for title, wikied_lst in article_dict.items():
    if len(list(set(wikied_lst))) > 1:
        for wikied in wikied_lst:
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
        studentdata.at[ind, 'group_recheck'] = None
    
studentdata.to_csv(dir_file+"fullstudentset_updatedgroup.csv", index=False)



















       