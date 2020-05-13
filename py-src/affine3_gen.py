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
    from afsyn.op import Op
    from afsyn.dfg import make_graph
    from afsyn.scheduling import scheduling
    from afsyn.mem_layout import MemLayout
    from afsyn.binder import bind
    from afsyn.codegen3 import CodeGen3

    filename = '../data/Affine_3_W.op'
    with open(filename, 'rt') as fin :
        op_list = Op.read(fin)
        if op_list is None :
            print('read failed.')
            exit(1)

    op1_limit = 16
    op2_limit = 15

    imemory_size = 298
    block_num = 5
    block_size = 60
    bank_size = 1
    imem_layout = MemLayout(imemory_size, block_num, block_size, bank_size)

    omemory_size = 1
    oblock_num = 1
    oblock_size = 1
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, oblock_size, obank_size)
    oaddr_list = [ i for i in range(omemory_size) ]

    dfg = make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout)

    op_limit = 8
    s_method = 2
    dfg = scheduling(dfg, op_limit, s_method)
    #dfg.print()
    unit_mgr = bind(dfg)
    #unit_mgr.print(sys.stdout)

    codegen = CodeGen3(sys.stdout)
    module_name = 'affine3'
    op1_module_name = 'affine3_op1'
    op2_module_name = 'affine3_op2'
    codegen.generate(unit_mgr, module_name, op1_module_name, op2_module_name)
