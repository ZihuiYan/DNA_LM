#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 16:04:04 2021

@author: serena-mo
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from DNA_L_M_code.encoder import Codeword_Strand
from DNA_L_M_code.decoder import Strand_Decode
from DNA_L_M_code.error_test import Error_Type



def test_nu_err_r(sub_pr,del_pr,ins_pr,msg_len,msg_block_num,test_num):
    """
    Test LM_code
    :param sub_pr: the probability of nucleotide substitution error
    :param del_pr: the probability of nucleotide deletion error
    :param ins_pr: the probability of nucleotide insertion error
    :param msg_len: the length of the message
    :param msg_block_num: the number of message blocks
    :param test_num: the number of tests to run
    :return: the nucleotide error rate after decoding
    """
    # Set the length of each message block
    msg_block_len = msg_len // msg_block_num

    # Generate a random quaternary string for encoding
    or_msg = np.random.randint(0, high=4, size=msg_len)

    # LM.encoder
    msg = np.copy(or_msg)
    LM_enc, LM_code_block_length = Codeword_Strand(msg, msg_block_len).encode()

    # Nucleotide error rate statistics
    LM_nu_err_times = 0
    for test_t in range(test_num):
        # Set errors
        LM_error_seq, LM_error_list = Error_Type(LM_enc,sub_pr, ins_pr, del_pr).random_error()

        # LM.decoder
        LM_dec = Strand_Decode(LM_error_seq, msg_block_len, msg_block_num).decode()

        for i in range(msg_len):
            if not np.array_equal(LM_dec[i], or_msg[i]):
                LM_nu_err_times += 1

    # Calculate the nucleotide error rate
    nu_n = test_num * msg_len
    LM_nu_err_rate = LM_nu_err_times / nu_n


    return LM_nu_err_rate

pr = np.linspace(0.002, 0.02, 10, endpoint=True)
# pr = np.arange(0,0.001,0.0001,dtype='float64')


# r_msg = np.zeros(len(pr))
# r_cai = np.zeros(len(pr))
r_LM_block1 = np.zeros(len(pr))
r_LM_block2 = np.zeros(len(pr))
# r_LM_block3 = np.zeros(len(pr))
r_LM_block4 = np.zeros(len(pr))
r_LM_block5 = np.zeros(len(pr))
# r_msg_ = np.zeros(len(pr))
# r_cai = np.zeros(len(pr))
for i in tqdm(range(len(pr))):
    pr_test = pr[i]

    r_LM_block1[i] = test_nu_err_r(pr_test / 2, pr_test / 4, pr_test / 4, 180, 1, 3)
    r_LM_block2[i] = test_nu_err_r(pr_test / 2, pr_test / 4, pr_test / 4, 180, 3, 3)
    # r_LM_block3[i] = test_nu_err_r(pr_test/2,pr_test/4,pr_test/4,180,4,5000)
    r_LM_block4[i] = test_nu_err_r(pr_test / 2, pr_test / 4, pr_test / 4, 180, 6, 3)
    r_LM_block5[i] = test_nu_err_r(pr_test / 2, pr_test / 4, pr_test / 4, 180, 12, 3)


plt.figure(dpi=200)

plt.plot(pr, r_LM_block1, label='$l=1$', marker='o', color='chocolate', linewidth=1, markevery=1, markersize=3)
plt.plot(pr, r_LM_block2, label='$l=3$', marker='*', color='slategrey', markevery=1, linewidth=1, markersize=3)
# plt.plot(pr,r_LM_block3,label='$l=4$',marker='s',color='olivedrab',linewidth=1, markevery=1,markersize=3)
plt.plot(pr, r_LM_block4, label='$l=6$', marker='>', color='palevioletred', linewidth=1, markevery=1, markersize=3)
plt.plot(pr, r_LM_block5, label='$l=12$', marker='d', color='cadetblue', markevery=1, linewidth=1, markersize=3)

# plt.plot(pr,r_msg,label='non-encoding',marker='p',color ='k',markevery=10)
# plt.plot(pr,r_cai,label ='Cai',color='c')
plt.yscale("log")
plt.xlabel("DNA IDS error rate, $pr$ (%)", fontsize=10)
set_xticks = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
plt.xticks(pr, set_xticks, fontsize=8, rotation=0)
plt.ylabel("Bit error rate", fontsize=10)
# plt.subplots_adjust(bottom = 0.2)
plt.legend(fontsize=8, markerscale=1, scatterpoints=1)

# plt.title("msg length:200, test:1000")
plt.show()