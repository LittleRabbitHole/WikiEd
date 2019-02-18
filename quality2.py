#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 11:54:16 2019

@author: angli
"""

import pandas as pd
import pickle
import csv
import numpy as np
import math
import datetime
import requests
from collections import Counter
from utilities import GetPageRevision
from utilities import returnJsonCheck

def articleRevision(articles):
    """
    input articles as df, columns as: ['title', 'startdate', 'enddate','student_courseID']
    output two article df, columns as: ['title', 'startdate', 'enddate','student_courseID', 'pageid', 'parent_start', 'start_revid', 'end_revid'] 
    with timepoint revision ids: start_revid, end_revid
    """
    df = articles
    articles_extended = []
    n=0
    for ind, row in df.iterrows():
        n+=1
        if n%100==0: print(n)
        
        row_lst = list(row)
        title = row_lst[0]
        startdate = row_lst[1]
        enddate = row_lst[2]
        starttime = startdate+"T00:00:00Z"
        endtime = enddate+"T00:00:00Z"
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json&rvdir=newer&rvlimit=500&prop=revisions&rvstart={}&rvend={}&rvprop=ids|timestamp|user|userid&titles={}".format(starttime, endtime, title)
        pageid, contri_lst = GetPageRevision(url)
        if len(contri_lst)>0:
            firstparent = contri_lst[0]['parentid']
            first = contri_lst[0]['revid']
            last = contri_lst[-1]['revid']
            articleinfo_lst = row_lst + [pageid, firstparent, first, last]
            articles_extended.append(articleinfo_lst)
        else:
            articleinfo_lst = row_lst + [pageid, None, None, None]
    return articles_extended


def timedict(timepoint_df, student_df):
    
    alltimepoints = {}
    for ind, row in student_df.iterrows():
        student_wpid, student_start, student_end = row['student_userid'], row['startdate'], row['enddate'] 
        alltimepoints[student_wpid] = [student_start, student_end]
    
    for ind, row in timepoint_df.iterrows():
        control_wpid, control_start, control_end = row['startcontrol_userid'], row['startdate'], row['enddate']
        alltimepoints[control_wpid] = [control_start, control_end]
    
    return alltimepoints


if __name__ == "__main__":
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    studentfile = "students_contributes_semester.csv"
    articlefile = "duringSocializationQuality_uniqueArticleUnit2.csv"
    alltimepoint = "control_students_all.csv"
    
    student_allcontri = pd.read_csv(dir_file+studentfile)
    student_df = student_allcontri[['student_username', 'student_userid', 'student_courseID','startdate', 'enddate']].drop_duplicates()
    
    timepoint_df = pd.read_csv(dir_file+alltimepoint)
    timepoint_df.columns.values
    
    timepoints_dict = timedict(timepoint_df, student_df)
    
    #collect article revision data
    articledata_df = pd.read_csv(dir_file+articlefile)
    articledata_df.columns.values
    
    
    
    
    
