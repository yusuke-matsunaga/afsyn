#! /usr/bin/env python3

### @file codegen.py
### @brief Verilog-HDL 記述を出力するクラス
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

if __name__ == '__main__' :
    import sys
    import os
    import random
    import argparse
    from afsyn import Op
    from afsyn import make_graph
    from afsyn import scheduling
    from afsyn import MemLayout
    from afsyn import bind
    from afsyn import CodeGen

    filename = '../data/Affine_W.op'
    with open(filename, 'rt') as fin :
        op_list = Op.read(fin)
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

    imemory_size = 1500
    block_num = 12
    block_size = 128
    bank_size = 32
    imem_layout = MemLayout(imemory_size, block_num, block_size, bank_size)

    omemory_size = len(op_list)
    oblock_num = 8
    oblock_size = 125
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, oblock_size, obank_size)
    oaddr_list = [ i for i in range(omemory_size) ]

    op1_limit = 16
    op2_limit = 15

    dfg = make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout)

    op_limit = 16
    s_method = 2
    dfg = scheduling(dfg, op_limit, s_method)
    #dfg.print()
    unit_mgr = bind(dfg)
    #unit_mgr.print(sys.stdout)

    codegen = CodeGen(sys.stdout)
    module_name = 'affine'
    op1_module_name = 'affine_op1'
    op2_module_name = 'affine_op2'
    codegen.generate(unit_mgr, module_name, op1_module_name, op2_module_name)
