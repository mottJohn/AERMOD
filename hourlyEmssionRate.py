##############################
# USER INPUTS
##############################
workingHour = list(range(7,19))#very tricky no. (endhr: 8 - 19) 
path = r'C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\Program\HOUREMI'

#comment out if not use
#pollutants = 1 #TSP
#pollutants = 2 #RSP (PM10) daily
pollutants = 3 #RSP (PM10) annual
#pollutants = 4 #FSP (PM2.5) daily
#pollutants = 5 #FSP (PM2.5) annual


##############################
#CODES DO NOT MODIFY

#MODIFY IF NEEDED
#The hourly emission rate file is project specific. You may need to understand the codes and modify according.
##############################

import pandas as pd
import csv
import numpy as np

if pollutants == 1: #TSP
    EF_HC_workingHour = 1.72276e-05
    EF_HC_nonWorkingHour = 0

    EF_WE_workingHour = 2.23713e-07
    EF_WE_nonWorkingHour = 2.69533e-06

    factor = 1

    fileName = 'mTSP_hr_houremi_1.txt'

elif pollutants == 2: #RSP daily
    EF_HC_workingHour = 5.16829e-06
    EF_HC_nonWorkingHour = 0

    EF_WE_workingHour = 6.71138e-08
    EF_WE_nonWorkingHour = 8.086e-07

    factor = 1

    fileName = 'mRSP_dn_houremi_1.txt'

elif pollutants == 3: #RSP annual
    EF_HC_workingHour = 1.13039e-06
    EF_HC_nonWorkingHour = 0

    EF_WE_workingHour = 1.46789e-08
    EF_WE_nonWorkingHour = 1.77892e-07

    factor = 1

    fileName = 'mRSP_an_houremi_1.txt'

elif pollutants == 4: #FSP daily
    EF_HC_workingHour = 5.16829e-07
    EF_HC_nonWorkingHour = 0

    EF_WE_workingHour = 6.71138e-09
    EF_WE_nonWorkingHour = 8.086e-08

    factor = 1

    fileName = 'mFSP_dn_houremi_1.txt'

elif pollutants == 5: #FSP annaul
    EF_HC_workingHour = 1.13039e-07
    EF_HC_nonWorkingHour = 0

    EF_WE_workingHour = 1.46789e-09
    EF_WE_nonWorkingHour = 1.77892e-08

    factor = 1

    fileName = 'mFSP_an_houremi_1.txt'

date_index = pd.date_range(start=pd.datetime(2010,1,1), end=pd.datetime(2011,1,1,23), freq='H') #hr0 to hr23 will add one later

hourlyEF_HC = pd.DataFrame(index = date_index)
hourlyEF_WE = pd.DataFrame(index = date_index)

for index, row in hourlyEF_HC.iterrows(): #loop throught the pd and assign EF
    if index.hour in(workingHour):
        hourlyEF_HC.loc[index,'EF'] = EF_HC_workingHour
    else:
        hourlyEF_HC.loc[index, 'EF'] = EF_HC_nonWorkingHour

for index, row in hourlyEF_WE.iterrows(): #loop throught the pd and assign EF
    if index.hour in(workingHour):
        hourlyEF_WE.loc[index,'EF'] = EF_WE_workingHour
    else:
        hourlyEF_WE.loc[index, 'EF'] = EF_WE_nonWorkingHour

#generate emission factor

HV_source = []

for i in range(1,169):
    name = '{}_HC          '.format(i)
    HV_source.append(name)

WE_source = []

for i in range(1,169):
    name = '{}_WE          '.format(i)
    WE_source.append(name)

master = pd.DataFrame()

for name in HV_source:
    hourlyEF_HC['Source'] = name #assign name to the whole dataframe

    master = pd.concat([master, hourlyEF_HC]) #master = #sources * df
        
for name in WE_source:
    hourlyEF_WE['Source'] = name #assign name to the whole dataframe
    
    master = pd.concat([master, hourlyEF_WE]) #master = #sources * df

master['Year'] = master.index.year
master['Month'] = master.index.month
master['Day'] = master.index.day
master['Hour'] = master.index.hour

master['SO'] = 'SO'
master['HOUREMIS'] = 'HOUREMIS'

cols = master.columns.tolist()
cols = cols[-2:] +  cols[2:-2] + cols[1:2] + cols[0:1]

master = master[cols]
master['EF'] = master['EF']*factor
master['Hour'] = master['Hour'] + 1 #add one hour to change hr0 - hr 23 to hr1 - hr24
master['Sort'] = master['Source'].str.extract('(\d+)', expand = False).astype(int)
master.sort_values(['Year','Month','Day','Hour', 'Sort'], inplace=True)
master.drop('Sort', axis = 1, inplace = True)
master['EF']= master['EF'].apply(lambda x: '%.13f' % x).values.tolist() #for decimal place

fmt = '%0s %+1s %+1s %+2s %+2s %+2s %-1s %+13s'
np.savetxt(path +'\\' + fileName, master.values, fmt=fmt)