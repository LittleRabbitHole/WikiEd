#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 11:54:16 2019
this is to do the author map

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
from functools import reduce



def returnIDX(course_lst, course_intersect):
    IDX = []
    for i in range(len(course_lst)):
        item = course_lst[i]
        if any(elem in item for elem in course_intersect):
            #print (item)
            IDX.append(i)
    return IDX    

def reviseAuthor(row):
    mainauthor = row['author']
    courseID = row['courseID']
    group = row['control_wikied']
    if group == -2:
        finalauthors = mainauthor
    else:
        author_lst = row['authors'].split("||")
        course_lst = [course_dict[x] for x in author_lst]
        course_intersect = list(reduce(set.intersection, [set(item) for item in course_lst ]))
        if len(course_intersect) == 0:
            finalauthors = mainauthor
        elif str(courseID) in course_intersect:
            indx = returnIDX(course_lst, course_intersect)
            finalauthors = '||'.join([author_lst[i] for i in indx])
        else:
            finalauthors = mainauthor
    return finalauthors

if __name__ == "__main__":
    dir_file = "/Users/jiajunluo/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/final/"
    coureseInfofile = "datafanalysis/fullstudentset_updatedgroup.csv"
    article_author = "datafanalysis/duringSocializationQuality_uniqueArticleUnit_authormap.csv"
    
    f = open(dir_file+coureseInfofile, 'r')
    courseinfo = f.readlines()
    f.close()

    
    course_dict = {}
    for line in courseinfo[1::]:
        lst = line.split(",")
        courseID = lst[0]
        wikied = lst[-10]
        if wikied in course_dict.keys():
            course_dict[wikied].append(courseID)
        else:
            course_dict[wikied] = [courseID]
    course_dict.pop('#N/A', None)
    course_dict.pop('0', None)
    
    authormap_df = pd.read_csv(dir_file+article_author)
    authormap_df["updated_classauthor"] = authormap_df.apply(reviseAuthor, axis=1)
    authormap_df.to_csv(dir_file+"duringSocializationQuality_uniqueArticleUnit_authormap_updated.csv", index=False)
    
    row = authormap_df.iloc[2]
    reviseAuthor(row)
    
    
    
    
