# -*- coding: utf-8 -*-
"""
Created on Mon May  2 14:32:49 2022

@author: Eileanor LaRocco
"""

import pandas as pd
import os
import numpy as np

path = "C:/Users/Eileanor/Desktop/Data"
os.chdir(path)

#Date Lookup Table
datesTable = pd.read_csv("C:/Users/Eileanor/Desktop/Data/DatesTable.csv")
datesTable = datesTable.iloc[:,1:] #Remove index column
datesTable['Full_Date'] = pd.to_datetime(datesTable['Full_Date']).dt.date #change datetime to date

#Holidays
excel = pd.ExcelFile("C:/Users/Eileanor/Desktop/Data/hoilday.xlsx")
holiday = excel.parse(header=[0]) #include header
holiday = holiday.iloc[:, np.r_[1,3]]
holiday['Holiday'] = pd.to_datetime(holiday['Holiday']).dt.date #change datetime to date

#Merge
data = datesTable.merge(holiday, how = 'left', left_on='Full_Date', right_on='Holiday')
data = data.drop('Holiday', 1) #delete extra date column

#Weather
weather1 = pd.read_csv("C:/Users/Eileanor/Desktop/Data/Jamestown_2012-01-01_to_2014-09-26.csv")
weather2 = pd.read_csv("C:/Users/Eileanor/Desktop/Data/jamestown, VA 2014-09-27 to 2017-06-21.csv")
weather3 = pd.read_csv("C:/Users/Eileanor/Desktop/Data/Jamestown 2017-06-22 to 2020-02-29.csv")
weather4 = pd.read_csv("C:/Users/Eileanor/Desktop/Data/jamestown, VA 2020-03-01 to 2022-04-28.csv")

weather = pd.concat([weather1,weather2,weather3,weather4])
weather['datetime'] = pd.to_datetime(weather['datetime']).dt.date #change datetime to date
weather = weather[['datetime', 'temp','precip','snow','windspeed']] #extract only features we want

#Merge
data = data.merge(weather, how = 'left', left_on='Full_Date', right_on='datetime')
data = data.drop('datetime', 1) #delete extra date column

#School Breaks/Graduation
excel = pd.ExcelFile("C:/Users/Eileanor/Desktop/Data/School.xlsx")
school = excel.parse(header=[0]) #include header
school= school.drop('Year', 1) #delete extra year column

school["id"] = school.index + 1
melt = school.melt(id_vars=['id','Holiday Observed'], value_name='date').drop('variable', axis=1)
melt['date'] = pd.to_datetime(melt['date'])

melt = melt.groupby('id').apply(lambda x: x.set_index('date').resample('d').first())\
           .ffill()\
           .reset_index(level=1)\
           .reset_index(drop=True)
melt = melt.drop('id', 1) #delete id column
melt['date'] = pd.to_datetime(melt['date']).dt.date #change datetime to date

#Merge
data = data.merge(melt, how = 'left', left_on='Full_Date', right_on='date')
data = data.drop('date', 1) #delete extra date column

#Truncate for what dates we have (02/01/2014-03/31/22)
data['Full_Date'] = pd.to_datetime(data['Full_Date']) #change datetime to date
data = data[(data['Full_Date'] > '2014-01-31') & (data['Full_Date'] < '2022-04-01')]

# Export
data.to_csv ("ExtraData.csv", index = False, header=True)
