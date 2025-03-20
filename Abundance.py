# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:29:36 2025

@author: User
"""

#Cell abundance from Ecotaxa output Summary->Abundance by NONE

import os
import pandas as pd
import numpy as np

#Set working directory
directory = os.chdir('C:/file/path/')
#Name extension
ext = ('.tsv')

#Print the file names for the files being processed
for files in os.listdir(directory):
    if files.endswith(ext): print(files)
    
#Create dataframe
df = pd.DataFrame(columns = ['Sample', 'Status', 'Taxa', 'Count'])

#Read file with ext ending into python
for files in os.listdir(directory):
    if files.endswith(ext):
        data=pd.read_csv(files, sep='\t') 

        #Input data to dataframe
        df['Sample']=data['sampleid']
        df['Status']=data['status']    
        df['Taxa']=data['taxonid']
        df['Count']=data['count'].astype(float)
        
        #Assuming chaing length of 6 (Chaetoceros sp.), 8 (Rhizosolenia), 2 (Thalassiosira)
        df['Cells']=np.where((df['Taxa']=="Chaetoceros sp."), df['Count']*6,
                                                 np.where((df['Taxa']=="Rhizosolenia"), df['Count']*8, 
                                                          np.where((df['Taxa']=="Thalassiosira"), df['Count']*2, 
                                                                   df['Count']*1)))        
        totalsampleabund = df.groupby(['Sample', 'Taxa']).sum()
        
totalsampleabund.to_csv('C:/file/path.csv')
