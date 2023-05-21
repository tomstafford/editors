#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on  2023-05-18

@author: tom

OPen Editor data summary for Univeristy of Sheffield

Repo https://github.com/andreaspacher/openeditors

#Uses conda env in environment.yml
conda env create --name munge --file environment.yml

#export conda env with 
conda env export > environment.yml


"""


SAVEENV = False #toggle, export conda environment

#set up environment

import socket #to get host machine identity
import os #file and folder functions
import numpy as np #number function
import pandas as pd #dataframes!
import matplotlib.pyplot as plt #plotting function
import seaborn as sns
#matplotlib named colours https://matplotlib.org/stable/gallery/color/named_colors.html

print("identifying host machine")
#test which machine we are on and set working directory
if 'tom' in socket.gethostname():
    os.chdir('/home/tom/t.stafford@sheffield.ac.uk/A_UNIVERSITY/toys/editors')
else:
    print("Running in expected location, we are in :" + os.getcwd())
    print("Maybe the script will run anyway...")
    
#export environment in which this was last run
if SAVEENV:
    os.system('conda env export > environment.yml') 

#functions
    
def count_editors(institution,lf,df):
    '''count number of editors in editors list from that instituion'''
    #count=sum(df['affiliation'].str.contains(institution)==True)
    
    if not pd.isnull(lf.loc[institution].alt_name):
        count=sum((df['affiliation'].str.contains(lf.loc[institution].search_name)==True) |
                  (df['affiliation'].str.contains(lf.loc[institution].alt_name)==True))
    else:
        count=sum(df['affiliation'].str.contains(lf.loc[institution].search_name)==True)
    
            
    return count

# list of institutions

# See https://github.com/tomstafford/ref2021
    
filename='REF 2021 Results - All - 2022-05-06.xlsx'

df= pd.read_excel(os.path.join('data',filename),skiprows=6)

df['GPA']=pd.to_numeric(df['4*'],errors='coerce').fillna(0)/100*4+pd.to_numeric(df['3*'],errors='coerce').fillna(0)/100*3+pd.to_numeric(df['2*'],errors='coerce').fillna(0)/100*2+pd.to_numeric(df['1*'],errors='coerce').fillna(0)/100*1

df=df[df['Profile']=='Overall']

lf1=df.groupby('Institution name')['FTE of submitted staff'].sum()
lf2=df.groupby('Institution name')['GPA'].median()

lf=pd.merge(lf1,lf2,how='left',left_index=True,right_index=True)
lf.sort_values('GPA',inplace=True,ascending=False)

lf['search_name']=lf.index.str.replace('The ','')

lf.to_csv('names.csv')

#at this stage i add the alternate names by hand to this spreadsheet

lf=pd.read_csv('data/names.csv')
lf.set_index('Institution name',inplace=True)


#load editor data

df1 = pd.read_csv('data/editors1.tsv',sep='\t')
df2 = pd.read_csv('data/editors2.tsv',sep='\t')

df=pd.concat([df1,df2])

institutionlist=lf.index.values
for institution in institutionlist:
    
    lf.loc[institution,'editors']=count_editors(institution, lf,df)


lf['ed_per_FTE']=lf['editors']/lf['FTE of submitted staff']

ms=list(lf['FTE of submitted staff'].values/10)
ms_SHF =lf.loc['The University of Sheffield','FTE of submitted staff']/10
ms_STN =lf.loc['University of Southampton','FTE of submitted staff']/10
SHOWSHF=False;SHOWSTN=False
annotext='Point size scaled by FTE staff\nsubmitted to REF2021\n\n'
if SHOWSHF:
    annotext=annotext+"TUOS in red\n"
if SHOWSTN:
    annotext=annotext+"SOTON in yellow"
plt.clf()
plt.scatter(lf['GPA'],lf['ed_per_FTE'],s=ms,marker='o',alpha=0.3)
if SHOWSHF:
    plt.scatter(lf.loc['The University of Sheffield','GPA'],lf.loc['The University of Sheffield','ed_per_FTE'],marker='o',s=ms_SHF,color='red',alpha=0.8)
if SHOWSHF:
    plt.scatter(lf.loc['University of Southampton','GPA'],lf.loc['University of Southampton','ed_per_FTE'],marker='o',s=ms_STN,color='yellow',alpha=0.8)    
plt.ylim([-0.05,1])
plt.xlim([1.5,4])
plt.ylabel('Editorships per FTE research staff',fontsize=12)
plt.xlabel('Institution median GPA from REF2021',fontsize=14)
plt.title('University REF2021 results vs proportion of journal editors')
plt.annotate(annotext,(3.83,0.0),color='#1f77b4',fontsize=8,rotation=90)
plt.savefig(os.path.join('figs','gpa_vs_eds.png'),bbox_inches='tight',dpi=320)


import plotly.express as px

fig = px.scatter(lf, x="GPA", y="ed_per_FTE", size='FTE of submitted staff',hover_data=['search_name','ed_per_FTE'])
fig.update_xaxes(range=[1.5, 4])
fig.update_yaxes(range=[-0.05,1])  
fig.write_html("figs/plotly.html")

