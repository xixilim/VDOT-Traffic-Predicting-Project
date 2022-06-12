# -*- coding: utf-8 -*-
"""
Created on Mon May  2 14:32:49 2022

@author: Eileanor LaRocco
"""

import os
import pandas as pd 
from datetime import date
import datetime
import requests

#Change
os.chdir('C:/Users/Eileanor/Desktop/FutureData/VDOTPredictApp') #Directory data is in
days = 20 #how many days ahead to predict (starting today)
apiKey = 'N3MWRWQ2C9R4B3M2FUNB38Q2R' #Weather Data API key from https://www.visualcrossing.com/weather/weather-data-services

#Date Range
start_date = date.today()
end_date = date.today() + datetime.timedelta(days=days)

#Create Date Lookup Table
df = pd.DataFrame()
df['Full_Date'] = pd.date_range(start=start_date,end=end_date).to_pydatetime().tolist()
df['Month'] = pd.DatetimeIndex(df['Full_Date']).month
df['Day'] = pd.DatetimeIndex(df['Full_Date']).day
df['Year'] = pd.DatetimeIndex(df['Full_Date']).year
df['Week Number'] = pd.DatetimeIndex(df['Full_Date']).week
df['Day of Week'] = pd.DatetimeIndex(df['Full_Date']).weekday
df['Day.1'] = pd.DatetimeIndex(df['Full_Date']).day_name()
df['Count'] = df.groupby(['Month','Year','Day.1']).cumcount()+1


df['Full_Date'] = pd.to_datetime(df['Full_Date']).dt.date #change datetime to date

#Holidays
holiday = pd.read_csv("Holidays.csv", encoding_errors='ignore')
#holiday = excel.parse(header=[0]) #include header
holiday['Date'] = pd.to_datetime(holiday['Date']).dt.date #change datetime to date

#Take Holidays within next 14 days
holiday = holiday[(holiday['Date'] >= start_date) & (holiday['Date'] <= end_date)]

#Merge
data = df.merge(holiday, how = 'left', left_on='Full_Date', right_on='Date')
data = data.drop('Date', 1) #delete extra date column
data = data.fillna(value="No Holiday") #fill NA with "No Holiday"

#Weather
r = requests.get(f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Jamestown/{start_date}/{end_date}?unitGroup=us&include=days&key={apiKey}&contentType=json')
rjson = r.json()

#Create dataframe
weather = pd.DataFrame()
for i in range(len(data)): #14 day forecast
    weather.loc[i,'datetime'] = rjson['days'][i]['datetime']
    weather.loc[i,'temp']= rjson['days'][i]['temp']
    weather.loc[i,'precip'] = rjson['days'][i]['precip']
    weather.loc[i,'snow'] = rjson['days'][i]['snow']
    weather.loc[i,'windspeed'] = rjson['days'][i]['windspeed']
    
weather['datetime'] = pd.to_datetime(weather['datetime']).dt.date #change datetime to date

#Merge
data = data.merge(weather, how = 'left', left_on='Full_Date', right_on='datetime')
data = data.drop('datetime', 1) #delete extra date column

#Create Covid column
for i in range(len(data)):
    data.loc[i,'covid'] = 0

#Create Hour Column   
new = pd.date_range(start_date, end_date + datetime.timedelta(days=1), freq='H') #daily to hourly
new = new.to_frame()
new.drop(new.tail(1).index,inplace=True) #drop last row
new = new.reset_index()
new = new.iloc[:,1:]
new['Date'] = pd. to_datetime(new.loc[:,0]).dt.date
new['Time'] = pd. to_datetime(new.loc[:,0]).dt.time
new = new.iloc[:,1:]

#join dfs to create hourly data
new = new.merge(data, how = 'left', left_on='Date', right_on='Full_Date')
new = new.drop('Date', 1) #delete extra date column   

#Transform Time to Hour
for i in range(len(new)):
    new.loc[i,'Time'] = new.loc[i,'Time'].hour

#Rename columns
new.rename(columns={'Time': 'Hour', 'Day.1': 'WeekDay', 'Count' : 'CountWeekDay', 'Full_Date' : 'Date'}, inplace=True)

# Export
new.to_csv ("PredictiveData.csv", index = False, header=True)
