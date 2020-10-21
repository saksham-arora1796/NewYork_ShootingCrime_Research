import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import time
import docx
from docx import Document
import os
import subprocess
import collections
import glob
#import sys
import string
import enchant
from pprint import pprint

#########Reading the dataset and filling NA in place of any sort of missing data##########################
d = pd.read_csv('/Users/piyu/Documents/DAEN 698/NYPD_Shooting_Incident_Data__Historic_.csv', delimiter = ',')
d.fillna("NA", inplace=True)

#########Creating lists of all the columns present in the dataset##############################
ds_key = d['INCIDENT_KEY'].tolist()
ds_date = d['OCCUR_DATE'].tolist()
ds_time = d['OCCUR_TIME'].tolist()
ds_boro = d['BORO'].tolist()
ds_precinct = d['PRECINCT'].tolist()
ds_jcode = d['JURISDICTION_CODE'].tolist()
ds_location = d['LOCATION_DESC'].tolist()
ds_location = [dt.replace('MULTI DWELL - PUBLIC HOUS', 'MULTI DWELL - PUBLIC HOUSE') for dt in ds_location]     #####replacing MULTI DWELL - PUBLIC HOUS to MULTI DWELL - PUBLIC HOUSE
ds_mflag = d['STATISTICAL_MURDER_FLAG'].tolist()
ds_pagegrp = d['PERP_AGE_GROUP'].tolist()
ds_psex = d['PERP_SEX'].tolist()
ds_prace = d['PERP_RACE'].tolist()
ds_pagegrp = d['VIC_AGE_GROUP'].tolist()
ds_vsex = d['VIC_SEX'].tolist()
ds_vrace = d['VIC_RACE'].tolist()
ds_xcord = d['X_COORD_CD'].tolist()
ds_ycord = d['Y_COORD_CD'].tolist()
ds_latitude = d['Latitude'].tolist()
ds_longitude = d['Longitude'].tolist()
print("                  Count of null values after handling missing data                        ")
print()
print(d.isnull().sum())
print()
print("#############################################################################")
print()

#####Most unsafe borough###############
counter = collections.Counter(ds_boro)                                      
boro = list(counter.keys())
no_of_incidents = list(counter.values())
print("                    Total Number of cases in each Borough                   ")                
print()
for i in range(0,len(boro)):
    print(boro[i], " - ",no_of_incidents[i])
    
maximum_incidents = max(no_of_incidents)
index = no_of_incidents.index(maximum_incidents)
print()
print("The maximum number of incidents have occured in",boro[index])
print("Therefore,",boro[index],"is the most unsafe borough of New York.")
print()
print("#############################################################################")

######Perp majority Sex####################
malecounter = 0
femalecounter = 0
for i in ds_psex:
    if i == 'M':
        malecounter = malecounter + 1
    if i == 'F':
        femalecounter = femalecounter + 1

print()
print("                           Sex wise count of Perps                           ")
print()
print("The number of female perps is",femalecounter)
print("The number of male perps is",malecounter)
print()
if malecounter>femalecounter:
    print("Males commit this sort of crime more frequently as compared to females.")

if femalecounter>malecounter:
    print("Females commit this sort of crime more frequently as compared to males.")
print()
print("#############################################################################")

######Perp Race####################

race = []
no_of_incidents = []
p_race_list = []
for i in ds_prace:
    if i != 'NA' and i != 'UNKNOWN':
        p_race_list.append(i)
        
counter_of_race = collections.Counter(p_race_list)                                  
race = list(counter_of_race.keys())
no_of_incidents = list(counter_of_race.values())
print()
print("                           Race wise count of Perps                           ")
print()
for i in range(0,len(race)):
    print(race[i], " - ",no_of_incidents[i])
    
maximum_incidents = max(no_of_incidents)
index = no_of_incidents.index(maximum_incidents)
print()
print("The maximum number of incidents have been caused by the",race[index],"race.")
print()
print("#############################################################################")
print()

######Victim Sex####################
malecounter = 0
femalecounter = 0
for i in ds_vsex:
    if i == 'M':
        malecounter = malecounter + 1
    if i == 'F':
        femalecounter = femalecounter + 1
print("                           Sex wise count of Victims                           ")
print()
print("The count of female victims is",femalecounter)
print("The count of male victims is",malecounter)
print()
if malecounter>femalecounter:
    print("Males fall prey to this sort of crime more frequently as compared to females.")

if femalecounter>malecounter:
    print("Females fall prey to this sort of crime more frequently as compared to males.")
print()
print("#############################################################################")
print()
######Murder Flag####################

counter = collections.Counter(ds_mflag)
flag = list(counter.keys())
no_of_incidents = list(counter.values())
print("                                 Murder Flag                                 ")
print()
for i in range(0,len(flag)):
    print(flag[i], " - ",no_of_incidents[i])
    if flag[i] == True:
        d_index = i
    elif flag[i] == False:
        s_index = i
print()
print("A total of",no_of_incidents[d_index],"incidents finally led to the death of the victims.")
print("The victims survived in a total number of",no_of_incidents[s_index],"such incidents.")
print()
print("#############################################################################")
print()
######Location Category####################
location = []
no_of_incidents = []
counter = collections.Counter(ds_location)
loc = list(counter.keys())
noi = list(counter.values())
for i in range(0,len(loc)):
    if loc[i] is not "NA":
        location.append(loc[i])
        no_of_incidents.append(noi[i])
print("        Count of the number of cases in each Category of Locations             ")
print()
for i in range(0,len(location)):
    print(location[i], " : ",no_of_incidents[i])
    
maximum_incidents = max(no_of_incidents)
index = no_of_incidents.index(maximum_incidents)
print()
print("The maximum number of incidents have occured in",location[index])
print("Therefore,",location[index],"is the most unsafe type of location of New York.")
print()
print("#############################################################################")
print()

##############Prime hours of occurence of crime###############

keys = ["12 AM to 4 AM","4 AM to 8 AM","8 AM to 12 PM","12 PM to 4 PM","4 PM to 8 PM","8 PM to 12 AM"]
li = [0,0,0,0,0,0]
for t in ds_time:
    time = int(t[:2].replace(":",""))
    if time < 4:
        li[0] = li[0] + 1
    elif time >= 4 and time < 8:
        li[1] = li[1] + 1
    elif time >= 8 and time < 12:
        li[2] = li[2] + 1
    elif time >= 12 and time < 16:
        li[3] = li[3] + 1
    elif time >= 16 and time < 20:
        li[4] = li[4] + 1
    elif time >= 20 and time <= 23:
        li[5] = li[5] + 1
dic = dict(zip(keys, li))
print("                     Prime hours of occurence of crime             ")
print()
print("The number of incidents occuring in the mentioned time slots")
pprint(dic)
prime_hours = max(dic, key=dic.get)
print()
print("The prime hours of occurence of such crimes are between",prime_hours,".")


#####################################################################
