#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 15:22:53 2021

@author: serena-mo
"""

import numpy as np
from .marker_correct_decode import Marker_Correct_Decode
from .marker_uncorrect_decode import Marker_Uncorrect_Decode
from .code_segments import Marker_Detection


class Strand_Decode:


    def __init__(self, received_sequence: np.ndarray, block_length: int, num_blocks: int):
        self.received_sequence = received_sequence
        self.block_length = block_length
        self.num_blocks = num_blocks
        '''
        received_sequence: received sequence
        block_length: the length of block
        num_blocks: the number of blocks
        '''
    def decode(self):
        received_sequence = self.received_sequence
        k = self.block_length
        p = self.num_blocks

        i = 1
        or_received_sequence = np.concatenate((np.array([1, 1]), received_sequence))
        correct_msg = np.empty(0, dtype=np.int8)
        length_block = k + 4 + int(np.ceil(np.log2(2 * k)))

        while i < p:
            if or_received_sequence[0] == or_received_sequence[1]: # markercoder is correct
                rec_msg, block_boundary, block_end = Marker_Correct_Decode(or_received_sequence, k).decode()
            else:
                rec_msg, block_boundary, block_end = Marker_Uncorrect_Decode(or_received_sequence, k).decode()

            if block_boundary == 1 and len(rec_msg) == k:
                or_received_sequence = or_received_sequence[block_end:]

            else:
                rec_msg, block_boundary, block_end = Marker_Uncorrect_Decode(or_received_sequence, k).decode()
                if block_boundary == 1 and len(rec_msg) == k:
                    or_received_sequence = or_received_sequence[block_end:]
                else:
                    # print("Synchronization Failed")
                    for j in range(6):
                        connect = or_received_sequence[length_block - j + 3:length_block - j + 8]
                        connect_marker = ''.join((str(i) for i in connect))
                        if connect_marker in Marker_Detection():
                            block_end = length_block - j + 4
                            or_received_sequence = or_received_sequence[block_end:]
                            break
                    else:
                        block_end = length_block
                        or_received_sequence = or_received_sequence[block_end + 2:]
                    rec_msg = np.empty(k, dtype=np.int8)
                    rec_msg.fill(6)

            correct_msg = np.concatenate([correct_msg, rec_msg])
            i = i + 1

        if i == p:
            if length_block - p <= len(or_received_sequence) <= length_block + 2 + p:
                if len(or_received_sequence) >= length_block + 1 and or_received_sequence[0] == or_received_sequence[1]: # markercoder is correct
                    rec_msg, block_boundary, block_end = Marker_Correct_Decode(or_received_sequence, k).decode()
                else:
                    rec_msg, block_boundary, block_end = Marker_Uncorrect_Decode(or_received_sequence, k).decode()
                if block_boundary == 0:
                    rec_msg, block_boundary, block_end = Marker_Uncorrect_Decode(or_received_sequence, k).decode()

            else:
                # print("more than one error in this block")
                rec_msg = np.empty(k, dtype=np.int8)
                rec_msg.fill(6)

            correct_msg = np.concatenate([correct_msg, rec_msg])

            correct_msg = np.array(correct_msg, dtype=np.int8)
        return correct_msg


