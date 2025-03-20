# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 10:06:20 2025

@author: User
"""

#Concentration calculation from Ecotaxa tsv output "General export separated by NONE"

import os
import pandas as pd
import numpy as np

#Set working directory
directory = os.chdir('C:/file/path/Concentration/')
#Name extension
ext = ('.tsv')

#Print the file names for the files being processed
for files in os.listdir(directory):
    if files.endswith(ext): print(files)
    
#Create dataframe
df = pd.DataFrame()

#Read in tsv file, could be more than one too but then need to add append function!!!
for files in os.listdir(directory):
    if files.endswith(ext):
        data=pd.read_csv(files, sep='\t') 
        
        #Input data to dataframe as a number (float) and convert to correct units
        df['Sample']=data['sample_id']
        df['Cruise']=data['sample_project']
        df['Taxa']=data['object_annotation_category']
        #Count number of each taxa in each sample
        df['Total abundance'] = df.groupby(['Sample','Taxa'])['Taxa'].transform('count')
        #Input volume data
        df['ImagedV']=data['acq_imaged_volume'].astype(float)
        df['SamplevmL']=(data['sample_total_volume'].astype(float))*1000
        df['ConcV']=data['sample_concentrated_sample_volume'].astype(float)
        #Drop all the rows with duplicate data, including counts of 0
        df=df.drop_duplicates()
        
        #Assuming chaing length of 6 (Chaetoceros sp.), 8 (Rhizosolenia), 2 (Thalassiosira)
        df['Cells']=np.where((df['Taxa']=="Asterionellopsis"), df['Total abundance']*1.3, 
                             np.where((df['Taxa']=="centric diatoms"), df['Total abundance']*1.44,
                                      np.where((df['Taxa']=="Chaetoceros sp."), df['Total abundance']*5.7, 
                                               np.where((df['Taxa']=="chain diatom"), df['Total abundance']*5.94,
                                                        np.where((df['Taxa']=="cylindrical chain forming centric diatoms"), df['Total abundance']*1.62,
                                                                 np.where((df['Taxa']=="Eucampia zodiacus"), df['Total abundance']*3.64,
                                                                          np.where((df['Taxa']=="Pseudo-nitzschia"), df['Total abundance']*1.92,
                                                                                   np.where((df['Taxa']=="Skeletonema"), df['Total abundance']*6.16,
                                                                                            np.where((df['Taxa']=="Thalassionema"), df['Total abundance']*2.75, 
                                                                                                     np.where((df['Taxa']=="Thalassiosira"), df['Total abundance']*2.22,
                                                                                                              np.where((df['Taxa']=="thalassiosira chain"), df['Total abundance']*2.22,
                                                                                                                       np.where((df['Taxa']=="Thalassiosira rotula"), df['Total abundance']*1.14, 
                                                                                                                                df['Total abundance']*1))))))))))))
        #Convert the total cell abundance to concentration
        df['Concentrated (cells/mL)']=((df['Cells'])/df['ImagedV'])*(df['ConcV'])
        df['Total concentration (cells/mL)']=df['Concentrated (cells/mL)']/df['SamplevmL']
        df['Total concentration (cells/m3']=df['Total concentration (cells/mL)']*1000000
        

df.to_csv('C:/file/path/Concentration per sample in cells.csv')
