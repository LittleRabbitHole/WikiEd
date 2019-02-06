#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 14:49:00 2018
for utilities

@author: Ang
"""

import pandas as pd
import os
import datetime
import numpy as np
import urllib.parse
import json
import csv
import os
import requests
import sys

def returnJsonCheck(response) -> dict:
    try:
        return response.json()
    except:
        print("ERROR")
        print(response)
        print(response.text)
        sys.exit("json error")


#api calls for revision
#https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvdir=newer&rvprop=ids|timestamp|user|userid|commen|size&pageids=31445634&rvlimit=500
#https://zh.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvdir=newer&rvprop=ids%7Ctimestamp%7Cuser%7Cuserid%7Ccomment%7Csize&pageids=1623767&rvlimit=500
#https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Executive_Order_13769&rvprop=timestamp|user|comment&generator=revisions
#url = "https://en.wikipedia.org/w/api.php?action=query&format=json&rvdir=newer&rvlimit=500&prop=revisions&rvprop=ids|timestamp|user|userid|comment&titles=" + pageTitle
#url = API + pageid
def GetPageRevision(url):
    #input the API url for revisions of one article
    revisions = []                                        #list of all accumulated revisions
    next = ''                                             #information for the next request
    while True:
        #response = urllib2.urlopen(url + next).read()     #web request
        response=requests.get(url + next)
        responsedata = returnJsonCheck(response)        
        page_id = list(responsedata["query"]["pages"].keys())[0]
        revision_data_lst=responsedata['query']['pages'][page_id].get('revisions')
        if revision_data_lst is not None:
            revisions += revision_data_lst  #adds all revisions from the current request to the list
    
            try:        
                cont = responsedata['continue']['rvcontinue']
            except KeyError:                                      #break the loop if 'continue' element missing
                break
    
            next = "&rvcontinue=" + cont             #gets the revision Id from which to start the next request
        else:
            break
    return page_id, revisions




def AllArticlesRevisions(all_articles):
    #input all article df, output all revisions as json
    output_json = {}
    i=0
    for idx, item in all_articles.iterrows():
        i+=1
        print (i)
        lang = item.loc["Lang"]
        pageid = str(item.loc["Ori_PageID"])
        wiki_link = "https://{}.wikipedia.org/".format(lang)
        API = wiki_link + "w/api.php?action=query&format=json&prop=revisions&rvdir=newer&rvprop=ids|timestamp|user|userid|comment|size&pageids={}&rvlimit=500".format(pageid)
        results = GetPageRevision(API)
        output_json[pageid, lang] = results
    return output_json



def getUserContributions(url):
    #input the API url for contributions of one user
    revisions = []                                        #list of all accumulated revisions
    next = ''                                             #information for the next request
    while True:
        #response = urllib2.urlopen(url + next).read()     #web request
        response=requests.get(url + next)
        responsedata = returnJsonCheck(response)        
        revision_data_lst=responsedata["query"]["usercontribs"]
        revisions += revision_data_lst  #adds all revisions from the current request to the list

        try:        
            cont = responsedata['continue']['uccontinue']
        except KeyError:                                      #break the loop if 'continue' element missing
            break

        next = "&uccontinue=" + cont             #gets the revision Id from which to start the next request

    return revisions





#page contributors
def GetPageContributors(lang, pageid):
    #this is to retrieve all contributors given a page id
    wiki_link = "https://{}.wikipedia.org/".format(lang)
    API = wiki_link + "/w/api.php?action=query&format=json&prop=contributors&pageids={}&pcexcludegroup=bot&pclimit=500".format(str(pageid))
    PageContributors = []
    next = ''                                             #information for the next request
    while True:
        response=requests.get(API + next)
        responsedata = returnJsonCheck(response)        
        page_id = list(responsedata["query"]["pages"].keys())[0]
        contributor_lst=responsedata['query']['pages'][page_id].get('contributors')
        if contributor_lst is not None:
            PageContributors += contributor_lst  #adds all contributors from the current request to the list
        #retrieve continue
        try:        
            cont = responsedata['continue']['pccontinue']
        except KeyError:                                      #break the loop if 'continue' element missing
            break
        next = "&pccontinue=" + cont             #gets the revision Id from which to start the next request
    return PageContributors
    


def GetAllContributors(all_article_pages):
    #collect all the contributors for articles from article lists
    i = 0
    all_contributors = []
    for item in all_article_pages:#'PageType||Ori_PageID||Lang||Red_PgId||title'
        i += 1
        if i%1000 == 0: print(i)
        lang = item[2]
        pageid = item[3]
        PageType = item[0]
        Ori_PageID = item[1]
        #get all contributors
        Contributors_lst = GetPageContributors(lang, pageid) #as [{},{}]
        #process the contributors_lst into lists
        if Contributors_lst != []:
            Contributors = []
            for contributor in Contributors_lst:
                Contributors.append([Ori_PageID, PageType, pageid, lang, str(contributor['userid']), contributor['name']])
            #add into all_contributors
            all_contributors += Contributors
    return all_contributors


def GetRedirectPages(postid, lang, article):
    #collect all the redirects for a single article
    #redirectAPI = wiki_link + "w/api.php?action=query&pageids=31593941&redirects&prop=redirects&rdlimit=max"
    allpages = [] # [pgid, redir['pageid'], redir['title']]
    wiki_link = "https://{}.wikipedia.org/".format(lang)
    redirectAPI = wiki_link + "w/api.php?action=query&format=json&titles={}&redirects&prop=redirects&rdlimit=max".format(article)
    response=requests.get(redirectAPI)
    r_json = returnJsonCheck(response)
    pgid = list(r_json['query']['pages'].keys())[0]
    red_pg_lst = r_json['query']['pages'][pgid].get('redirects')
    #append original page
    allpages.append(["orig", pgid, lang, pgid, article, postid])
    #if has the redirect
    if red_pg_lst is not None:
        for item in red_pg_lst:
            id_title = ["redirct", pgid, lang, item['pageid'], item['title'], postid]
            allpages.append(id_title)
    #if without redirect
    else: allpages.append(["orig", pgid, lang, pgid, r_json['query']['pages'][pgid]['title'], postid])
    return allpages
    


def GetAllPageswithDirect(article_df):
    #input all article as df, output list of all redirect articles
    directpages_alllist = []
    counter = 0
    for index, row in article_df.iterrows():
        counter += 1
        if counter%100 == 0: print (counter)
        postid = row.loc['post_id']
        lang = row.loc['wiki_lang']
        article = row.loc['article']  
        alldirectpages = GetRedirectPages(postid, lang, article)
        directpages_alllist += alldirectpages
    #return
    return directpages_alllist
    

def WriteOut_Lst2Str1(lst, filename):
    i = 0
    outString = 'PageType||Ori_PageID||Lang||Red_PgId||title||Postid'
    #outString = 'Ori_PageID||PageType||pageid||lang||userid||name'
    for item in lst:
        i += 1
        item[3] = str(item[3])
        item[-1] = str(item[-1])
        outString += '\n'
        outString += '||'.join(item)
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filename, 'w') as f:
        f.write(outString)
        f.close()

def WriteOut_Lst2Str2(lst, filename):
    i = 0
    outString = 'PageType,Ori_PageID,Lang,Red_PgId,Postid'
    #outString = 'Ori_PageID, PageType, pageid, lang, userid'
    for item in lst:
        i += 1
        outString += '\n'
        outString += ','.join([item[0],item[1],item[2], str(item[3]), str(item[-1])])
        
#    result_path = '{}/results'.format(file_loc)
#    if not os.path.exists(result_path):
#        os.makedirs(result_path)
        
    with open(filename, 'w') as f:
        f.write(outString)
        f.close()

    
def NearestDate(all_datesobj_list, pivot_datetime):
    #this is to find the nearest pivot_datetime from all_datesobj_list
    #all inputs should be in datetime format
    return min(all_datesobj_list, key=lambda x: abs(x - pivot_datetime))
    




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    