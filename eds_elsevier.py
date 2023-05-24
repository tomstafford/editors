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
SHOWENV = False #use Environment rather than Overall profile
LOADING = False #toggle, if loading rather than regenerating summary data

#set up environment

import socket #to get host machine identity
import os #file and folder functions
import numpy as np #number function
import pandas as pd #dataframes!
import matplotlib.pyplot as plt #plotting function
#import seaborn as sns
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
    
def count_editors(institution,publisher,lf,df):
    '''count number of editors in editors list from that instituion'''
    #count=sum(df['affiliation'].str.contains(institution)==True)
    
    if publisher =='All':
    
        if not pd.isnull(lf.loc[institution].alt_name):
            count=sum((df['affiliation'].str.contains(lf.loc[institution].search_name)==True) |
                      (df['affiliation'].str.contains(lf.loc[institution].alt_name)==True))
        else:
            count=sum(df['affiliation'].str.contains(lf.loc[institution].search_name)==True)
        
    else:
        if not pd.isnull(lf.loc[institution].alt_name):
            count=sum(
                    ( (df['affiliation'].str.contains(lf.loc[institution].search_name)==True) |
                      (df['affiliation'].str.contains(lf.loc[institution].alt_name)==True)) &
                        (df['publisher']==publisher)
                        )
        else:
            count=sum((df['affiliation'].str.contains(lf.loc[institution].search_name)==True) &
                      (df['publisher']==publisher))
        
    return count

# list of institutions

# See https://github.com/tomstafford/ref2021
    
filename='REF 2021 Results - All - 2022-05-06.xlsx'

df= pd.read_excel(os.path.join('data',filename),skiprows=6)

df['GPA']=pd.to_numeric(df['4*'],errors='coerce').fillna(0)/100*4+pd.to_numeric(df['3*'],errors='coerce').fillna(0)/100*3+pd.to_numeric(df['2*'],errors='coerce').fillna(0)/100*2+pd.to_numeric(df['1*'],errors='coerce').fillna(0)/100*1

if SHOWENV:
    df=df[df['Profile']=='Environment']
else:
    df=df[df['Profile']=='Overall']

lf1=df.groupby('Institution name')['FTE of submitted staff'].sum()
lf2=df.groupby('Institution name')['GPA'].median()

lf=pd.merge(lf1,lf2,how='left',left_index=True,right_index=True)
lf.sort_values('GPA',inplace=True,ascending=False)

lf['search_name']=lf.index.str.replace('The ','')

lf.to_csv('names.csv')

GPA=lf['GPA']

#at this stage i add the alternate names by hand to this spreadsheet

lf=pd.read_csv('data/names.csv')

lf['GPA']=GPA.values

lf.set_index('Institution name',inplace=True)



#load editor data

df1 = pd.read_csv('data/editors1.tsv',sep='\t')
df2 = pd.read_csv('data/editors2.tsv',sep='\t')

df=pd.concat([df1,df2])


publishers=df['publisher'].unique()

publishers=np.append(publishers,'All')

institutionlist=lf.index.values


for publisher in publishers:

    for institution in institutionlist:
        
        lf.loc[institution,publisher]=count_editors(institution, publisher,lf,df)


lf.to_csv(os.path.join('data','by_publisher.csv'))

if LOADING:
    lf=pd.read_csv(os.path.join('data','by_publisher.csv'))

#publisher count
lf[publishers].sum().sort_values(ascending=False).astype(int).to_markdown(os.path.join('data','publisher_table.txt'))

savename='concentration_eds.png'

totals=[]
colors=['red','blue','orange','darkgreen','k','grey']
labelnames=['Springer Nature','Cambridge University Press','Elsevier','Frontiers','All','others']

plt.clf()

for publisher in publishers:
    if publisher==labelnames[0]:
        color=colors[0]
        lw=1.25
        alpha=1
    elif publisher==labelnames[1]:
        color=colors[1]
        lw=1.25
        alpha=1
    elif publisher==labelnames[2]:
        color=colors[2]
        lw=1.25
        alpha=1
    elif publisher==labelnames[3]:
        color=colors[3]
        lw=1.25
        alpha=1
    elif publisher==labelnames[4]:
        color=colors[4]
        lw=1.75
        alpha=1
    else:
        color=colors[5]
        lw=0.25
        alpha=0.6
        
    y=lf[publisher].sort_values(ascending=False).cumsum()
    y=y.values/max(y.values)*100
    plt.plot(y,lw=lw,alpha=alpha,color=color,label=publisher)
    totals.append(sum(y<100)+1)

plt.ylim([0,105])
plt.xlabel('Number of institutions')
plt.ylabel('Cumulative percentage of editors')


from matplotlib.patches import Patch



legend_elements = [Patch(facecolor=color, alpha=0.75, label=labelname) for color,labelname in zip(colors,labelnames)]
 
plt.legend(handles=legend_elements, title="Journal publisher",loc='lower right')
plt.title('Institutional concentration of journal editors, by publisher')
plt.savefig(os.path.join('figs',savename),bbox_inches='tight',dpi=320)

pd.DataFrame(totals,publishers).sort_values(by=0).to_markdown(os.path.join('data','alleds.md'))