#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 07:49:59 2018

@author: giacomoveneri
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import ttest_ind
from scipy.stats import wilcoxon
from scipy.stats import normaltest
from scipy.stats import ranksums
from scipy.stats import f_oneway

import numpy as np

PATIENT="PT"
CTRL="CTRL"
SBJ="SBJ"
GRP="GRP"
GRP_FENOTIPO="Fenotipo"

FZ_EXEC="FUNZ. ESECUTIVE"
FZ_VIS_SPAT="AB VISUO-SPAZIALI"
FZ_LAN="LINGUAGGIO"
FZ_FLUEN="FLUENZA VERBALE"
FZ_MAL_ETA="Storia di mal (mesi)"
FZ_MEMORIA="MEMORIA"

SEQUENCING="SEQUENCING"
DNROI="DNROI"
DNROI_OUT="DNROI-OUT"
NFIX="NFIX"
NFIX_OUT="NFIX-OUT"
DURATION="DURATION"

TMT=[SEQUENCING, DNROI, DNROI_OUT, NFIX, NFIX_OUT, DURATION]

def show_box(data,indkey,groupkey):
    gb = data.groupby(groupkey)
    idx=[]
    l=[]
    d=[]
    i=1
    for x in gb.groups:
        #d=np.append(d, gb.get_group(x)[indkey])
        d1=gb.get_group(x)
        d.append(d1[indkey].values)
        idx.append(i)
        l.append(x)
        i=i+1
    plt.figure(figsize=(10,10))
    plt.boxplot(d)
    plt.xticks(idx, l)
    plt.show()
    r,pvalue=f_oneway(*d)
    print("%s: r=%s p-value=%s %s"%(indkey, r,pvalue, ("**" if pvalue<0.05 else "")))
    #
    #plt.show()


def show_corr(data, col1,col2):
    plt.figure(figsize=(10,10))
    plt.scatter(data[col1], data[col2])
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.show()
    r,pvalue=pearsonr(data[col1], data[col2])
    print("r=%s p-value=%s %s"%(r,pvalue, ("**" if pvalue<0.05 else "")))
    
    
def show_diff(data,grp1,grp2, ind):
    a=data[ind][data[GRP]==grp1]
    b=data[ind][data[GRP]==grp2]
    
    (t,pvalue)=ttest_ind(a, b, axis=0, equal_var=True, nan_policy='propagate')
    d = np.array ([a,b])
    
    k2, p = normaltest(a)
    alpha = 0.05

    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("")
    else:
        print(grp1 + " not normal : The null hypothesis cannot be rejected p: " + str(p))
        
    k2, p = normaltest(b)
    if p < alpha:
        print("")
    else:
        print(grp2 + " not normal : The null hypothesis cannot be rejected p: " + str(p))
   
    plt.boxplot(d)
    plt.xticks([1, 2], [grp1,grp2])
    plt.show()
    print("%s: TTEST t=%s p-value=%s %s"%(ind,t,pvalue, ("**" if pvalue<alpha else "")))
    
    (t,pvalue)= ranksums(a,b)
    print("%s: ranksums T=%s p-value=%s %s"%(ind,t,pvalue, ("**" if pvalue<alpha else "")))
    

basepath= "/Users/giacomoveneri/Documents/workspace-unisi/bin"#os.path.dirname(os.path.abspath(__file__)) 

tnps = pd.read_excel(os.path.join(basepath,"..", "data","analysis","TNPS_26.4.18.xls.xlsx"))
data = pd.read_excel(os.path.join(basepath,"..", "data","analysis","output.xlsx"))


data[SBJ] = data[SBJ].apply(lambda x: x[:x.find('_')])

tnps[FZ_EXEC] = tnps[FZ_EXEC].apply(lambda x: float(x[:x.find('/')]))
tnps[FZ_VIS_SPAT] = tnps[FZ_VIS_SPAT].apply(lambda x: float(x[:x.find('/')]))
tnps[FZ_LAN] = tnps[FZ_LAN].apply(lambda x: float(x[:x.find('/')]))
tnps[FZ_FLUEN] = tnps[FZ_FLUEN].apply(lambda x: float(x[:x.find('/')]))
tnps[FZ_MEMORIA] = tnps[FZ_MEMORIA].apply(lambda x: float(x[:x.find('/')]))

#FILTER ONLY OK
data = data[(data[GRP] == "CTRL") | (data[GRP] == "PT") ]

#PATIENTS JOINED
data = pd.merge(data, tnps, left_on=SBJ, right_on=SBJ, how='left', sort=False);

#USE ONLY THE BEST
idx = data.groupby([SBJ])[SEQUENCING].transform(max)==data[SEQUENCING]

#AVERAGING SAME VALUES
data_AVG=data[idx].groupby([GRP, SBJ], as_index=False).mean()

#EXPORT TO EXCEL
writer = pd.ExcelWriter(os.path.join(basepath,"..", "data","analysis","joined.xlsx"))
data.to_excel(writer,'orig')
data[idx].to_excel(writer,'max')
data_AVG.to_excel(writer,'avg')
writer.save()


#USING AVERAGED
data=data_AVG


for V in TMT:
    show_diff(data,"CTRL","PT",V)

#FILETR BY PATIENTS
data_PT = data.loc[data[GRP] == PATIENT]

data=data_PT



for V in TMT:

    show_corr(data,V, FZ_EXEC)
    show_corr(data,V, FZ_VIS_SPAT)
    show_corr(data,V, FZ_LAN)
    show_corr(data,V, FZ_FLUEN)
    show_corr(data,V, FZ_MAL_ETA)
    show_corr(data,V, FZ_MEMORIA)

#PATIENTS W FENOTIPO
data = pd.merge(data, tnps[[SBJ, GRP_FENOTIPO]], left_on=SBJ, right_on=SBJ, how='left', sort=False);
for V in TMT:
    show_box(data[[SBJ, GRP_FENOTIPO, V]], V,GRP_FENOTIPO)
