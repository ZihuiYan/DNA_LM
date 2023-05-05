#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:54:26 2021

@author: serena-mo
"""
import numpy as np
from .decoder_function import Decode_Deletion, Decode_Insertion, Decode_Substitution, Block_End
from .code_segments import ISRemainder, Check_Note


class Marker_Correct_Decode:
    def __init__(self,r:np.zeros(shape=0, dtype=np.int8),k:int):
        self.r = r
        self.k = k
        
    def decode(self):
        r = self.r
        k = self.k
        r = r[2:]
        '''
        marker code is correct 
        -------
        deal with one edit error in codeword block

        '''
        length_remainder = int(np.ceil(np.log2(2*k)))
        rec_msg = r[0:k]
        msg_rem = ISRemainder(rec_msg)
        msg_check = Check_Note(rec_msg)[0]
        block_end = 0
       
            
        if r[k+1] == r[k+2] == r[k+3]: 
            rec_rem = r[k+4: k+length_remainder+4]
            if np.array_equal(msg_check, r[k]):
                
                if np.array_equal(msg_rem, rec_rem):
                    '''whole block is correct'''
                    correct_rem = rec_rem
                    block_boundary = 1
                    block_end = k + 6 + length_remainder
                else:
                    '''remainder has one error'''
                    correct_rem = msg_rem
                   
                    if len(r) >= 2*k+length_remainder+4:
                        block_end = Block_End(r,correct_rem,length_remainder,k) + 2
                        block_boundary = 1
                    else: 
                        block_boundary = 1
                        block_end = 0
                        
            else:
               
                if np.array_equal(msg_rem, rec_rem):
                    '''check has one sub'''
                    correct_rem = rec_rem
                    block_boundary = 1
                    block_end = k + 6 + length_remainder
                else:
                    '''msg has one sub'''
                    rec_msg = Decode_Substitution(rec_msg, rec_rem, k)
                    correct_rem = rec_rem
                    block_boundary = 1
                    block_end = k + 6 + length_remainder
                    
                    
                        
                        
        elif r[k] == r[k+1] == r[k+2] != r[k+3]:
            rec_rem = r[k+3 : k+3+length_remainder]
            if np.array_equal(msg_rem, rec_rem):
                '''msg is correct'''
                correct_rem = msg_rem
                block_end = k + 5 + length_remainder
                
            else:
                '''msg has one del'''
                rec_msg = Decode_Deletion(rec_msg[0:k-1], rec_rem, k)
                correct_rem = rec_rem
                block_end = k + 5 + length_remainder
            block_boundary = 1
            
                        
        elif r[k+2] == r[k+3] == r[k+4] and r[k+2]!=r[k+1]:
            rec_rem = r[k+5: k+5+length_remainder]
            if np.array_equal(msg_rem, rec_rem):
                '''msg is correct'''
                correct_rem = msg_rem
            else:
                '''msg has one ins'''
                rec_msg = Decode_Insertion(r[0:k+1], rec_rem, k)
                correct_rem = rec_rem
            block_boundary = 1
            block_end = k + 7 + length_remainder
            
        else:
            '''separator has one error'''
            if msg_check == r[k]:
                if np.array_equal(msg_rem, r[k+3: k+3+length_remainder]):
                    correct_rem = msg_rem
                    block_boundary = 1
                    block_end = k+5+length_remainder
                elif np.array_equal(msg_rem, r[k+4: k+4+length_remainder]):
                    correct_rem = msg_rem
                    block_boundary = 1
                    block_end = k+6+length_remainder
                elif np.array_equal(msg_rem,r[k+5: k+5+length_remainder]):
                    correct_rem = msg_rem
                    block_boundary = 1
                    block_end = k+7+length_remainder
                else:
                    '''more than one error in this block'''
                    rec_msg = np.empty(k,dtype=np.int8)
                    rec_msg.fill(6)
                    correct_rem = np.empty(length_remainder,dtype = np.int8)
                    correct_rem.fill(6)
                    block_boundary = 0
            else: 
                '''more than one error in this block'''
                rec_msg = np.empty(k,dtype=np.int8)
                rec_msg.fill(6)
                correct_rem = np.empty(length_remainder,dtype = np.int8)
                correct_rem.fill(6)
                block_boundary = 0
                
        return rec_msg, block_boundary, block_end 
    
'''x = [1,1,2,0,1,2,2,3,1,1,1,0,0,1,1,0,3,3,0,1,0,0,0,1,3,3,3,0,0,1,0]
print(Marker_Correct_Decode(x,5).Decode())'''

