#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 10:58:53 2021

@author: serena-mo
"""

import numpy as np
import random

class Error_Type:
    def __init__(self, y:np.ndarray, sub_pr, ins_pr, del_pr):
        self.y = y
        self.sub_pr = sub_pr
        self.ins_pr = ins_pr
        self.del_pr = del_pr


    """
    Generates a random error sequence based on the given probabilities.
    
    param:
    sub_pr: Probability of a substitution error.
    y: encoding sequence
    ins_pr: Probability of an insertion error.
    del_pr: Probability of a deletion error.

    Returns:
    A tuple consisting of the error sequence and a list of error positions.
    """

    def random_error(self):
        y = np.copy(self.y)
        sub_pr = np.copy(self.sub_pr)
        ins_pr = np.copy(self.ins_pr)
        del_pr = np.copy(self.del_pr)
        error_pos = []
        unit_list = [0,1,2,3]
        error_code = []
        interval_n = 10 ** 5

        for i in range(len(y)):
            ins_times = 0
            while ins_times < 1:
                if random.randint(1, interval_n) <= interval_n * ins_pr:
                    error_code.append(random.choice(unit_list))
                    error_pos.append({'type': 'ins', 'pos': i, 'symbol': error_code[-1]})
                else:
                    break
            if random.randint(1, interval_n) <= interval_n * del_pr:
                error_pos.append({'type': 'del', 'pos': i, 'symbol': y[i]})
                continue
            else:
                if random.randint(1, interval_n) <= interval_n * sub_pr:
                    error_symbols = [j for j in range(4)]
                    error_symbols.remove(y[i])
                    error_code.append(np.random.choice(error_symbols))
                    error_pos.append({'type': 'sub', 'pos': i, 'symbol': error_code[-1]})
                else:
                    error_code.append(y[i])

        error_code_array = np.array(error_code)
        return error_code_array, error_pos
