#! /usr/bin/env python3

### @file analyze.py
### @brief
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.

import openpyxl as px
import random
import sys
import os

from op import Op, read_op

def naive_scheduling(op_list, limit) :
    cur_size = 0
    cur_step = 0
    for op in op_list :
        if cur_size + op.block_size < limit :
            cur_size += op.block_size
        else :
            cur_step += 1
            cur_size = op.block_size
    return cur_step + 1


def random_scheduling(op_list, limit) :
    return naive_scheduling(random.sample(op_list, len(op_list)), limit)


def monte_carlo_scheduling(op_list, limit, num) :
    best_step = naive_scheduling(op_list, limit)
    for i in range(num) :
        cur_step = random_scheduling(op_list, limit)
        if best_step > cur_step :
            best_step = cur_step
    return best_step


if __name__ == '__main__' :
    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    with open(filename, 'rt') as fin :
        op_list = read_op(fin)

        num = 100000
        for limit in (32, 64, 128, 256) :
            ans1 = naive_scheduling(op_list, limit)
            ans2 = monte_carlo_scheduling(op_list, limit, num)
            print('limit = {}, naive = {}, monte_carlo = {}'.format(limit, ans1, ans2))
