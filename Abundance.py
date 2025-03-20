# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:29:36 2025

@author: User
"""

#Using the output from Ecotaxa Summary->Abundance by NONE, this code will calculate the total counts ('Count') and the cell concentration ('Cells')

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
        
        #Assuming chaing length
        df['Cells']=np.where((df['Taxa']=="Asterionellopsis"), df['Count']*1.3, 
                             np.where((df['Taxa']=="centric diatoms"), df['Count']*1.44,
                                      np.where((df['Taxa']=="Chaetoceros sp."), df['Count']*5.7, 
                                               np.where((df['Taxa']=="chain diatom"), df['Count']*5.94,
                                                        np.where((df['Taxa']=="cylindrical chain forming centric diatoms"), df['Count']*1.62,
                                                                 np.where((df['Taxa']=="Eucampia zodiacus"), df['Count']*3.64,
                                                                          np.where((df['Taxa']=="Pseudo-nitzschia"), df['Count']*1.92,
                                                                                   np.where((df['Taxa']=="Skeletonema"), df['Count']*6.16,
                                                                                            np.where((df['Taxa']=="Thalassionema"), df['Count']*2.75, 
                                                                                                     np.where((df['Taxa']=="Thalassiosira"), df['Count']*2.22,
                                                                                                              np.where((df['Taxa']=="thalassiosira chain"), df['Count']*2.22,
                                                                                                                       np.where((df['Taxa']=="Thalassiosira rotula"), df['Count']*1.14, 
                                                                                                                                df['Count']*1))))))))))))    
        totalsampleabund = df.groupby(['Sample', 'Taxa']).sum()  
        
totalsampleabund.to_csv('C:/file/path.csv')
