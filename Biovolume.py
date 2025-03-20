# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:05:39 2025

@author: user
"""

#Biovolume calculation from Ecotaxa tsv output "General export separated by NONE"
#For equations see planktoscope manual and ecotaxa->export->summary->formulae

import os
import pandas as pd
import math

#Set working directory
directory = os.chdir('C:/file/path/')
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
        df['Pixelmm']=(data['process_pixel'].astype(float))*0.001  
        df['Majormm']=(data['object_major'].astype(float))*df['Pixelmm']
        df['Minormm']=(data['object_minor'].astype(float))*df['Pixelmm']
        df['Area']=(data['object_area'].astype(float))*df['Pixelmm']*df['Pixelmm']
        df['ImagedV']=data['acq_imaged_volume'].astype(float)
        df['SamplevmL']=(data['sample_total_volume'].astype(float))*1000
        df['ConcV']=data['sample_concentrated_sample_volume'].astype(float)
        
        #Choose biovolume equation
        #Calculate elipsoid volume (Ebv) in mm^3
        df['BV']=((4/3)*math.pi)*((df['Majormm']*(0.5))*(df['Minormm']*(0.5))*(df['Minormm']*(0.5)))
        #Calcaulte the individual volume as shown in Ecotaxa
        #df['BV']=(4/3)*math.pi*(np.sqrt((df['Areamm2'])/math.pi)*df['Sizemm'])**3

        #Calculate mm3/mL in subsample for each taxa
        df['BV sub sample'] = df['BV']/df['ImagedV']
        #Use C1V1=C2V2 to determine the real mm3/mL for each taxa
        df['Biovolume mm3/mL']=(df['BV sub sample']*df['ConcV']/df['SamplevmL'])
        #Convert mm3/mL to mm3/m3 to get a biovolume per m3 for each taxa
        df['Biovolume mm3/m3']=df['Biovolume mm3/mL']*1000000
        
        #Total biovolume per sample
        biovolumes=df[["Sample", "BV sub sample", "Biovolume mm3/mL", "Biovolume mm3/m3"]]
        sampleBV = biovolumes.groupby('Sample').sum()
        
        #Total biovolume per taxa for whole project (all files)
        biovolumet=df[["Taxa", "BV sub sample", "Biovolume mm3/mL", "Biovolume mm3/m3"]]
        taxaBV = biovolumet.groupby('Taxa').sum()
        
        #Total biovolume of each taxa per sample
        biovolumets=df[["Sample", "Taxa", "BV sub sample", "Biovolume mm3/mL", "Biovolume mm3/m3"]]        
        taxasampleBV=biovolumets.groupby(['Sample', 'Taxa']).sum()
        
        #Total biovolume of each taxa by cruise
        biovolumec=df[["Cruise", "Taxa", "BV sub sample", "Biovolume mm3/mL", "Biovolume mm3/m3"]]        
        cruiseBV=biovolumec.groupby(['Cruise', 'Taxa']).sum()

sampleBV.to_csv('C:/file/path/totalsamplebiovolume.csv')
taxaBV.to_csv('C:/file/path/totaltaxabiovolume.csv')
taxasampleBV.to_csv('C:/file/path/taxabysamplebiovolume.csv')
cruiseBV.to_csv('C:/file/path/cruisetaxabiovolume.csv')


#COULD ALSO ADD CALCULATION FOR AVERAGE BIOVOLUME OF TAXA, IF THAT DATA IS INTERESTING
      
        
