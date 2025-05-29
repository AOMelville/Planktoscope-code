# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:29:36 2025

@author: User
"""

#Using the output from Ecotaxa Export->General Export, this code will calculate the total counts ('Count') and the cell concentration ('Cells')

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

        #Split the sample ID into cruise and sample name, adding meta data to new datframe df
        dfp[['Cruise', 'Info']] = df['sample_id'].str.split('_', n=1, expand=True)
        dfp[['Station', 'Event', 'Sample', 'Bottle']]=dfp['Info'].str.split('-', n=3, expand=True)
        
        #Building dataframe metadata
        dfp['Latitude']=df['object_lat'] 
        dfp['Longitude']=df['object_lon'] 
        dfp[['Year', 'Month', 'Day']]=df['object_date'].str.split('-', n=2, expand=True)
        
        #Adding taxonomic information
        dfp['Taxa']=df['object_annotation_category']

        #Input volume data
        dfp['ImagedV']=df['acq_imaged_volume'].astype(float)
        dfp['SamplevmL']=(df['sample_total_volume'].astype(float))*1000 #Conver the L to mL
        dfp['ConcV']=df['sample_concentrated_sample_volume'].astype(float)
        
        #Count number of each taxa in each sample
        dfp['Total abundance'] = dfp.groupby(['Cruise', 'Station','Sample','Taxa'])['Taxa'].transform('count')
        #Drop all the rows with duplicate data, including counts of 0
        dfp=dfp.drop_duplicates()
        
        #Calculating total cells by assuming chain length
        #Change the species id depending on the project
        #Change the chain length depending on the species
        dfp['Cells']=np.where((dfp['Taxa']=="Asterionellopsis"), dfp['Total abundance']*1.2, 
                             np.where((dfp['Taxa']=="centric diatoms"), dfp['Total abundance']*1.27,
                                      np.where((dfp['Taxa']=="Chaetoceros sp."), dfp['Total abundance']*3.53, 
                                               np.where((dfp['Taxa']=="chain diatom"), dfp['Total abundance']*6.19,
                                                                 np.where((dfp['Taxa']=="Eucampia zodiacus"), dfp['Total abundance']*3.64,
                                                                          np.where((dfp['Taxa']=="Detonula pumila"), dfp['Total abundance']*3.8,
                                                                                            np.where((dfp['Taxa']=="Pseudo-nitzschia"), dfp['Total abundance']*1.29,
                                                                                                     np.where((dfp['Taxa']=="Skeletonema"), dfp['Total abundance']*6.36,
                                                                                                              np.where((dfp['Taxa']=="Thalassionema"), dfp['Total abundance']*2.87,
                                                                                                                       np.where((dfp['Taxa']=="Phaeoceros"), dfp['Total abundance']*1.35, 
                                                                                                                                np.where((dfp['Taxa']=="thalassiosira chain"), dfp['Total abundance']*2.38,
                                                                                                                                         np.where((dfp['Taxa']=="Thalassiosira rotula"), dfp['Total abundance']*1.38, 
                                                                                                                                                  dfp['Total abundance']*1))))))))))))
        
       
        #Convert the total cell abundance/mL
        dfp['Concentrated (cells/mL)']=((dfp['Cells'])/dfp['ImagedV'])*(dfp['ConcV'])
        dfp['Total concentration (cells/mL)']=dfp['Concentrated (cells/mL)']/dfp['SamplevmL']
        dfp['Total concentration (cells/m3']=dfp['Total concentration (cells/mL)']*1000000
        
        #Create a table with species at the top to remove the non-phyto from the percentage calculation
        cells = dfp.pivot(index=['Cruise', 'Station', 'Sample', 'Month'], columns='Taxa', values='Total concentration (cells/mL)').reset_index()
        cells = cells.fillna(0)
        cells=cells.drop(columns=["background", 'Tintinnida',"detritus", "duplicate","ghost",'setae<Chaetoceros', 'zooplankton', 'Noctiluca sp.'])

        #Calculate the percent composition of phytoplankton
        new = cells.melt(id_vars=['Cruise', 'Station', 'Sample', 'Month'], value_name='CellsPerML')
        new['Total']=new.groupby(['Cruise', 'Station', 'Sample', 'Month'])['CellsPerML'].transform('sum')
        new['Percent']=(new['CellsPerML']/new['Total'])*100

#Export to csv
new.to_csv('C:/file/path.csv')
