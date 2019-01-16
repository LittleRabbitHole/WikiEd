#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 12:34:18 2019

@author: angli
"""
import pandas as pd
import pickle
import csv
import numpy as np
import math
import datetime

def WriteOut_Lst2Str2(lst, filename):
    i = 0
    outString = 'control_wpid,register_date,edit_count,ave_sizediff,article_sizediff,article_count,talk_count,user_count,usertalk_count,unique_article_numbers'
    for item in lst:
        str_item = [str(i) for i in item]
        i += 1
        outString += '\n'
        outString += ','.join(str_item)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filename, 'w') as f:
        f.write(outString)
        f.close()


def semesterAggre(dir_file, file):
    data = pd.read_csv(dir_file+file)
    #data.columns.values
    
    aggre_data=[]
    Grouped = data.groupby(['control_wpid', 'register_date'])
    
    n=0
    for pidgroup in Grouped:
        n+=1
        if n%100==0: print (n)
        #if n==2: break
        control_wpid, register_date = pidgroup[0]
        edit_count = len(list(pidgroup[1]['control_wpid']))
        ave_sizediff = pidgroup[1]['sizediff'].mean()
        if math.isnan(ave_sizediff): ave_sizediff = 0
        #ave article size diff
        all_df = pidgroup[1][['ns','sizediff']]
        article_df = all_df.loc[all_df['ns'] == 0]
        article_sizediff = article_df['sizediff'].mean()
        if math.isnan(article_sizediff): article_sizediff = 0
        # article type count
        articleType_list = list(pidgroup[1]['ns'])
        article_count = articleType_list.count(0) #edits in article
        article_index = [i for i in range(len(articleType_list)) if articleType_list[i]==0]
        talk_count = articleType_list.count(1)
        user_count = articleType_list.count(2)
        usertalk_count = articleType_list.count(3)
        #number of articles
        title_lst = list(pidgroup[1]['title'])
        article_lst = list(set([title_lst[j] for j in article_index]))
        unique_article_numbers = len(article_lst)
        #unit data
        pidgroup_data = [control_wpid, register_date, edit_count, ave_sizediff, article_sizediff, article_count, talk_count, user_count, usertalk_count, unique_article_numbers]        
        aggre_data.append(pidgroup_data)
    
    #return    
    return aggre_data        

def Today(row):
    #return as pd.datetime
    #for ind, row in data.iterrows():
    timestamp = row['timestamp']
    if type(timestamp) is str:
        timestamp = pd.to_datetime(timestamp)
        today = pd.to_datetime(timestamp.strftime('%Y-%m-%d'))
        #timedelta = today - pd.to_datetime(row['register_date'])
        #day_index = timedelta.days             
    elif math.isnan(timestamp):
        today = pd.to_datetime(row['register_date'])
    return  today



def TimeDelta(row):
    #for ind, row in data.iterrows():
    timestamp = row['timestamp']
    if type(timestamp) is str:
        timestamp = pd.to_datetime(timestamp)
        #today = pd.to_datetime(timestamp.strftime('%Y-%m-%d'))
        timedelta = timestamp - pd.to_datetime(row['register_date'])
        #day_index = timedelta.days             
    elif math.isnan(timestamp):
        timedelta = pd.to_datetime("2019-01-15") - pd.to_datetime("2019-01-15") #0
    return  timedelta


def LastEdit(row, last_survivalday, max_timedelta):
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



def Death(row, last_survivalday):
    #for ind, row in data.iterrows():
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

    
#2016-05-28T22:24:35Z
def AfterSemesterAggre(dir_file, file):
    data = pd.read_csv(dir_file+file)
    #data.columns.values
    
    data["day_index_timedelta"] = data.apply(TimeDelta, axis=1)
    data["today"] = data.apply(Today, axis=1)
    data['last_day_censored'] = pd.to_datetime("2019-01-15")
    data["last_edit_mark"] = 0
    data["death"] = 0

    aggre_data=[]
    Grouped = data.groupby(['control_wpid', 'register_date'])
    
    n=0
    for pidgroup in Grouped:
        n+=1
        if n%100==0: print (n)
        if n==4: break
        control_wpid, register_date = pidgroup[0]
        
        day_lst = pidgroup[1][['today','day_index_timedelta']]
        first_survivalday = day_lst['today'].iloc[0]
        last_survivalday = day_lst['today'].iloc[-1]
        max_timedelta = day_lst['day_index_timedelta'].max()
        #last edit mark
        pidgroup[1]["last_edit_mark"] = pidgroup[1].apply(LastEdit, axis=1, last_survivalday = last_survivalday, max_timedelta = max_timedelta)
        pidgroup[1]["death"] = pidgroup[1].apply(Death, axis=1, last_survivalday = last_survivalday)
        
        #survival elements
        lastedit_row = pidgroup[1].loc[pidgroup[1]['last_edit_mark'] == 1]
        death = lastedit_row['death']
        dayindex = lastedit_row['day_index_timedelta'].iloc[0].days
        
        #efforts
        edit_count = len(list(pidgroup[1]['control_wpid']))
        ave_sizediff = pidgroup[1]['sizediff'].mean()
        if math.isnan(ave_sizediff): ave_sizediff = 0
        #ave article size diff
        all_df = pidgroup[1][['ns','sizediff']]
        article_df = all_df.loc[all_df['ns'] == 0]
        article_sizediff = article_df['sizediff'].mean()
        if math.isnan(article_sizediff): article_sizediff = 0
        # article type count
        articleType_list = list(pidgroup[1]['ns'])
        article_count = articleType_list.count(0) #edits in article
        article_index = [i for i in range(len(articleType_list)) if articleType_list[i]==0]
        talk_count = articleType_list.count(1)
        user_count = articleType_list.count(2)
        usertalk_count = articleType_list.count(3)
        #number of articles
        title_lst = list(pidgroup[1]['title'])
        article_lst = list(set([title_lst[j] for j in article_index]))
        unique_article_numbers = len(article_lst)
        #unit data
        pidgroup_data = [control_wpid, register_date, edit_count, ave_sizediff, article_sizediff, article_count, talk_count, user_count, usertalk_count, unique_article_numbers]        
        aggre_data.append(pidgroup_data)
    
    #return    
    return aggre_data        


    
if __name__ == "__main__":
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "controlgroup_contributes_semester.csv"
    aggre_data  = semesterAggre(dir_file, file)
    WriteOut_Lst2Str2(aggre_data, dir_file+"controlgroup_semester_contri_aggre.csv")
    
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "controlgroup_contributes_afterSemester.csv"
    aggre_data  = semesterAggre(dir_file, file)
    WriteOut_Lst2Str2(aggre_data, dir_file+"controlgroup_AfterSemester_contri_aggre.csv")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
