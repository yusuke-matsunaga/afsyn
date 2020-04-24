#! /usr/bin/env python3

### @file randgen.py
### @brief
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

import random

imem_size = 1500
block_num = 12
bank_size = 32
bank_num = 4
block_size = bank_size * bank_num
num = 10

slice_size = block_num * bank_size
imem_size1 = ((imem_size + slice_size - 1) // slice_size) * slice_size

for i in range(num) :
    ivals = [ random.randrange(0, 256) for j in range(imem_size1) ]
    for block in range(block_num) :
        filename = 'imem{:02d}_{}.hex'.format(block, i)
        with open(filename, 'wt') as fout :
            for bank in range(bank_num) :
                offset = block_size * block + bank_size * bank
                for j in range(bank_size) :
                    fout.write('{:02x}'.format(ivals[offset + (bank_size - j - 1)]))
                fout.write('\n')
