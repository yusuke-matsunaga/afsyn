#! /usr/bin/env python3

### @file make_graph.py
### @brief DFG を作る関数
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


#from afsyn.unit import Unit
from afsyn.dfg import DFG

### @brief DFG を作る
### @param[in] op_list 演算リスト
### @param[in] op1_limit OP1のファンイン数
### @param[in] op2_limit OP2のファンイン数
### @param[in] imem_layout 入力メモリレイアウト
### @param[in] omem_layout 出力メモリレイアウト
### @return DFG を返す．
def make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout) :
    dfg = DFG(op1_limit, op2_limit, imem_layout, omem_layout)
    for o_id, op in enumerate(op_list) :
        l1_fanin_list = []
        l1_fanin_num = 0
        l1_weight_list = []
        l2_fanin_list = []

        assert len(op.fanin_list) <= op1_limit * op2_limit

        for i_id, w in op.fanin_list :
            mem_node = dfg.make_memsrc(i_id)
            if w == 0.375 or w == -0.375 :
                n = 3
            elif w == 0.25 or w == -0.25 :
                n = 2
            elif w == 0.125 or w == -0.125 :
                n = 1
            else :
                print('Unexpected weight value {}'.format(w))
                exit(-1)
            if l1_fanin_num + n >= op1_limit :
                op_node = dfg.make_op1(l1_fanin_list, l1_weight_list)
                l2_fanin_list.append(op_node)
                l1_fanin_list = []
                l1_fanin_num = 0
                l1_weight_list = []
            l1_fanin_list.append(mem_node)
            l1_weight_list.append(w)
            l1_fanin_num += n

        if l1_fanin_num > 0 :
            op_node = dfg.make_op1(l1_fanin_list, l1_weight_list)
            l2_fanin_list.append(op_node)

        if len(l2_fanin_list) > op2_limit :
            print('l2_fanin_list: {}'.format(len(l2_fanin_list)))
            print('op2_limit: {}'.format(op2_limit))
            print('op.fanin_list: {}'.format(len(op.fanin_list)))
            for op1 in l2_fanin_list :
                print(' op1.fanin_list: {}'.format(op1.fanin_num))
            print()
        assert len(l2_fanin_list) <= op2_limit
        node = dfg.make_op2(l2_fanin_list)
        for inode in l2_fanin_list :
            inode.set_fanout(node)
        onode = dfg.make_memsink(o_id, node)
        node.set_fanout(onode)

    return dfg


if __name__ == '__main__' :
    # テストプログラム
    # Op.dump() ファイルを読み込んで DFG を作る．
    import sys
    import os
    from op import Op
    from mem_layout import MemLayout

    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    op_list = None
    with open(filename, 'rt') as fin :
        op_list = Op.read(fin)

    if op_list is None :
        print('read failed.')
        exit(1)

    memory_size = 1500
    #block_num = 24
    block_num = 12
    bank_size = 32
    print('Block num: {}'.format(block_num))
    print('Bank Size: {}'.format(bank_size))
    imem_layout = MemLayout(memory_size, block_num, bank_size)
    omemory_size = len(op_list)
    oblock_num = 8
    obank_size = 1
    op1_limit = 32
    op2_limit = 31
    omem_layout = MemLayout(omemory_size, oblock_num, obank_size)
    dfg = make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout)
    print('# of nodes: {}'.format(dfg.node_num))
    print('# of OP1 nodes: {}'.format(dfg.op1node_num))
    print('# of OP2 nodes: {}'.format(dfg.op2node_num))
    print('# of MemSink:   {}'.format(dfg.memsinknode_num))

    for node in dfg.memsrcnode_list :
        print('[MEMSRC] #{}: {}-{}-{}'.format(node.id, node.block_id, node.bank_id, node.offset))

    for node in dfg.memsinknode_list :
        print('[MEMSINK] #{}: {}-{}-{}'.format(node.id, node.block_id, node.bank_id, node.offset))
