#!/usr/bin/env python
# coding: utf-8



import numpy as np

def Get_Remainder(a, k):
    t = np.ceil(np.log2(2*k))
    a = list(a)
    a_0 = 0
    a_1 = 0
    for i in range(len(a)):
        a_0 += (int(a[i])%2) * 2**(t-1-i)
        a_1 += (int(a[i])//2) *2 **(t-1-i)
    return a_0,a_1

def Decode_Substitution(x, a, k):
    
    a_0,a_1 = Get_Remainder(a,k)
    x = list(x)
    remainder_x_0 = remainder_x_1 = 0
    for i in range (len(x)):
        remainder_x_0 +=  (x[i]%2) * (i+1)
        remainder_x_1 += (x[i]//2) * (i+1)
    sub_symbol_0 = int((remainder_x_0 - a_0) % (2*k))
    sub_symbol_1 = int((remainder_x_1 - a_1) % (2*k))
    
    if 0 < sub_symbol_0 <= k:
        sub_x_0 = (x[sub_symbol_0 - 1] % 2 + 1) % 2
    elif k < sub_symbol_0 < 2*k:
        sub_symbol_0 = 2*k - sub_symbol_0
        sub_x_0 = (x[sub_symbol_0 - 1] % 2 + 1) % 2
    else:
        if sub_symbol_1 <= k:
            sub_x_0 = x[sub_symbol_1 - 1] % 2
        else: 
            sub_position = 2*k - sub_symbol_1
            sub_x_0 = x[sub_position - 1] % 2
        
    if 0 < sub_symbol_1 <= k:
        sub_x_1 = (x[sub_symbol_1 - 1]//2 + 1) % 2
    elif k < sub_symbol_1 < 2*k:
        sub_symbol_1 = 2*k - sub_symbol_1
        sub_x_1 = (x[sub_symbol_1 - 1]//2 + 1) % 2
    else:
        sub_x_1 = x[sub_symbol_0 - 1] // 2
    
    sub_x = sub_x_1 * 2 + sub_x_0
    if sub_symbol_0 == 0:
        x[sub_symbol_1 - 1] = sub_x
    else:
        x[sub_symbol_0 - 1] = sub_x
    x = np.array(x,dtype=np.int8)
    return x
    
'''x = [1,0,0,0,0]
a = [0,2,0,3]
k = 5
print(Get_Remainder(a, k))

print(Decode_Substitution(x, a, k))'''


def Decode_Deletion(x,a,k):
    a_0,a_1 = Get_Remainder(a,k)
    x = list(x)
    sum_x_0 = sum_x_1 = remainder_x_0 = remainder_x_1 = 0
    
    x_0 = []
    x_1 = []
    for i in range(len(x)):
        x_0.append(x[i] % 2)
        x_1.append(x[i] // 2)
    
    for i in range (len(x)):
        sum_x_0 += x[i] % 2
        remainder_x_0 +=  (x[i] % 2) * (i+1)
        sum_x_1 += x[i] // 2
        remainder_x_1 += (x[i] // 2) * (i+1)
    del_symbol_0 = int((a_0 - remainder_x_0) % (2*k))
    del_symbol_1 = int((a_1 - remainder_x_1) % (2*k))

    
    if 0 <= del_symbol_0 <= sum_x_0:
        del_x_0 = 0
    
    else:
        del_x_0 = 1
        
    if 0 <= del_symbol_1 <= sum_x_1:
        del_x_1 = 0
    else:
        del_x_1 = 1
        
    if del_symbol_0 == 0:
        x_0.append(0)
    elif 0 < del_symbol_0 <= sum_x_0:
        x_0.reverse()
        for i in range (k):
            if x_0[0:i].count(1) == del_symbol_0:
                x_0.insert(i, del_x_0)
                x_0.reverse()
                break
    else:
        del_symbol_0 = del_symbol_0 - sum_x_0 - 1
        for i in range(k):
            if x_0[0:i].count(0) == del_symbol_0:
                x_0.insert(i, del_x_0)
                break
            
    if del_symbol_1 == 0:
        x_1.append(0)
                
    elif 0 < del_symbol_1 <= sum_x_1:
        x_1.reverse()
        for i in range (k):
            if x_1[0:i].count(1) == del_symbol_1:
                x_1.insert(i, del_x_1)
                x_1.reverse()
                break
    else:
        del_symbol_1 = del_symbol_1 - sum_x_1 - 1
        for i in range(k):
            if x_1[0:i].count(0) == del_symbol_1:
                x_1.insert(i, del_x_1)
                break
    l = int((len(x_0)+len(x_1)) // 2)
    if l != k:
        correct_x = np.empty(k,dtype=np.int8)
        correct_x.fill(6)
    else:
        correct_x = []
        for i in range(l):
            correct_x.append(int(x_0[i] + x_1[i] * 2))
        
    correct_x = np.array(correct_x,dtype=np.int8)
    return correct_x



def Decode_Insertion(x,a,k):
    a_0,a_1 = Get_Remainder(a,k)
    x = list(x)
    sum_x_0 = sum_x_1 = remainder_x_0 = remainder_x_1 = 0
    
    x_0 = x.copy()
    for i in range(len(x)):
        x_0[i]= x[i] % 2 

    
    x_1 = x.copy()
    for i in range(len(x)):
        x_1[i]= x[i] // 2 

    
    for i in range (len(x)):
        sum_x_0 += x[i] % 2
        remainder_x_0 +=  (x[i] % 2) * (i+1)
        sum_x_1 += x[i] // 2
        remainder_x_1 += (x[i] // 2) * (i+1)
    ins_symbol_0 = int((remainder_x_0 - a_0) % (2*k))
    ins_symbol_1 = int((remainder_x_1 - a_1) % (2*k))

    
    if 0 <= ins_symbol_0 < sum_x_0:
        x_0.reverse()
        for i in range (k+1):
            if x_0[0:i].count(1) == ins_symbol_0:
                x_0.pop(i)
                x_0.reverse()
                break
    else:
        ins_symbol_0 = ins_symbol_0 - sum_x_0
        for i in range(k+1):
            if x_0[0:i].count(0) == ins_symbol_0:
                x_0.pop(i)
                break
                
    if 0 <= ins_symbol_1 < sum_x_1:
        x_1.reverse()
        for i in range (k+1):
            if x_1[0:i].count(1) == ins_symbol_1:
                x_1.pop(i)
                x_1.reverse()
                break
    else:
        ins_symbol_1 = ins_symbol_1 - sum_x_1
        for i in range(k+1):
            if x_1[0:i].count(0) == ins_symbol_1:
                x_1.pop(i)
                break

    correct_x = []
    for i in range(k):
        correct_x.append(int(x_0[i] + x_1[i] * 2))
        
    correct_x = np.array(correct_x,dtype=np.int8)
    return correct_x

def Block_End(r,a,t,k):
    '''
    Parameters
    ----------
    r : received strand
    a : correct remainder sequence
    t : the length of remainder
    k : the length of message block

    Returns
    -------
    the end position of first codeword block 

    '''
    if r[k+3+t]==r[k+4+t] and r[k+3+t]!= a[-1] and r[k+4+t]!= r[k+5+t]:
        '''remainder has one del'''
        end_position = k+3+t
    elif r[k+4+t]==r[k+5+t] != a[-1]:
        '''remainder has one sub'''
        end_position = k+4+t
    elif r[k+5+t]==r[k+6+t] != a[-1] and r[k+4+t]==a[-1]:
        '''remainder has one ins'''
        end_position = k+5+t
    else:
        end_position = k+4+t
    return end_position





