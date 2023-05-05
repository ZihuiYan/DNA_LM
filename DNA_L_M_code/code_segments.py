#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-

import numpy as np


def SRemainder(x):
    '''computes ($ix_i^s \pmod {2k}$)
    x: message sequecnce
    k: length of x 
    '''
    x = list(x)
    a0 = 0
    a1 = 0
    k = len(x)
    t = np.ceil(np.log2(2*k))
    for i in range (len(x)):
        a0 += (int(x[i])%2) * (i+1)
        a1 += (int(x[i])//2) * (i+1)
    a0 = a0 % (2 * k)
    a1 = a1 % (2 * k)
    seq_a0 = bin(a0).replace('0b','')
    seq_a1 = bin(a1).replace('0b','')
    while len(seq_a0) < t:
        seq_a0 = '0'+seq_a0
    while len(seq_a1) < t:
        seq_a1 = '0'+seq_a1
    return seq_a0,seq_a1



def ISRemainder(x):
    
    a0 = SRemainder(x)[0]
    a1 = SRemainder(x)[1]
    a = str()
    for i in range(len(a0)):
        ai = int(a0[i]) + int(a1[i])*2
        a += str(ai)
    a = np.array(list(a),dtype=np.int8)
    return a




def Check_Note(x):
    c = np.sum(x) % 4
    return np.array([c],dtype=np.int8)


def Separator_Note(a,b,c):
    s = (a + 2) % 4
    if s!=b and s!=c:
        sep = s
    else:
        s = (s+1)%4 
        if s !=b and s != c:
            sep = s % 4
        else:
            sep = (s+2) % 4
    sep = np.array([sep,sep,sep],dtype=np.int8)
    return sep



def Marker_Note(a,b,c):
    m = (a + 2) % 4
    if m !=b and m!=c:
        marker = m
    else:
        m =(m+1)%4
        if m !=b and m !=c:
            marker = m
        else:
            marker = (m+2) % 4
    marker = np.array([marker,marker],dtype = np.int8)
    return marker

def Marker_Detection():
    marker_book = set()
    for a in range(4):
        for b in range(4):
            for c in range(4):
                m = Marker_Note(a,b,c)
                markercode = (np.concatenate(([a],m,[b],[c])))
                markercode = ''.join((str(i) for i in markercode))
                marker_book.add(markercode)
    return marker_book



