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
    from dfg import make_graph
    from scheduling import scheduling
    from mem_layout import MemLayout
    from binder import bind

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type = int, default = 1000)
    parser.add_argument('--test-vector', action = "store_true")
    parser.add_argument('-d', '--debug', action = "store_true")

    args = parser.parse_args()
    if not args :
        exit(1)

    # デバッグフラグ
    debug = args.debug

    filename = '../data/Affine_W.op'
    with open(filename, 'rt') as fin :
        op_list = Op.read(fin)
        if op_list is None :
            print('read failed.')
            exit(1)

    # 入力の仕様
    imemory_size = 1536
    block_num = 12
    block_size = 128
    bank_size = 32
    imem_layout = MemLayout(imemory_size, block_num, block_size, bank_size)

    # 出力の仕様
    omemory_size = 1000
    oblock_num = 8
    oblock_size = 125
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, oblock_size, obank_size)
    oaddr_list = [ i for i in range(omemory_size) ]

    # OP1 の入力数
    op1_limit = 16

    # OP2 の入力数
    op2_limit = 15

    # DFG を作る．
    dfg = make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout)

    # OP1 の個数制約
    op_limit = 16

    # スケジューリングを行う．
    s_method = 2
    dfg = scheduling(dfg, op_limit, s_method)
    dfg.print()

    # バインディングを行う．
    unit_mgr = bind(dfg)
    unit_mgr.print(sys.stdout)

    random.seed(1234)

    debug_dfg = debug
    debug_rtl = debug
    for c in range(args.count) :
        # 入力値をランダムに生成する．
        ivals = { i: random.randrange(-128, 128) for i in range(imemory_size) }
        # 出力値の参考値を求める．
        ovals1 = [ op.eval(ivals) for op in op_list ]
        # DFG のレベルで値を求める．
        ovals2 = dfg.simulate(ivals, debug_dfg)
        # RTL のレベルで値を求める．
        ovals3 = unit_mgr.simulate(ivals, oaddr_list, debug_rtl)

        # 値を比較する．
        for i in range(omemory_size) :
            val1 = ovals1[i]
            val2 = ovals2[i]
            val3 = ovals3[i]
            error = 0
            if val2 != val1 :
                error |= 1
            if val3 != int(math.floor(val1)) :
                error |= 2
            if error :
                print('Error at O[{}]:'.format(i))
                print('  expected value = {}'.format(val1))
                if error & 1 :
                    print('  DFG value = {}'.format(val2))
                if error & 2 :
                    print('  RTL value = {}'.format(val3))

        if args.test_vector :
            # 入力メモリの内容をダンプする．
            for block in range(imem_layout.block_num) :
                if args.count > 1 :
                    filename = 'imem{:02d}_{}.hex'.format(block, c)
                else :
                    filename = 'imem{:02d}.hex'.format(block)
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
                if args.count > 1 :
                    filename = 'omem{:0d}_{}.hex'.format(block, c)
                else :
                    filename = 'omem{:0d}.hex'.format(block)
                with open(filename, 'wt') as fout :
                    for bank in range(omem_layout.bank_num) :
                        addr = omem_layout.encode(block, bank, 0)
                        if addr < len(op_list) :
                            val = ovals3[addr]
                        else :
                            val = 0
                        uval = (val + 256) % 256
                        fout.write('{:02x}\n'.format(uval))
