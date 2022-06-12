# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:33:20 2022

@author: Eileanor LaRocco
"""
import pandas as pd

#Extra Data
extra = pd.read_csv("C:/Users/Eileanor/Desktop/Data/ExtraData.csv")

#VDOT Data
vdot = pd.read_csv("C:/Users/Eileanor/Desktop/Data/AllData.csv")

#Datetime
vdot['Date'] = pd.to_datetime(vdot['Date']).dt.date #change datetime to date
extra['Full_Date'] = pd.to_datetime(extra['Full_Date']).dt.date #change datetime to date

#Merge
data = vdot.merge(extra, how = 'left', left_on='Date', right_on='Full_Date')
data = data.drop('Full_Date', 1) #delete extra year column

#we're missing some days in 2015

# Export
data.to_csv ("MergedData.csv", index = False, header=True)
