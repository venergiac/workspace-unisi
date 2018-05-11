#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 16:04:48 2018

@author: giacomoveneri
"""

from collections import defaultdict

def group_by(grouper, data):
    grouped=defaultdict(list)
    for x in data:
        grouped[grouper(x)].append(x)
    
    return grouped

def main(argv):
    # My code here
    data = []
    for i in range(0,10):
        data.append( (i%2,i) )
    
    print('....')
    print(data)
    
    grouped = group_by(lambda x : x[0], data)
    
    print (grouped)
    
    
if __name__ == "__main__":
    main([])