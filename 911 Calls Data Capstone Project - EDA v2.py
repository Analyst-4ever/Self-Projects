# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:54:27 2019

@author: gupta
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

df = pd.read_csv("911.csv")
df.info()
df.head()

#Finding out top 5 Zip COdes
df['zip'].value_counts().head(5)

#no of unique titles
df['title'].nunique()

#reason for call
df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df['Reason'].value_counts()
sns.countplot(x='Reason',data=df,palette='viridis')

#converting timestamp column
type(df['timeStamp'].iloc[0])
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)
df['Date']=df['timeStamp'].apply(lambda t: t.date())
#assigning day of weeks (MAPPING)
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

#Reason Plot
sns.countplot(x='Day of Week',data=df,hue='Reason',palette='viridis')
# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

#grouping by month
byMonth = df.groupby('Month').count()
byMonth
byMonth['twp'].plot()

#Linear Fit
sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())

df.groupby('Date').count()['twp'].plot()
plt.tight_layout()

#traffic plot
df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()

#fire plot
df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()

#EMS plot
df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()

#day vs hour of call
dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour
plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')
sns.clustermap(dayHour,cmap='viridis')

#Day vs Month
dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth
plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')
sns.clustermap(dayMonth,cmap='viridis')
