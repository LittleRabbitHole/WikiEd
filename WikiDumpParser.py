#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 09:54:31 2018

this is to parse the wiki dump: enwiki-20170420-pages-logging.xml
write out the all newcomers registered after 2010

@author: angli
"""

from lxml import etree
import pickle
import csv
import os

# this one is good
# incoporated english eversion
# add txt writing feature

def WikiParserNewcomers(filedir, file):
    n = 0
    with open("results.txt", 'w') as x_file:
        for event, elem in etree.iterparse("enwiki-20170420-pages-logging.xml", events=('start', 'end')):
            if event == 'start':
                if elem.tag == "{http://www.mediawiki.org/xml/export-0.10/}logitem":
                    record = {}
                    for child in elem:
                        tag = child.tag.replace("{http://www.mediawiki.org/xml/export-0.10/}","").replace(" ","")
                        if "contributor" not in tag and "params" not in tag:
                            record[tag] = child.text
                        elif "contributor" in tag:
                            for c in child:
                                ctag = "contributor"+c.tag.replace("{http://www.mediawiki.org/xml/export-0.10/}","").replace(" ","")
                                record[ctag] = c.text
                    #finish parsing
                    if record.get('contributorusername') is not None:
                        if "newuser" in str(record.get('action')) or "newuser" in str(record.get('type')):
                            registration = record['timestamp'][:10]
                            if int(registration[:4])>=2010:
                                n+=1
                                username = record['contributorusername']
                                userid = str(record['contributorid'])
                                action = str(record.get('action'))
                                tp = str(record.get('type'))
                                if n%1000000 == 0: print (username, registration)
                                x_file.write("{}, {}, {}, {}, {}\n".format(userid, username, registration, action, tp))
                elem.clear()