#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 09:47:35 2018

@author: giacomoveneri
"""

import csv,functools
import sys
import os
import numpy
import matplotlib.pyplot as plt
from shutil import copyfile


X_MAX=261
Y_MAX=240
VALID_EXP_ID=['1','3','5','7']
SEQUENCE=['1','A','2','B','3','C','4','D','5','E','Z']


def comp(a,b):
    i1=SEQUENCE.index(a[0])
    i2=SEQUENCE.index(b[0])
    return (i1-i2)


def buildRegionFile(sequence, directoryname):
       with open(os.path.join(directoryname,"regions_template.csv"), 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=';')
        i=0
        regions=[]
        for row in reader:
            regions.append([sequence[i], row[1],row[2],50,80])
            i+=1
            
        #order
        regions = sorted(regions, key=functools.cmp_to_key(comp))
        numpy.savetxt(os.path.join(directoryname,sequence+".csv"), numpy.asarray(regions), delimiter="\t", fmt='%s')
            


def processData(row,experiments):
    #print('%s %s %s %s' % (row[0], row[2], row[6], row[8]))
    return (row[8], float(row[0]), float(row[2]),float(row[6]),float(row[4]))

def readDataFile(filename,subject, enabled, experiments):
   if (os.path.isfile(filename)):
       readStandardDataFile(filename,subject, enabled, experiments)
   else:
       readGCDataDirectory(filename,subject, enabled, experiments)
       
       
       
def getDirectory(baseDirectory, experiment):
    dirs = os.listdir(baseDirectory)
    for directory in dirs:
        if experiment in directory:
            return directory
       
def readGCDataDirectory(filename,subject, enabled, experiments):
    
    baseDirectory = os.path.dirname(filename)
    for i in range(len(experiments)):
        
        #search directory
        expDirectory = getDirectory(baseDirectory, experiments[i])
        print("%s %s" % (experiments[i],expDirectory))
        
        #build directory
        directory = os.path.join(os.path.dirname(filename) , experiments[i]).replace("_SRC","")
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        #build region
        buildRegionFile(experiments[i], os.path.join(directory,'..','..','..','regions'))
        
        #copy file
        copyfile(os.path.join(baseDirectory,expDirectory,"DATA.txt"), os.path.join(directory,"DATA.txt"))
        print("%s %s" % (os.path.join(baseDirectory,expDirectory,"DATA.txt"), os.path.join(directory,"DATA.txt")))
    
    return
       
def readStandardDataFile(filename,subject, enabled, experiments):
       with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=' ')
            lastexpid=-999999

            i=-1
            data=[]
            for row in reader:
                (expid,x,y,t,p) = processData(row,experiments)

                if expid:
                    if expid!=lastexpid:
                    
                        if lastexpid in VALID_EXP_ID:
                            v_max = max(data, key=lambda e: float(e[0]))
                            v_min = min(data, key=lambda e: float(e[0]))
                            print('save list data %s-%s exp=%s' % (v_min, v_max, experiments[i]))
                            directory = os.path.join(os.path.dirname(filename) , experiments[i]).replace("_SRC","")
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            numpy.savetxt(os.path.join(directory,"DATA.txt"), numpy.asarray(data), delimiter=" ", fmt='%g')
                            plt.figure(1)
                            plt.plot([row[0] for row in data],[row[1] for row in data], 'r',linewidth=1.0)
                            plt.ylabel( subject + " " +experiments[i])
                            plt.figure(2)
                            plt.subplot(111)
                            plt.plot([row[3] for row in data],[row[0] for row in data], 'g',linewidth=1.0)
                            plt.subplot(111)
                            plt.plot([row[3] for row in data],[row[1] for row in data], 'b',linewidth=1.0)
                            plt.ylabel( subject + " " +experiments[i])
                            plt.show()
                            buildRegionFile(experiments[i], os.path.join(directory,'..','..','..','regions'))
                            data=[]
                        
                        lastexpid=expid
                        if expid in VALID_EXP_ID:
                            i+=1
    
                    if expid in VALID_EXP_ID:
                        if (x>0 and y>0 and x<=X_MAX and y<=Y_MAX):
                            data.append( [x,y,p,t,0,0] )
                            #print(i)
                            #print("%s %s-%s %s %s %s" % (subject,lastt,t,expid,experiments[i], i))
                        
                        
                        
def processMetaData(row):
    return (row[0], True, (row[2], row[4], row[6], row[8]))      

def readMetaDataFile(directoryname, filename):
   with open(os.path.join(directoryname,filename), 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            #print(row)
            (subject, enabled, experiments) = processMetaData(row)
            if (enabled):
                readDataFile(os.path.join(directoryname,subject, "DATA.txt"),subject, enabled, experiments)

def main(argv):
    # My code here
    readMetaDataFile('../DATA/TMT_SRC/CTRL/','metadata.csv')
    
    readMetaDataFile('../DATA/TMT_SRC/SLA/','metadata.csv')
    
    pass

if __name__ == "__main__":
    main(sys.argv)