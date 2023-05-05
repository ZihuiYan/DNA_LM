#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:01:40 2021

@author: serena-mo
"""

import numpy as np
from .code_segments import ISRemainder, Check_Note, Separator_Note, Marker_Note


class Codeword_Strand:
    
    def __init__(self, x: np.zeros(shape=0, dtype=np.int8),k:int):
        self.x = x
        self.k = k


    def encode(self):
        x = self.x
        k = self.k
        
        """
        Parameters
        ----------
        x : Qary sequrnce of length (l)

        Returns
        -------
        x_enc :         QaryString of length (N)
        k :             Length of one message block
        n :             length of one codeword block
        p :             number of blocks in one strand
        """
        x_enc = np.zeros(shape=0)
        
        l = len(x)
        p = int(np.ceil(l / k))
        
        n = int(k + np.ceil(np.log2(2*k))+4)
       
        for i in range (p-1):
            x_block_enc = None
            x = np.copy(x)
            a = i*k
            b = (i+1)*k
            x_block = x[a:b]

            check = Check_Note(x_block)
            rem = ISRemainder(x_block)
            s_1 = int(check)
            s_2 = int(rem[0])
            s_3 = int(rem[1])
            separator = Separator_Note(s_1,s_2,s_3)
            m_1 = int(rem[-1])
            m_2 = int(x[b])
            m_3 = int(x[b+1])
            mark = Marker_Note(m_1,m_2,m_3)

            x_block_enc = np.concatenate((x_block, check, separator, rem, mark))
            x_enc = np.concatenate((x_enc,x_block_enc))
        a = (p-1)*k

        x = np.copy(x)
        x_block = x[a:]
        check = Check_Note(x_block)
        rem = ISRemainder(x_block)
        s_1 = int(check)
        s_2 = int(rem[0])
        s_3 = int(rem[1])
        separator = Separator_Note(s_1,s_2,s_3)
        x_block_enc = np.concatenate((x_block,check, separator, rem),axis=0)
        x_enc = np.concatenate((x_enc,x_block_enc),axis=0)
        x_enc = np.array(x_enc,dtype=np.int8)

        return x_enc,n
    

    


    

    
    
    
    
    
    
    
    