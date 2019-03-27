from __future__ import division

##############################
# USER INPUTS

# reference
#https://www.epd.gov.hk/epd/english/environmentinhk/air/guide_ref/guide_aqa_model_g5.html
#https://www.epd.gov.hk/epd/english/environmentinhk/air/guide_ref/guide_aqa_model_g1.html
##############################

path_cmaq = r'C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\PATH\cmaq'
path_aermod = r'C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\Model\AERMOD\Model results\Tier 2 mit\TSPhr'
excel_name = r'P:\Hong Kong\ENL\ENL Personal Folders\Nikita\Hirams HW\ASR results\mFSPan.xlsx'
ASR_list = r'C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\Program\REAL\ASR_list.xlsx'

grids = ['48_38', '49_38', '49_39', '49_40', '50_40', '50_41']

#comment out if not use
pollutants = 1 #TSP
#pollutants = 2 #RSP (PM10) daily
#pollutants = 3 #RSP (PM10) annual
#pollutants = 4 #FSP (PM2.5) daily
#pollutants = 5 #FSP (PM2.5) annual

##############################
#CODES DO NOT MODIFY
##############################

if pollutants == 1: #TSP
    factor_annual = 1
    factor_daily = 1
    factor_aermod = 1
    
    RSP_an_adj = 0
    RSP_10_adj = 0
    
    hourlyExceedance = 500
    dailyExceedance = 100 #not used

elif pollutants == 2: #RSP daily
    factor_annual = 1
    factor_daily = 1 
    factor_aermod = 1
    
    RSP_an_adj = 15.6
    RSP_10_adj = 26.5
    
    hourlyExceedance = 500 #not used
    dailyExceedance = 100

elif pollutants == 3: #RSP annual
    factor_annual = 1
    factor_daily = 1 
    factor_aermod = 1
    
    RSP_an_adj = 15.6
    RSP_10_adj = 26.5
    
    hourlyExceedance = 500 #not used
    dailyExceedance = 100 #not used

elif pollutants == 4: #FSP daily
    factor_annual = 0.71
    factor_daily = 0.75
    factor_aermod = 1
    
    RSP_an_adj = 15.6*factor_annual
    RSP_10_adj = 26.5*factor_daily
    
    hourlyExceedance = 500 #not used
    dailyExceedance = 75

elif pollutants == 5: #FSP annaul
    factor_annual = 0.71
    factor_daily = 0.75
    factor_aermod = 1
    
    RSP_an_adj = 15.6*factor_annual
    RSP_10_adj = 26.5*factor_daily
    
    hourlyExceedance = 500 #not used
    dailyExceedance = 100 #not used

import pandas as pd
from pandas import ExcelWriter
import math
import numpy as np

import glob

def getFiles (path, type):
    filteredFiles = []
    allFiles = glob.glob(path + "/*.{}".format(type))
    
    return allFiles

files_cmaq = getFiles(path_cmaq, 'txt')
files_aermod = getFiles(path_aermod, 'xlsx')

def matrix(cmaq, aermod, factor_daily, factor_annual, factor_aermod):
    data = pd.read_csv(cmaq, sep='\s+')
    data = data.drop([0,1], axis = 0)
    data = data.apply(pd.to_numeric)
    
    index = data.index.tolist()
    re_index = index[-7:] + index[:-7]
    data = data.reindex(re_index) #move the last 8 rows to the top
    
    for i in list(range(7)): #set YYYY to be the year in the 9th row
        data.iloc[i,0] = data.iloc[7,0]
    
    data = data.reset_index(drop=True)
    
    xls = pd.ExcelFile(aermod)
    aermod = xls.parse('Sheet1')
    aermod = aermod.drop(aermod.columns[[0,1]], axis = 1)
    aermod.columns = aermod.loc[0] #set columns equal to row 1
    aermod = aermod.drop([0,1])
    aermod = aermod[:-24] #drop last 24 rows
    aermod = aermod.dropna(axis = 1, how='all') #drop nan columns
    aermod = aermod.reset_index(drop=True)
    lstCols = aermod.columns.tolist()
    lstCols[0]='Time'
    aermod.columns = lstCols
    aermod = aermod.apply(pd.to_numeric)
    
    
    factor_daily = factor_daily #factor for cmeq
    factor_aermod = factor_aermod #factor for aermod

    aermodPath = pd.DataFrame()
    aermodPath['Time'] = aermod[aermod.columns[0]]

    for cols in aermod.columns[1:]: #skip index
        aermodPath[cols] = aermod[cols]*factor_aermod + data['RSP']*factor_daily
    
    #for annual average

    aermod_an = pd.DataFrame()
    aermod_an['Time'] = aermod[aermod.columns[0]]

    for cols in aermod.columns[1:]: #skip index
        aermod_an[cols] = aermod[cols]*factor_aermod + data['RSP']*factor_annual
    
    return data[['Year', 'mm','dd','hh','RSP']], aermod, aermodPath, aermod_an

PATH = pd.DataFrame()
AERMOD =  pd.DataFrame()
AERMODPATH =  pd.DataFrame()
AERMODPATH_24 = pd.DataFrame()
AERMODAN = pd.DataFrame()

df_list = []

for file_aermod in files_aermod: #loop through each aermod files
    for grid in grids: #loop through each grid
        if file_aermod.find(grid) != -1: #check if grid match the name of aermod
            for file_cmaq in files_cmaq: # loop through the cmaq files
                if file_cmaq.find(grid) != -1: #find the one that match with aermod
                    PATH_temp, AERMOD_temp, AERMODPATH_temp, AERMODAN_temp = matrix(file_cmaq, file_aermod, factor_daily, factor_annual, factor_aermod)
                    if len(PATH) == 0:
                        PATH = PATH_temp
                        AERMOD = AERMOD_temp
                        AERMODPATH = AERMODPATH_temp
                        AERMODAN = AERMODAN_temp
                        
                    else:
                        PATH = pd.merge(PATH, PATH_temp, on=['Year', 'mm','dd','hh'])
                        AERMOD = pd.merge(AERMOD, AERMOD_temp, on=['Time'])
                        AERMODPATH = pd.merge(AERMODPATH, AERMODPATH_temp, on=['Time'])
                        AERMODAN = pd.merge(AERMODAN, AERMODAN_temp, on=['Time'])

AERMODPATH_24 = AERMODPATH.groupby(np.arange(len(AERMODPATH))//24).mean()
AERMODPATH_24['Time'] = AERMODPATH.iloc[::24, 0].tolist() #set begining time as col time

AERMOD_24 = AERMOD.groupby(np.arange(len(AERMOD))//24).mean()

cols = AERMOD.columns.tolist()
cols = cols[:1] + sorted(cols[1:])

AERMOD = AERMOD[cols]
AERMOD_24 = AERMOD_24[cols]
AERMODPATH = AERMODPATH[cols]
AERMODPATH_24 = AERMODPATH_24[cols]
AERMODAN = AERMODAN[cols]

AERMODPATH_24.iloc[:,1:] = AERMODPATH_24.iloc[:,1:] + RSP_10_adj

df_list.append(PATH)
df_list.append(AERMOD)
df_list.append(AERMOD_24)
df_list.append(AERMODPATH)
df_list.append(AERMODPATH_24)

def get_nlargest(df, n, adj):
    result = {}
    for cols in df.columns[1:]: #skip index
        tem = df[cols].nlargest(n).tolist()[-1] + adj
        result[cols] = tem
    return result

def nthProjectContribution(df_project, df_total, n, factor_aermod, adj):
    result = {}
    for cols in df_project.columns[1:]: #skip index
        value_total = df_total[cols].nlargest(n).tolist()[-1] + adj
        index = df_total[cols].nlargest(n).index.tolist()[-1]
        value_project = df_project.loc[index, cols]        
        result[cols] = (value_project*factor_aermod)/value_total
    
    return result

def nthbgContribution(df_project, df_total, n, factor_aermod, adj):
    result = {}
    for cols in df_project.columns[1:]: #skip index
        value_total = df_total[cols].nlargest(n).tolist()[-1] + adj
        index = df_total[cols].nlargest(n).index.tolist()[-1]
        value_project = df_project.loc[index, cols]        
        result[cols] = 1- ((value_project*factor_aermod)/value_total)
    
    return result

lst = []
lst.append(get_nlargest(AERMODPATH, 1, 0)) #Max Hourly
lst.append(get_nlargest(AERMODPATH_24, 10,0)) #10th Max Daily
lst.append(get_nlargest(AERMODPATH, 19, 0)) #19th Max Hourly
lst.append((AERMODAN.iloc[:,1:].mean() + RSP_an_adj).to_dict()) #annual average
lst.append(AERMODPATH.iloc[:,1:][AERMODPATH>hourlyExceedance].count().to_dict()) #Exceedance of hourly
lst.append(AERMODPATH_24.iloc[:,1:][AERMODPATH_24>dailyExceedance].count().to_dict()) #Exceedance of daily
lst.append(((AERMOD.iloc[:,1:].mean()/factor_aermod)/((AERMODAN.iloc[:,1:].mean() + RSP_an_adj))).to_dict()) #annual project contribution
lst.append((1-(AERMOD.iloc[:,1:].mean()/factor_aermod)/((AERMODAN.iloc[:,1:].mean() + RSP_an_adj))).to_dict()) #annaul background contribution
lst.append(nthProjectContribution(AERMOD_24, AERMODPATH_24, 10, factor_aermod, 0)) #10th daily max -project contribution (zero becoz added already)
lst.append(nthbgContribution(AERMOD_24, AERMODPATH_24, 10, factor_aermod, 0)) #10th daily max -background contribution
lst.append(nthProjectContribution(AERMOD, AERMODPATH, 1, factor_aermod, 0)) #max hourly -project contribution
lst.append(nthbgContribution(AERMOD, AERMODPATH, 1, factor_aermod, 0)) #Max hourly max -background contribution
lst.append(nthProjectContribution(AERMOD, AERMODPATH, 19, factor_aermod, 0)) #19th hourly -project contribution
lst.append(nthbgContribution(AERMOD, AERMODPATH, 19, factor_aermod, 0)) #19th hourly max -background contribution

summary = pd.DataFrame(lst)
summary['Index'] = ['Max hourly','10th Max Daily','19th Max hourly','Annual average','Exceedance of hourly',
                   'Exceedance of daily','Annual project contribution','Annual background contribution','10th Daily Max - project contribution',
                   '10th Daily Max - background contribution','Max Hourly project contribution','Max Hourly background contribution',
                   '19th Max Hourly project contribution','19th Max Hourly background contribution']
cols = summary.columns.tolist()
cols = cols[-1:]+cols[:-1] #rearrange cols
summary= summary[cols]

if pollutants == 1:
    lst_rows = ['Max hourly', 'Exceedance of hourly', 'Max Hourly project contribution','Max Hourly background contribution']
    summary = summary[summary['Index'].isin(lst_rows)]

elif pollutants == 2:
    lst_rows = ['10th Max Daily', 'Exceedance of daily','10th Daily Max - project contribution','10th Daily Max - background contribution']
    summary = summary[summary['Index'].isin(lst_rows)]

elif pollutants == 3:
    lst_rows = ['Annual average', 'Annual project contribution','Annual background contribution']
    summary = summary[summary['Index'].isin(lst_rows)]
    
elif pollutants == 4:
    lst_rows = ['10th Max Daily', 'Exceedance of daily','10th Daily Max - project contribution','10th Daily Max - background contribution']
    summary = summary[summary['Index'].isin(lst_rows)]

elif pollutants == 5:
    lst_rows = ['Annual average', 'Annual project contribution','Annual background contribution']
    summary = summary[summary['Index'].isin(lst_rows)]

lst = pd.read_excel(ASR_list)
lst = lst['ASRS'][lst['ASRS'].isin(summary.columns.tolist())].tolist() #filter ASRs that is in the sumamry table columns
lst.insert(0, "Index")
summary = summary[lst]
df_list.append(summary)

summary_T = summary.T
summary_T.columns = summary_T.iloc[0]
summary_T = summary_T.drop('Index', axis = 0)
summary_T = summary_T.reset_index()

df_list.append(summary_T)

sheet_name = ['PATH','AERMOD','AERMOD_24','AERMODPATH', 'AERMODPATH_24', 'Summary', 'Summary Trasposed']

def save_xls(list_dfs, xls_path, sheet_name):
    writer = ExcelWriter(xls_path)
    for n, df in zip(sheet_name, list_dfs):
        df.to_excel(writer,'%s' % n, index = False)
    writer.save()

save_xls(df_list, excel_name, sheet_name)