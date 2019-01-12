#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 12:34:18 2019

@author: angli
"""

import pickle
import csv

if __name__ == "__main__":
    dir_file = "/Users/angli/ANG/OneDrive/Documents/Pitt_PhD/ResearchProjects/Wiki_Edu_Project/Data/finalRevise/"
    file = "final_control_endSemester.pk"
    f = open(dir_file+file, 'rb')   # 'r' for reading; can be omitted
    students_controls = pickle.load(f)          # load file content as mydict
    f.close() 
