#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 11:00:46 2021

@author: serena-mo
"""

import numpy as np
from .code_segments import ISRemainder, Check_Note

class Marker_Uncorrect_Decode:
    def __init__(self,r:np.zeros(shape=0, dtype=np.int8),k:int):
        self.r = r
        self.k = k
        
        
        
    def correct_block(self,t):
        r = self.r
        k = self.k
        length_remainder = int(np.ceil(np.log2(2*k)))
        rec_msg = r[0:k]

        if len(r) >= t+k+6 and r[k+t+3] == r[k+t+4] == r[k+t+5] and r[k+t+3]!= r[k+t+2]: 
            '''code displacement of t positions'''
            rec_msg = r[2+t:k+2+t]
            rec_rem = r[k+t+6:k+6+t+length_remainder]
            msg_check = Check_Note(rec_msg)
            msg_rem = ISRemainder(rec_msg)
            if msg_check == r[k+2+t] and np.array_equal(msg_rem, rec_rem):
                correct_block = 1
                
            else:
                correct_block = 0
        else: correct_block = 0
        return correct_block
    
    def decode(self):
        r = self.r
        k = self.k
        length_remainder = int(np.ceil(np.log2(2*k)))
        i=0
        while i <= 4:
            displacement = i-2
            if Marker_Uncorrect_Decode.correct_block(self,displacement) == 1:
                block_boundary = 1
                correct_msg = r[2+displacement:k+2+displacement]
                block_end = k+6+displacement+length_remainder
                break
            else:
                block_boundary = 0
                block_end = 0
                i=i+1
        if block_boundary == 0:
            '''more than one error in this block'''
            correct_msg = np.empty(k,dtype=np.int8)
            correct_msg.fill(6)
                
        return correct_msg, block_boundary, block_end
        
'''x = [1,1,2,1,1,2,1,1,1,0,0,3,2]
print(Marker_Uncorrect_Decode(x,5).Decode())'''
     
        
        
        
        
        
        
        
        
        
        