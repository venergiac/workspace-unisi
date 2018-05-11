#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 10:23:33 2018

@author: giacomoveneri
"""

import json,sys


def update(k,v):
    d = {}
    d[k]=v
    return d 

    
    
def processRow(row):
    value = row.split(';', 2)
    #print(value)
    if len(value)<=1:
        return 
    keys = value[0].split('/')
    v=value[1]
    
    try:
        v=[float(v)]
    except:
        v=[v]
        
    for i, e in reversed(list(enumerate(keys))):
        v = update(e,v)
    
    return v

def updateTree(dic, tree):
    #print("IN %s -> OUT %s" % (dic, json.dumps(tree, indent = 4)))
    #print()
    for key in dic:
        value=dic[key]
        subtree = tree.get(key)

        if subtree and isinstance(subtree, dict):
            updateTree(value,subtree)
        elif subtree and isinstance(subtree, list) and isinstance(value, list):
            subtree.extend(value)
        elif not(subtree):
            tree.update(dic)
        else:
            sys.stderr.write ("ERROR: incoherent data type %s vs %s" % (dic, json.dumps(tree, indent = 4)))
    


fid = open('./output.par', mode='r')
content = fid.readlines()
content = [x.replace(' ', '').strip() for x in content]
rows=content

#x = [processRow(row) for row in rows]
'''for row in rows:
    v = processRow(row)
    if (v):
        x.append(v)
'''
txt = "HP;1\nMN;stringval\nIS/VD1;32.00\nIS/HD1;1.34\nIS/E/ID;362.0000000\n"
rows = txt.split('\n')
x = []

t={}
for row in rows:
    v = processRow(row)
    if (v):
        updateTree(v,t)

print (json.dumps(t, indent = 4))