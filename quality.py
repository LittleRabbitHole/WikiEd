#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 10:26:12 2019

@author: angli
"""

import pandas as pd
import pickle
import csv
import numpy as np
import math
import datetime
import requests
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
    

def revidStackLst(extendedlst):
    
    revid_stack_list = []
    n=0
    revid_stack = []
    for lst in extendedlst: 
        n+=1
        revids = lst[-2::]
        revid_stack += revids
        if len(revid_stack) == 40:
            revid_stack_clean = [str(x) for x in revid_stack]
            stack50s = "|".join(revid_stack_clean)
            revid_stack_list.append(stack50s)
            revid_stack = []
        elif n == len(extendedlst):
            revid_stack_clean = [str(x) for x in revid_stack]
            stacklast = "|".join(revid_stack_clean)
            revid_stack_list.append(stacklast)
            revid_stack = []

    return revid_stack_list


def articleQualityDict(artlestacks):
    '''
    input as list of article stacks
    output as dictionary: revid: quality
    '''
    final_dict = {}
    #len(final_dict.keys())
    n=0
    for stack in students_stackedrevids:
        n+=1
        if n%10==0: print(n)
        revids = stack.split("|")
        url = "https://ores.wmflabs.org/v3/scores/enwiki/?models=wp10&revids="+stack
        stackresult = articleQualityWP10(url)
        for revid in revids:
            final_dict[revid] = stackresult.get(revid)
        
    
    
          
def articleQualityWP10(url):
    '''
    input quality url, 
    output cleaned
    '''
    #https://en.wikipedia.org/w/index.php?oldid=680285575
    #https://ores.wmflabs.org/v3/scores/enwiki/?models=wp10&revids=713578318|722330091
    response=requests.get(url)
    responsedata = returnJsonCheck(response)
    results = responsedata['enwiki']['scores']
    return results



if __name__ == "__main__":
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    studentfile = "students_contributes_semester.csv"
    controlfile = "controlgroup_contributes_semester.csv"
    alltimepoint = "control_students_all.csv"
    
    control_students_df = pd.read_csv(dir_file+alltimepoint)
    control_students_df = control_students_df[['startcontrol_userid', 'startcontrol_registerdate', 'enddate']].drop_duplicates()
    control_students_df.columns = ['control_userid', 'register_date', 'enddate']
    
    student_allcontri = pd.read_csv(dir_file+studentfile)
    student_allcontri = student_allcontri.loc[student_allcontri['ns'] == 0]
    students_articles = student_allcontri[['title', 'startdate', 'enddate','student_courseID']].drop_duplicates()
    students_articleextend_lst = articleRevision(students_articles) 
    #['title', 'startdate', 'enddate','student_courseID', 'pageid', 'parent_start', 'start_revid', 'end_revid']
    pickle.dump( students_articleextend_lst, open( dir_file+"students_articlelst_forquality.p", "wb" ) )
    students_stackedrevids = revidStackLst(students_articleextend_lst)
    
    
    control_allcontri = pd.read_csv(dir_file+controlfile)
    control_allcontri = control_allcontri.loc[control_allcontri['ns'] == 0]
    control_allcontri = pd.merge(control_allcontri, control_students_df, how = 'left', on = ['control_userid', 'register_date'])
    control_articles = control_allcontri[['title', 'register_date', 'enddate']].drop_duplicates()
    control_articles['register_date'] = pd.to_datetime(control_articles['register_date'])
    control_articles['enddate'] = pd.to_datetime(control_articles['enddate'])
    control_articles['register_date'] = control_articles['register_date'].dt.strftime('%Y-%m-%d')
    control_articles['enddate'] = control_articles['enddate'].dt.strftime('%Y-%m-%d')
    control_articleextend_lst = articleRevision(control_articles)
    #['title', 'startdate', 'enddate','pageid', 'parent_start', 'start_revid', 'end_revid']
    pickle.dump( control_articleextend_lst, open( dir_file+"control_articlelst_forquality.p", "wb" ) )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    