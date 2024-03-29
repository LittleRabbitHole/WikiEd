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
    #outString = 'control_wpid,register_date,edit_count,ave_sizediff,article_sizediff,article_sizeadded,article_count,talk_count,user_count,usertalk_count,unique_article_numbers'
    #outString = 'control_wpid,register_date,death,dayindex,edit_count,ave_sizediff,article_sizediff,article_count,talk_count,user_count,usertalk_count,unique_article_numbers'
    #outString = 'student_username,student_courseID,startdate,enddate,edit_count,ave_sizediff,article_sizediff,article_sizeadded,article_count,talk_count,user_count,usertalk_count,unique_article_numbers'
    outString = 'student_username,student_courseID,startdate,enddate,death,dayindex,edit_count,ave_sizediff,article_sizediff,article_count,talk_count,user_count,usertalk_count,unique_article_numbers'
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


def ControlSemesterAggre(dir_file, file):
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
        article_sizeadded = article_df['sizediff'].sum()
        if math.isnan(article_sizeadded): article_sizeadded = 0
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
        pidgroup_data = [control_wpid, register_date, edit_count, ave_sizediff, article_sizediff, article_sizeadded, article_count, talk_count, user_count, usertalk_count, unique_article_numbers]        
        aggre_data.append(pidgroup_data)
    
    #return    
    return aggre_data        


def StudentSemesterAggre(dir_file, file):
    data = pd.read_csv(dir_file+file)
    #data.columns.values
    
    aggre_data=[]
    Grouped = data.groupby(['student_username', 'student_courseID', 'startdate','enddate'])
    #Grouped.ngroups
    
    n=0
    for pidgroup in Grouped:
        n+=1
        if n%100==0: print (n)
        #if n==2: break
        student_username, student_courseID, startdate, enddate = pidgroup[0]
        
        edit_count = len(list(pidgroup[1]['student_username']))
        ave_sizediff = pidgroup[1]['sizediff'].mean()
        if math.isnan(ave_sizediff): ave_sizediff = 0
        #ave article size diff
        all_df = pidgroup[1][['ns','sizediff']]
        article_df = all_df.loc[all_df['ns'] == 0]
        article_sizediff = article_df['sizediff'].mean()
        if math.isnan(article_sizediff): article_sizediff = 0
        article_sizeadded = article_df['sizediff'].sum()
        if math.isnan(article_sizeadded): article_sizeadded = 0
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
        pidgroup_data = [student_username, student_courseID, startdate, enddate, edit_count, ave_sizediff, article_sizediff, article_sizeadded, article_count, talk_count, user_count, usertalk_count, unique_article_numbers]        
        aggre_data.append(pidgroup_data)
    
    #return    
    return aggre_data 



def Today(row, setdate_colname = 'register_date'):
    #return as pd.datetime
    #for ind, row in data.iterrows():
    timestamp = row['timestamp']
    if type(timestamp) is str:
        timestamp = pd.to_datetime(timestamp)
        today = pd.to_datetime(timestamp.strftime('%Y-%m-%d'))
        #timedelta = today - pd.to_datetime(row['register_date'])
        #day_index = timedelta.days             
    elif math.isnan(timestamp):
        today = pd.to_datetime(row[setdate_colname])
    return  today



def TimeDelta(row, countfromdate_colname):
    #output (edit time - register date) as pd.timedelta
    timestamp = row['timestamp']
    if type(timestamp) is str:
        timestamp = pd.to_datetime(timestamp)
        #today = pd.to_datetime(timestamp.strftime('%Y-%m-%d'))
        timedelta = timestamp - pd.to_datetime(row[countfromdate_colname])#'register_date'
        #day_index = timedelta.days             
    elif math.isnan(timestamp):
        timedelta = pd.to_datetime("2019-01-15") - pd.to_datetime("2019-01-15") #0
    return  timedelta


def LastEdit(row, last_survivalday, max_timedelta):
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



def Death(row, last_survivalday):
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

 
def survivalManipulate(dir_file, file, cutdate = "2017-06-01"):
    data = pd.read_csv(dir_file+file)
    data["today"] = data.apply(Today, setdate_colname = 'enddate', axis=1)#as datetime
    cutdate_dt = pd.to_datetime(cutdate)
       
    data = data.loc[data["today"] < cutdate_dt]
    return data
    

#2016-05-28T22:24:35Z
#Control--after semester aggregation with survival information
def ControlAfterSemesterAggre(dir_file, file):
    data = pd.read_csv(dir_file+file)
    #data.columns.values
    
    data["day_index_timedelta"] = data.apply(TimeDelta, countfromdate_colname='register_date', axis=1)#as timedelta
    data["today"] = data.apply(Today, setdate_colname = 'register_date', axis=1)#as datetime
    data['last_day_censored'] = pd.to_datetime("2019-01-15")
    #data["last_edit_mark"] = 0
    #data["death"] = 0

    aggre_data=[]
    Grouped = data.groupby(['control_wpid', 'register_date'])
    #Grouped.ngroups
    
    n=0
    for pidgroup in Grouped:
        n+=1
        if n%50==0: print (n)
        #if n==4: break
        control_wpid, register_date = pidgroup[0]
        
        day_lst = pidgroup[1][['today','day_index_timedelta']]
        first_survivalday = day_lst['today'].iloc[0]
        last_survivalday = day_lst['today'].iloc[-1]
        max_timedelta = day_lst['day_index_timedelta'].max()#last edit time - register time
        #last edit mark
        pidgroup[1]["last_edit_mark"] = pidgroup[1].apply(LastEdit, axis=1, last_survivalday = last_survivalday, max_timedelta = max_timedelta)
        pidgroup[1]["death"] = pidgroup[1].apply(Death, axis=1, last_survivalday = last_survivalday)
        
        #survival elements
        lastedit_row = pidgroup[1].loc[pidgroup[1]['last_edit_mark'] == 1]
        death = list(lastedit_row['death'])[0]
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
        pidgroup_data = [control_wpid, register_date, death, dayindex, edit_count, ave_sizediff, article_sizediff, article_count, talk_count, user_count, usertalk_count, unique_article_numbers]        
        aggre_data.append(pidgroup_data)
    
    #return    
    return aggre_data        


#Student--after semester aggregation with survival information
#def StudentAfterSemesterAggre(dir_file, file, last_day_censored = "2019-01-15"):
#    data = pd.read_csv(dir_file+file)
    #data.columns.values
def StudentAfterSemesterAggre(data, last_day_censored = "2019-01-15"):    
    data['register_date'] = data['enddate']
    data["day_index_timedelta"] = data.apply(TimeDelta, countfromdate_colname='enddate', axis=1)#as timedelta
    data["today"] = data.apply(Today, setdate_colname = 'register_date', axis=1)#as datetime
    data['last_day_censored'] = pd.to_datetime(last_day_censored)
    #data = data.loc[data["day_index_timedelta"]>pd.Timedelta('0 days')]
    #data["last_edit_mark"] = 0
    #data["death"] = 0

    aggre_data=[]
    Grouped = data.groupby(['student_username', 'student_courseID', 'startdate','enddate'])
    Grouped.ngroups
    
    n=0
    for pidgroup in Grouped:
        n+=1
        if n%50==0: print (n)
        #if n==4: break
        student_username, student_courseID, startdate, enddate = pidgroup[0]
        
        day_lst = pidgroup[1][['today','day_index_timedelta']]
        first_survivalday = day_lst['today'].iloc[0]
        last_survivalday = day_lst['today'].iloc[-1]
        max_timedelta = day_lst['day_index_timedelta'].max()#last edit time - register time
        #last edit mark
        pidgroup[1]["last_edit_mark"] = pidgroup[1].apply(LastEdit, axis=1, last_survivalday = last_survivalday, max_timedelta = max_timedelta)
        pidgroup[1]["death"] = pidgroup[1].apply(Death, axis=1, last_survivalday = last_survivalday)
        
        #survival elements
        lastedit_row = pidgroup[1].loc[pidgroup[1]['last_edit_mark'] == 1]
        death = list(lastedit_row['death'])[0]
        dayindex = lastedit_row['day_index_timedelta'].iloc[0].days
        
        #efforts
        edit_count = len(list(pidgroup[1]['student_username']))
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
        pidgroup_data = [student_username, student_courseID, startdate, enddate, death, dayindex, edit_count, ave_sizediff, article_sizediff, article_count, talk_count, user_count, usertalk_count, unique_article_numbers]        
        aggre_data.append(pidgroup_data)
    
    #return    
    return aggre_data  
       
    
    


    
if __name__ == "__main__":
    #during semester effort
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "controlgroup_contributes_semester.csv"
    aggre_data  = ControlSemesterAggre(dir_file, file)
    WriteOut_Lst2Str2(aggre_data, dir_file+"controlgroup_semester_contri_aggre_v2.csv")

    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    #dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "students_contributes_semester.csv"
    aggre_data  = StudentSemesterAggre(dir_file, file)
    WriteOut_Lst2Str2(aggre_data, dir_file+"student_semester_contri_aggre_v2.csv")

    #after semester + survival
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "controlgroup_contributes_afterSemester.csv"
    aggre_data  = ControlAfterSemesterAggre(dir_file, file)
    WriteOut_Lst2Str2(aggre_data, dir_file+"controlgroup_AfterSemester_contri_aggre.csv")
    
    #censor date = 2019-01-15
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "students_contributes_aftersemester.csv"
    aggre_data  = StudentAfterSemesterAggre(dir_file, file)
    WriteOut_Lst2Str2(aggre_data, dir_file+"students_AfterSemester_contri_aggre_v2.csv")
    
    #change censor date
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "students_contributes_aftersemester.csv"   
    data = survivalManipulate(dir_file, file, cutdate = "2017-01-01")    
    aggre_data  = StudentAfterSemesterAggre(data, last_day_censored = "2017-01-01")
    WriteOut_Lst2Str2(aggre_data, dir_file+"students_AfterSemester_contri_aggre_censor_170101.csv")
    
    #semester control survival
#    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
#    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
#    file = "controlgroup_contributes_semester_survival.csv"
#    aggre_data  = ControlAfterSemesterAggre(dir_file, file)
#    WriteOut_Lst2Str2(aggre_data, dir_file+"controlgroup_semester_survival_aggre.csv")
    
#    #student survival
#    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
#    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
#    file = "students_contributes_semester_survival.csv" #original file
#    aggre_data  = StudentAfterSemesterAggre(dir_file, file)
#    WriteOut_Lst2Str2(aggre_data, dir_file+"student_semester_survival_aggre_v2.csv")
#    
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
