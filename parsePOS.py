##############################
# USER INPUTS
##############################

path_pos = r"C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\Program\REAL\contour\raw_File"
path_ASRs = r"C:\Users\CHA82870\Mott MacDonald\AERMOD Modelling Services - Do\06 Working\Program\REAL\ASR_list_contours.xlsx"

##############################
#CODES DO NOT MODIFY
##############################

import pandas as pd
import numpy as np
import glob

def getFiles (path, type):
    filteredFiles = []
    allFiles = glob.glob(path + "/*.{}".format(type))
    
    return allFiles

for path_pos in getFiles(path_pos, 'POS'):
    data = pd.read_csv(path_pos, sep = '\s+', header = None, skiprows=[0,1,2,3,4,5,6,7] )#
    ASRs = pd.read_excel(path_ASRs)
    
    cols = [ "X", "Y", "AVERAGE CONC", "DRY DEPO", "ZELEV", "ZHILL", "ZFLAG", "AVE", "GRP", "DATE"]
    
    data.columns = cols
    
    ASRs['X'] = ASRs['X'].round(2) #data rounding is 2 decimals
    ASRs['Y'] = ASRs['Y'].round(2)
    
    data = pd.merge(data, ASRs, on = ['X', 'Y', 'ZFLAG'])
    
    output = pd.pivot_table(data, values = 'AVERAGE CONC', index = ['DATE'], columns = ["ASRS"], aggfunc = np.sum)
    
    output.columns
    s2 = pd.Series([np.nan]*len(output.columns.tolist()), index= output.columns.tolist())
    s2.name = 0
    output = output.append(s2)
    output = output.sort_index()
    output = output.reset_index()
    
    file_name = path_pos.replace("POS", "xlsx")
    print(file_name)
    output.to_excel(file_name, startrow=2, startcol=2, index = False)