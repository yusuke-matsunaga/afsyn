#! /usr/bin/env python3

### @file binder.py
### @brief バインディングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


from scheduling import scheduling

def left_edge(dfg) :
    var_list = dfg.var_list
    # start, end でソートする．
    var_list.sort()

    reg_id = 0
    while len(var_list) > 0 :
        new_var_list = list()
        last = 0
        for var in var_list :
            if last <= var.start :
                var.bind(reg_id)
                last = var.end
            else :
                new_var_list.append(var)
        reg_id += 1
        var_list = new_var_list

    return reg_id

def bipartite_matchin(left_group_list, right_list) :


def input_binding(src_list_list, max_fanin) :
    sel_src_list = [ [] for i in range(max_fanin) ]
    for src_list in src_list_list :
        sel_src_list = bipartite_matching(sel_src_list, src_list)
    return sel_src_list


def alloc_selecter(dfg, reg_num) :
    reg_src_map = dict()
    total_num = 0

    # OP1 のファンインのセレクタ生成
    src_list_map = dict()
    for node in dfg.op1node_list :
        src_list = list()
        for inode in node.fanin_list :
            var = inode.var
            reg_id = var.reg_id
            src_list.append(reg_id)
        op_id = node.op_id
        if op_id not in src_list_map :
            src_list_map[op_id] = list()
        src_list_map[op_id].append(src_list)
        var = node.var
        reg_id = var.reg_id
        if reg_id not in reg_src_map :
            reg_src_map[reg_id] = list()
        reg_src_map[reg_id].append(op_id)

    for op_id in range(dfg.op1_num) :
        assert op_id in src_list_map
        # ファンインのレジスタ番号のリストのリスト
        src_list_list = src_list_map[op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_list_list, 16)
        n = 0
        for src_list in sel_src_list :
            n += len(src_list)
        print('# of inputs: {}'.format(n))
        total_num += n

    # OP2 のファンインのセレクタ生成
    src_list_map = dict()
    for node in dfg.op2node_list :
        src_list = list()
        for inode in node.fanin_list :
            var = inode.var
            reg_id = var.reg_id
            src_list.append(reg_id)
        op_id = node.op_id
        if op_id not in src_list_map :
            src_list_map[op_id] = list()
        src_list_map[op_id].append(src_list)
        var = node.var
        reg_id = var.reg_id
        if reg_id not in reg_src_map :
            reg_src_map[reg_id] = list()
        reg_src_map[reg_id].append(op_id)

    for op_id in range(dfg.op2_num) :
        assert op_id in src_list_map
        # ファンインのレジスタ番号のリストのリスト
        src_list_list = src_list_map[op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_list_list, 15)
        n = 0
        for src_list in sel_src_list :
            n += len(src_list)
        print('# of inputs: {}'.format(n))
        total_num += n

    var_set = set()
    for node in dfg.memnode_list :
        var = node.var
        if var in var_set :
            # 処理済み
            continue
        var_set.add(var)
        reg_id = var.reg_id
        if reg_id not in reg_src_map :
            reg_src_map[reg_id] = list()
        reg_src_map[reg_id].append(node)

    # レジスタの入力のセレクタ生成
    for reg_id in range(reg_num) :
        assert reg_id in reg_src_map
        src_list = reg_src_map[reg_id]
        # src_list の要素数がセレクタの入力数となる．
        total_num += len(src_list)

    print('Total inputs: {}'.format(total_num))


def bind(dfg) :
    op1_num, op2_num, reg_num, total_step = dfg.eval_resource()

    # 演算器はとりあえずナイーブに割り当てる．
    op1_map = dict()
    op1_count = [ 0 for i in range(total_step) ]
    for node in dfg.op1node_list :
        step = node.cstep
        op_id = op1_count[step]
        node.bind(op_id)
        op1_count[step] += 1

    op2_map = dict()
    op2_count = [ 0 for i in range(total_step) ]
    for node in dfg.op2node_list :
        step = node.cstep
        op_id = op2_count[step]
        node.bind(op_id)
        op2_count[step] += 1

    # 単純なレフトエッジ法で割り当てる．
    reg_num = left_edge(dfg)

    # セレクタの生成を行う．
    alloc_selecter(dfg, reg_num)


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

    for block_num, bank_size in ((24, 16), (24, 32), (12, 16), (12, 32), (6, 16), (6, 32)) :
        print()
        print('Block Num: {}'.format(block_num))
        print('Bank Size: {}'.format(bank_size))
        for m_method in (1, 2) :
            mem_layout = MemLayout(mem_size, block_num, bank_size, m_method)
            print()
            print('Memory model #{}'.format(m_method))
            for op_limit in (16, 32, 64, 128) :
                for s_method in (1, 2) :
                    dfg = scheduling(op_list, op_limit, mem_layout, s_method)
                    op1_num, op2_num, reg_num, total_step = dfg.eval_resource()
                    print('{}, {}, {}: {} steps'.format(op1_num, op2_num, reg_num, total_step))
                    bind(dfg)
