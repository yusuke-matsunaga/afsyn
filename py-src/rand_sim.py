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
    import math
    import random
    import argparse
    from op import Op
    from scheduling import scheduling
    from mem_layout import MemLayout
    from binder import bind

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type = int, default = 1000)
    parser.add_argument('--test-vector', action = "store_true")
    parser.add_argument('-d', '--debug', action = "store_true")
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

    bsize = block_num * bank_size
    imemory_size = ((mem_size + bsize - 1) // bsize) * bsize
    imem_layout = MemLayout(imemory_size, block_num, bank_size)
    omemory_size = len(op_list)
    oblock_num = 8
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, obank_size)
    oaddr_list = [ i for i in range(omemory_size) ]

    op_limit = 16
    s_method = 2
    dfg = scheduling(op_list, op_limit, imem_layout, omem_layout, s_method)
    #dfg.print()
    unit_mgr = bind(dfg)
    #unit_mgr.print(sys.stdout)

    random.seed(1234)

    debug = args.debug
    for c in range(args.count) :
        ivals = dict()
        for i in range(mem_size) :
            ivals[i] = random.randrange(-128, 128)
        ovals = [ op.eval(ivals) for op in op_list ]
        ovals2 = dfg.simulate(ivals, False)
        ovals3 = unit_mgr.simulate(ivals, oaddr_list, debug)
        for i, val in enumerate(ovals) :
            val2 = ovals2[i]
            val3 = ovals3[i]
            error = 0
            if val2 != val :
                error |= 1
            if val3 != int(math.floor(val)) :
                error |= 2
            if error :
                print('Error at O[{}]:'.format(i))
                print('  expected value = {}'.format(val))
                if error & 1 :
                    print('  DFG value = {}'.format(val2))
                if error & 2 :
                    print('  RTL value = {}'.format(val3))

        if args.test_vector :
            # 入力メモリの内容をダンプする．
            for block in range(imem_layout.block_num) :
                filename = 'imem{:02d}_{}.hex'.format(block, c)
                with open(filename, 'wt') as fout :
                    for bank in range(imem_layout.bank_num) :
                        for offset in range(imem_layout.bank_size) :
                            addr = imem_layout.encode(block, bank, bank_size - offset - 1)
                            if addr in ivals :
                                val = ivals[addr]
                            else :
                                val = 0
                            # 8ビットの符号なし数に変換する．
                            uval = (val + 256) % 256
                            fout.write('{:02x}'.format(uval))
                        fout.write('\n')

            # 出力メモリの内容をダンプする．
            for block in range(omem_layout.block_num) :
                filename = 'omem{:0d}_{}.hex'.format(block, c)
                with open(filename, 'wt') as fout :
                    for bank in range(omem_layout.bank_num) :
                        addr = omem_layout.encode(block, bank, 0)
                        if addr < len(op_list) :
                            val = ovals3[addr]
                        else :
                            val = 0
                        uval = (val + 256) % 256
                        fout.write('{:02x}\n'.format(uval))
                        print('oval[{}|{}:{}] = {}'.format(addr, block, bank, uval))
