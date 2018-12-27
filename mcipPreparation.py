##############################
# USER INPUTS
##############################
path = r'C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\PATH\mcip'

##############################
#CODES DO NOT MODIFY
##############################
import pandas as pd
import math
import glob

def getFiles (path):
    filteredFiles = []
    allFiles = glob.glob(path + "/*.txt")
    
    return allFiles

def get_tenth_deci(n):
    frac = math.modf(n)
    frac_str = str(frac[0])
    return int(frac_str[2])

def ceilingHeight(n):
    return ((n/1000)*100)

allFiles = getFiles(path)

for files in allFiles:
    print('working on {}'.format(files))
    data = pd.read_csv(files, sep='\s+')
    data = data.drop(0, axis = 0)
    data = data.apply(pd.to_numeric)
    
    data['cfrac'] = data['cfrac'].apply(get_tenth_deci) #convert cloud cover to be tenth
    data['pbl'][data['pbl'] > 3000] = 3000 #cap mixing height
    data['pbl'][data['pbl']<121.3] = 121.3 #cap mixing height
    data['wspd'][data['wspd']<1] = 1  #cap wind speed
    data['cldb'] = data['cldb'].apply(ceilingHeight)
    
    index = data.index.tolist()
    re_index = index[-7:] + index[:-7]
    data = data.reindex(re_index) #move the last 7 rows to the top
    
    for i in list(range(7)): #set YYYY to be the year in the 9th row
        data.iloc[i,0] = data.iloc[7,0]
    
    cols = data.columns.tolist()
    cols = cols[4:]
    data[cols] = data[cols].apply(lambda x: pd.Series.round(x, 3))
    
    fileName = files.replace('txt','csv')
    data.to_csv(fileName, index = False)