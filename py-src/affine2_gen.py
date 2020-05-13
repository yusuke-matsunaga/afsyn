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
    from afsyn.codegen2 import CodeGen2

    filename = '../data/Affine_2_W.op'
    with open(filename, 'rt') as fin :
        op_list = Op.read(fin)
        if op_list is None :
            print('read failed.')
            exit(1)

    op1_limit = 32
    op2_limit = 31

    # 入力メモリの仕様
    imemory_size = 1000;
    iblock_num = 8
    iblock_size = 125
    ibank_size = 32
    imem_layout = MemLayout(imemory_size, iblock_num, iblock_size, ibank_size)

    # 出力メモリの仕様
    omemory_size = 298
    oblock_num = 5
    oblock_size = 60
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, oblock_size, obank_size)

    dfg = make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout)

    op_limit = 16
    s_method = 2
    dfg = scheduling(dfg, op_limit, s_method)
    #dfg.print()
    #print('{}, {}, {}: {} steps'.format(dfg.op1_num, dfg.op2_num, dfg.reg_num, dfg.total_step))
    unit_mgr = bind(dfg)
    #unit_mgr.print(sys.stdout)

    codegen = CodeGen2(sys.stdout)
    module_name = 'affine2'
    op1_module_name = 'affine2_op1'
    op2_module_name = 'affine2_op2'
    codegen.generate(unit_mgr, module_name, op1_module_name, op2_module_name)
