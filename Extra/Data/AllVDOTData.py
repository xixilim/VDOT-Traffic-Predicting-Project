# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:38:01 2022

@author: Eileanor LaRocco
"""
import pandas as pd
import os

path = "C:/Users/Eileanor/Desktop/All"
os.chdir(path)
#Read in each .csv file in specified folder (above)
all_data = pd.DataFrame()

for file in os.listdir():
    name = os.path.basename(file)[:-3]
    if file.endswith(".csv"):
        df = pd.read_csv(f"{path}/{file}")
        all_data = all_data.append(df)
        
all_data = all_data.drop_duplicates(subset=["Date","DAILY"],keep="last")  

# Export
all_data.to_csv ("AllDataNew.csv", index = False, header=True)


