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

def articleQualityWP10(url):
    '''
    input quality url, 
    output cleaned model score
    '''
    #https://en.wikipedia.org/w/index.php?oldid=680285575
    #https://ores.wmflabs.org/v3/scores/enwiki/?models=wp10&revids=713578318|722330091
    response=requests.get(url)
    responsedata = returnJsonCheck(response)
    results = responsedata['enwiki']['scores']
    return results



def articleQualityDict(article_stackedrevids):
    '''
    input as list of article stacks
    output as dictionary: revid: quality
    '''
    final_dict = {}
    #len(final_dict.keys())
    n=0
    for stack in article_stackedrevids:
        n+=1
        if n%10==0: print(n)
        revids = stack.split("|")
        url = "https://ores.wmflabs.org/v3/scores/enwiki/?models=wp10&revids="+stack
        stackresult = articleQualityWP10(url)
        for revid in revids:
            final_dict[revid] = stackresult.get(revid)
    return final_dict


def finalScore(scoresProb_dict):
    '''
    this is to calculate the final score based on the wp10 probability
    '''
    matching = {
            'Stub': 1,
            'Start': 2,
            'C': 3,
            'B': 4,
            'FA': 6,
            'GA': 5
            }
    try:
        prediction = scoresProb_dict['wp10']['score']['prediction']
        probs = scoresProb_dict['wp10']['score']['probability']
        
        predicted_score = matching[prediction]
        predicted_prob = probs[prediction]
        
        B = probs['B']
        C = probs['C']
        FA = probs['FA']
        GA = probs['GA']
        Start = probs['Start']
        Stub = probs['Stub']
        
        aggre_score = 1*Stub + 2*Start + 5*GA + 6*FA + 3*C + 4*B
    except KeyError:
        predicted_score = None 
        predicted_prob = None
        aggre_score = None
    return (predicted_score, predicted_prob, aggre_score)
    
          
def attachRevidScores(articleextend_lst, score_dict):
    #geiven revid, find score from score_dict
    articleextend_scores_lsts = []
    for article in articleextend_lst:
        revid0 = str(article[-2])
        score_revid0 = score_dict[revid0]
        revid0_predicted, revid0_predicted_prob, revid0_aggre_score = finalScore(score_revid0)
        revid1 = str(article[-1])
        score_revid1 = score_dict[revid1]
        revid1_predicted, revid1_predicted_prob, revid1_aggre_score = finalScore(score_revid1)
        article_score_lst = article + [revid0_predicted, revid0_predicted_prob, revid0_aggre_score, revid1_predicted, revid1_predicted_prob, revid1_aggre_score]
        articleextend_scores_lsts.append(article_score_lst)
    return articleextend_scores_lsts


def courseInfoDict(dir_file, coureseInfofile):
    file = open(dir_file+coureseInfofile, "r")
    lines = file.readlines()
    file.close()
    
    courseDict = {}
    for line in lines[1:]:
        line = line.strip()
        line_lst = line.split(",")
        courseDict[line_lst[0]] = line_lst[1:]
    return courseDict    
    
    
def article_author(df):
    '''
    attribute article with an author who made the most contribution within the semester
    also return total # of authors for this article
    '''
    article_author_dict = {}
    articlegrouped = df.groupby('title')
    n=0
    for articlegroup in articlegrouped:
        n+=1
        if n%100==0: print (n)
        #if n==2: break
        title = articlegroup[0]
        userids_lst = [str(int(x)) for x in list(articlegroup[1]['userid'])]
        userid, times = Counter(userids_lst).most_common(1)[0]
        author = userid
        proportion = times/len(userids_lst)
        article_author_dict[title] = [author, proportion]
    return article_author_dict


def article_author_lst(df):
    '''
    article -- author list.
    find all authors for this article
    '''
    article_author_dict = {}
    articlegrouped = df.groupby('title')
    n=0
    for articlegroup in articlegrouped:
        n+=1
        if n%100==0: print (n)
        #if n==2: break
        title = articlegroup[0]
        userids_lst = [str(int(x)) for x in list(articlegroup[1]['userid'])]
        userids_lst = list(set(userids_lst))
        #userid, times = Counter(userids_lst).most_common(1)[0]
        #author = userid
        #proportion = times/len(userids_lst)
        article_author_dict[title] = userids_lst
    return article_author_dict



def article_author2(df):
    '''
    attribute each editor with an article who made the most contribution within the semester
    '''
    article_author_dict = {}
    usergrouped = df.groupby(['username', 'startdate'])
    n=0
    for group in usergrouped:
        n+=1
        if n%100==0: print (n)
        #if n==2: break
        username, startdate = group[0]
        title_lst = list(group[1]['title'])
        article, times = Counter(title_lst).most_common(1)[0]
        author = str(username)
        proportion = times/len(title_lst)
        article_author_dict[(author,startdate)] = [article, proportion]
    return article_author_dict

if __name__ == "__main__":
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    studentfile = "students_contributes_semester.csv"
    controlfile = "controlgroup_contributes_semester.csv"
    alltimepoint = "control_students_all.csv"
    coureseInfofile = "student_course_info.csv"
        
    #control, student list
    control_students_df = pd.read_csv(dir_file+alltimepoint)
    control_students_df = control_students_df[['startcontrol_userid', 'startcontrol_registerdate', 'enddate']].drop_duplicates()
    control_students_df.columns = ['control_userid', 'register_date', 'enddate']
    
    #handel students
    student_allcontri = pd.read_csv(dir_file+studentfile)
    student_allcontri = student_allcontri.loc[student_allcontri['ns'] == 0]
    student_articles_df = student_allcontri[['student_username', 'student_userid', 'student_courseID','title','startdate']].drop_duplicates()
    student_articles_df.columns = ['username','userid', 'courseid','title','startdate']
    student_articles_df['username'] = student_articles_df['username'].apply(str)
    student_articles_df['userid'] = student_articles_df['userid'].apply(int).apply(str)
    
    ##make article author for future use:
    student_articlesauthor_dict =  article_author(student_articles_df) #article-student
    student_articles_authorlist_dict = article_author_lst(student_articles_df)
    student_author_dict = article_author2(student_articles_df) #student-article
    
                                              
    students_articles = student_allcontri[['title', 'startdate', 'enddate','student_courseID']].drop_duplicates()
    
    ###this part is done
    #students_articleextend_lst = articleRevision(students_articles) 
    #['title', 'startdate', 'enddate','student_courseID', 'pageid', 'parent_start', 'start_revid', 'end_revid']
    #pickle.dump( students_articleextend_lst, open( dir_file+"students_articlelst_forquality.p", "wb" ) )
    
    #students info with 4 time points, and 2 time scores
    students_articleextend_lst = pickle.load( open( dir_file+"students_articlelst_forquality.p", "rb" ) ) 
    students_stackedrevids = revidStackLst(students_articleextend_lst)
    
    #collect the quality score
    #student_score_dict = articleQualityDict(students_stackedrevids)
    #pickle.dump( student_score_dict, open( dir_file+"student_score_dict.p", "wb" ) ) 

    student_score_dict = pickle.load( open( dir_file+"student_score_dict.p", "rb" ) )      
    student_articlescores = attachRevidScores(students_articleextend_lst, student_score_dict)
    #['title', 'startdate', 'enddate','student_courseID', 'pageid', 'parent_start', 'start_revid', 'end_revid', revid0_predicted, revid0_predicted_prob, revid0_aggre_score, revid1_predicted, revid1_predicted_prob, revid1_aggre_score]
    
    #make this into dictionary: (title, startdate) - scores
    student_article_scores = {}
    for item in student_articlescores:
        key = (item[0], item[1])
        pageid = [item[4]]
        scores = item[-6::]
        student_article_scores[key] = pageid + scores
    
    
    ###make a dict for use: articletitle-score
#    student_articlescore_dict = {}
#    for studentarticle in student_articlescores:
#        title = studentarticle[0]
#        pageid = studentarticle[4]
#        courseid = studentarticle[3]
#        start_quality = studentarticle[-6]
#        start_quality_prob = studentarticle[-5]
#        end_quality = studentarticle[-3]
#        end_quality_prob = studentarticle[-2]
#        student_articlescore_dict[title] = [pageid, courseid,start_quality,start_quality_prob,end_quality,end_quality_prob]
#   
#    pickle.dump( student_articlescore_dict, open( dir_file+"student_articlescore_dict.p", "wb" ) )  
    
    student_articlescore_dict = pickle.load(open(dir_file+"student_articlescore_dict.p", "rb"))
    
    ########
    #handel controls
    control_allcontri = pd.read_csv(dir_file+controlfile)
    control_allcontri = control_allcontri.loc[control_allcontri['ns'] == 0]
    control_allcontri = pd.merge(control_allcontri, control_students_df, how = 'left', on = ['control_userid', 'register_date'])
    control_articles_df = control_allcontri[['control_wpid', 'control_userid', 'title', 'register_date']].drop_duplicates()
    control_articles_df.columns = ['username','userid', 'title', 'startdate']
    control_articles_df['startdate'] = pd.to_datetime(control_articles_df['startdate']).dt.strftime('%Y-%m-%d')
    control_articles_df['username'] = control_articles_df['username'].apply(int).apply(str)
    control_articles_df['userid'] = control_articles_df['userid'].apply(int).apply(str)
    
    ##for future use:
    ##make article author:
    control_articlesauthor_dict =  article_author(control_articles_df) #article-control  
    control_articles_authorlist_dict =  article_author_lst(control_articles_df) #article-control-list of authors  
    ##control-article dictionary
    control_author_dict = article_author2(control_articles_df) #control-article
   
    
    control_articles = control_allcontri[['title', 'register_date', 'enddate']].drop_duplicates()
    control_articles['register_date'] = pd.to_datetime(control_articles['register_date'])
    control_articles['enddate'] = pd.to_datetime(control_articles['enddate'])
    control_articles['register_date'] = control_articles['register_date'].dt.strftime('%Y-%m-%d')
    control_articles['enddate'] = control_articles['enddate'].dt.strftime('%Y-%m-%d')
    control_articleextend_lst = articleRevision(control_articles)
    #['title', 'startdate', 'enddate','pageid', 'parent_start', 'start_revid', 'end_revid']
    pickle.dump( control_articleextend_lst, open( dir_file+"control_articlelst_forquality.p", "wb" ) )
    
    #control info with 4 time points, and 2 time scores
    control_articleextend_lst = pickle.load( open( dir_file+"control_articlelst_forquality.p", "rb" ) ) 
    
    ###this part is done
    #control_stackedrevids = revidStackLst(control_articleextend_lst)
    #collect the quality score
    #control_score_dict2 = articleQualityDict(control_stackedrevids)
    #pickle.dump( control_score_dict2, open( dir_file+"control_score_dict2.p", "wb" ) ) 
    
    control_score_dict = pickle.load( open( dir_file+"control_score_dict2.p", "rb" ) )      
    control_articlescores = attachRevidScores(control_articleextend_lst, control_score_dict)
    #['title', 'startdate', 'enddate', 'pageid', 'parent_start', 'start_revid', 'end_revid', revid0_predicted, revid0_predicted_prob, revid0_aggre_score, revid1_predicted, revid1_predicted_prob, revid1_aggre_score]
    
    #make this into dictionary: (title, startdate) - scores
    control_article_scores = {}
    for item in control_articlescores:
        key = (item[0], item[1])
        pageid = [item[3]]
        scores = item[-6::]
        control_article_scores[key] = pageid + scores
    
    ####set the date together######
    #use of
#    student_author_dict
#    student_article_scores    
#    control_author_dict
#    control_article_scores

    ##this is the format as unit analysis = editor
    file = open(dir_file+"duringSemesterStudentControlList.csv", "r")
    alleditors = file.readlines()
    file.close()
    
    finalscorelist = []
    for item in alleditors[1::]:
        itemlst = item.strip().split(",")
        control = itemlst[-2]
        username = itemlst[0]
        startdate = itemlst[3]
        if control == '1':
            title = student_author_dict.get((username,startdate))
            if title is not None:
                scores = student_article_scores.get((title[0],startdate))
            else:
                title = 2*[""]
                scores = 6*[""]
        else:
            title = control_author_dict.get((username,startdate))
            if title is not None:
                scores = control_article_scores.get((title[0],startdate))
            else:
                title = 2*[""]
                scores = 6*[""]
        if scores is None:
            scores = 6*[""]
        itemlst_extend =  itemlst + title + scores   
        finalscorelist.append(itemlst_extend)


    i = 0
    outString = '"control_wpid","courseID","key","startdate","article_count","unique_article_numbers","group","class_size","control_wikied","indiv_group","title","author_prop","pageid","start_quallevel","start_quallevel_prob","start_qual_aggre","end_quallevel","end_quallevel_prob","end_qual_aggre"'
    for lst in finalscorelist:
        i += 1
        strlst = ['"{}"'.format(str(x)) for x in lst]
        outString += '\n'
        outString += ','.join(strlst)
                
    with open(dir_file+"quality3.csv", 'w') as f:
        f.write(outString)
        f.close()




        
    ####set the date together######
    ##this is the format as unit analysis = article
    #course info dictionary
    courseDict = courseInfoDict(dir_file, coureseInfofile)
    #add course info to students using #courseDict
    final_article_score_lst = []
    
    for studentline in student_articlescores:
        title = studentline[0]
        author = student_articlesauthor_dict[title]
        pageid = studentline[4]
        coureseId = str(studentline[3])
        courseinfo = courseDict[coureseId] #[group, classsize]
        scores = studentline[-6:]
        student_article_scores = [title, pageid, coureseId] + author + courseinfo + scores
        final_article_score_lst.append(student_article_scores)
    
    for controlline in control_articlescores:
        title = controlline[0]
        author = control_articlesauthor_dict[title]
        pageid = controlline[3]
        courseinfo = ["-1", "1"] #[group, classsize]
        scores = controlline[-6:]
        control_article_scores = [title, pageid, ""] + author + courseinfo + scores
        final_article_score_lst.append(control_article_scores)
    
    
    unique_data = [list(x) for x in set(tuple(x) for x in final_article_score_lst)]
    pickle.dump( unique_data, open( dir_file+"final_article_score_lst.p", "wb" ) )
    unique_data = pickle.load( open( dir_file+"final_article_score_lst.p", "rb" ) ) 
    #'title,pageid,group,classsize,start_quallevel,start_quallevel_prob,start_qual_aggre,end_quallevel,end_quallevel_prob,end_qual_aggre'
    
    i = 0
    outString = 'pageid,courseId,author,author_prop,group,classsize,start_quallevel,start_quallevel_prob,start_qual_aggre,end_quallevel,end_quallevel_prob,end_qual_aggre'
    for lst in unique_data:
        i += 1
        strlst = [str(x) for x in lst[1:]]
        outString += '\n'
        outString += ','.join(strlst)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(dir_file+"quality.csv", 'w') as f:
        f.write(outString)
        f.close()
    
    
    ####article-authors matching######
    courseDict = courseInfoDict(dir_file, coureseInfofile)
    #add course info to students using #courseDict
    article_authors_lst = []
    
    for studentline in student_articlescores:
        title = studentline[0]
        mainauthor = student_articlesauthor_dict[title]
        authorlist = ["||".join(student_articles_authorlist_dict[title])]
        pageid = studentline[4]
        coureseId = str(studentline[3])
        courseinfo = courseDict[coureseId] #[group, classsize]
        scores = studentline[-6:]
        student_article_scores = [title, pageid, coureseId] + mainauthor + courseinfo + scores + authorlist
        article_authors_lst.append(student_article_scores)
    
    for controlline in control_articlescores:
        title = controlline[0]
        mainauthor = control_articlesauthor_dict[title]
        authorlist = ["||".join(control_articles_authorlist_dict[title])]
        pageid = controlline[3]
        courseinfo = ["-1", "1", "0"] #[group, classsize]
        scores = controlline[-6:]
        control_article_scores = [title, pageid, ""] + mainauthor + courseinfo + scores + authorlist
        article_authors_lst.append(control_article_scores)
    
    
    unique_data = [list(x) for x in set(tuple(x) for x in article_authors_lst)]
    #'title,pageid,group,classsize,start_quallevel,start_quallevel_prob,start_qual_aggre,end_quallevel,end_quallevel_prob,end_qual_aggre'


    
    i = 0
    outString = 'pageid,courseId,author,author_prop,group,classsize,group_ind,start_quallevel,start_quallevel_prob,start_qual_aggre,end_quallevel,end_quallevel_prob,end_qual_aggre,authorlst'
    for lst in unique_data:
        i += 1
        strlst = [str(x) for x in lst[1:]]
        outString += '\n'
        outString += ','.join(strlst)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(dir_file+"quality_authorlist.csv", 'w') as f:
        f.write(outString)
        f.close()
   
    
    
def quality():
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/datafanalysis/"
    file = "duringSocializationQuality_uniqueArticleUnit.csv"
    
    data = pd.read_csv(dir_file+file)
    data.columns.values
    
    article_author_alllist = []
    articlegrouped = data.groupby(["pageid","author","courseID","author_prop","group","control_wikied","indiv_group","classsize"])
    
    n=0
    for articlegroup in articlegrouped:
        n+=1
        if n%100==0: print (n)
        #if n==2: break
        uniqueArticle = list(articlegroup[0])
        groupdata_scores = articlegroup[1][["start_quallevel","start_quallevel_prob","start_qual_aggre","end_quallevel","end_quallevel_prob","end_qual_aggre"]]
        groupdata_scores_lst = list(groupdata_scores.mean())
        uniqueArticle_score_lst = uniqueArticle + groupdata_scores_lst
        article_author_alllist.append(uniqueArticle_score_lst)
    return article_author_alllist
    
    
def writeout(article_author_alllist):
    i = 0
    outString = '"pageid","selected","author","courseID","author_prop","group","control_wikied","indiv_group","classsize","start_quallevel","start_quallevel_prob","start_qual_aggre","end_quallevel","end_quallevel_prob","end_qual_aggre"'
    for lst in article_author_alllist:
        i += 1
        strlst = [str(x) for x in lst]
        outString += '\n'
        outString += ','.join(strlst)
                
    with open(dir_file+"duringSocializationQuality_uniqueArticleUnit2.csv", 'w') as f:
        f.write(outString)
        f.close()    
    