#! /usr/bin/env python3

### @file rand_sim.py
### @brief ランダムシミュレーションを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


if __name__ == '__main__' :
    import sys
    import os
    import random
    import argparse
    from op import Op
    from dfg import make_graph
    from mem_layout import MemLayout

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type = int, default = 1000)
    parser.add_argument('file', type = argparse.FileType('rt'))

    args = parser.parse_args()
    if not args :
        exit(1)

    op_list = Op.read(args.file)
    if op_list is None :
        print('read failed.')
        exit(1)

    # メモリサイズの計算
    mem_size = 0
    for op in op_list :
        for i_id, w in op.fanin_list :
            if mem_size < i_id :
                mem_size = i_id
    mem_size += 1

    #block_num = 24
    block_num = 12
    bank_size = 32
    print('Block num: {}'.format(block_num))
    print('Bank Size: {}'.format(bank_size))
    imem_layout = MemLayout(mem_size, block_num, bank_size)
    omemory_size = len(op_list)
    oblock_num = 8
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, obank_size)
    dfg = make_graph(op_list, imem_layout, omem_layout)

    for c in range(args.count) :
        ivals = [ random.randrange(-128, 128) for j in range(mem_size) ]
        ovals = [ op.eval(ivals) for op in op_list ]
        ovals2 = dfg.simulate(ivals)
        for i, val in enumerate(ovals) :
            val2 = ovals2[i]
            print('O#{}: {}'.format(i, val))
            if val2 != val :
                print('Error')
