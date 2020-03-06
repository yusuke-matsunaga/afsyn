#! /usr/bin/env python3

### @file synthesizer.py
### @brief 回路を生成するプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

from scheduling import scheduling
from binder import bind



if __name__ == '__main__' :
    import sys
    import os
    from op import Op, read_op
    from dfg import make_graph
    from mem_layout import MemLayout

    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    op_list = None
    with open(filename, 'rt') as fin :
        op_list = read_op(fin)

    if op_list is None :
        print('read failed.')
        exit(1)

    mem_size = 0
    for op in op_list :
        for i_id, w in op.fanin_list :
            if mem_size < i_id :
                mem_size = i_id
    mem_size += 1

    #mem_conf = ((24, 16), (24, 32), (12, 16), (12, 32), (6, 16), (6, 32))
    mem_conf = ((24, 32), )
    #op1_conf = (16, 32, 64, 128)
    op1_conf = (128, )
    #m_conf = (1, 2)
    m_conf = (2,)
    #s_conf = (1, 2, 3)
    s_conf = (2,)
    for block_num, bank_size in mem_conf :
        print()
        print('Block Num: {}'.format(block_num))
        print('Bank Size: {}'.format(bank_size))
        for m_method in m_conf :
            mem_layout = MemLayout(mem_size, block_num, bank_size, m_method)
            print()
            print('Memory model #{}'.format(m_method))
            for op_limit in op1_conf :
                for s_method in s_conf :
                    dfg = scheduling(op_list, op_limit, mem_layout, s_method)
                    op1_num, op2_num, reg_num, total_step = dfg.eval_resource()
                    print('{}, {}, {}: {} steps'.format(op1_num, op2_num, reg_num, total_step))
                    reg_list, op1_list, op2_list = bind(dfg)

                    for reg_spec in reg_list :
                        print('REG#{}:'.format(reg_spec.id))
                        for cstep, src in reg_spec.src_map().items() :
                            if isinstance(src, int) :
                                print('  REG#{}@{}'.format(src, cstep))
                            else :
                                print('  MEM{}@{}'.format(src, cstep))
                        print()

                    for op_id, op1_spec in enumerate(op1_list) :
                        print('OP1#{}:'.format(op_id))
                        for i in range(op1_spec.input_num) :
                            mux = op1_spec.mux_spec(i)
                            print('  I#{}:'.format(i))
                            for cstep, (src_id, inv) in mux.src_dict.items() :
                                if src_id == -1 :
                                    print('     C0@{}'.format(cstep))
                                else :
                                    minus = '-' if inv else ' '
                                    print('    {}REG#{}@{}'.format(minus, src_id, cstep))
                            print()
                        print()

                    for op_id, op2_spec in enumerate(op2_list) :
                        print('OP2#{}:'.format(op_id))
                        for i in range(op2_spec.input_num) :
                            mux = op2_spec.mux_spec(i)
                            print('  I#{}:'.format(i))
                            for cstep, (src_id, inv) in mux.src_dict.items() :
                                if src_id == -1 :
                                    print('    C0@{}'.format(cstep))
                                else :
                                    print('    REG#{}@{}'.format(src_id, cstep))
                            print()
                        print('  BIAS')
                        for cstep, bias in op2_spec.bias_map().items() :
                            print('    {}@{}'.format(bias, cstep))
                        print()
