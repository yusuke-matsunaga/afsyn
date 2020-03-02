#! /usr/bin/env python3

### @file binder.py
### @brief バインディングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


from scheduling import scheduling

debug = False

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


### @brief セレクタの入力のバインディングを行う．
### @param[in] src_list_map cstep をキーにしてセレクタの入力のリストを入れる辞書
### @param[in] max_fanin セレクタの入力数
def input_binding(src_list_map, max_fanin) :
    # 各入力の担当するレジスタ番号のセット
    sel_src_set = [ set() for i in range(max_fanin) ]
    # cstep をキーにして個々のセレクタのソースを入れた辞書
    sel_src_list = [ dict() for i in range(max_fanin) ]
    last_i = -1
    for cstep, src_list in src_list_map.items() :
        used = set()
        for src in src_list :
            # すでに同じレジスタを持つ入力があったらそこに割り当てる．
            for i in range(max_fanin) :
                if src in sel_src_set[i] :
                    sel_src_list[i][cstep] = src
                    used.add(i)
                    if last_i < i :
                        last_i = i
                    break
            else :
                # 未使用の入力に割り当てる．
                for i in range(max_fanin) :
                    if i not in used :
                        sel_src_list[i][cstep] = src
                        used.add(i)
                        if last_i < i :
                            last_i = i
                        break

    return sel_src_list[:last_i + 1]


### @brief セレクタを生成する．
### @param[in] dfg 対象のDFG
### @param[in] reg_num レジスタ数
def alloc_selecter(dfg, reg_num) :
    reg_src_map = dict()
    total_num = 0

    # OP1 のファンインのセレクタ生成
    src_list_map_dict = dict()
    for node in dfg.op1node_list :
        src_list = list()
        for inode in node.fanin_list :
            var = inode.var
            reg_id = var.reg_id
            src_list.append(reg_id)
        op_id = node.op_id
        if op_id not in src_list_map_dict :
            src_list_map_dict[op_id] = dict()
        src_list_map_dict[op_id][node.cstep] = src_list

    for op_id in range(dfg.op1_num) :
        assert op_id in src_list_map_dict
        # cstep をキーにしたファンインのレジスタ番号のリストの辞書
        src_list_map = src_list_map_dict[op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_list_map, 16)
        n = 0
        for src_dict in sel_src_list :
            src_set = set()
            for src in src_dict.values() :
                src_set.add(src)
            n += len(src_set)
        total_num += n
        if debug :
            print('OP1#{}: # of inputs: {}'.format(op_id, n))
            for i, src_dict in enumerate(sel_src_list) :
                src_set = set()
                for src in src_dict.values() :
                    src_set.add(src)
                print('INPUT#{}'.format(i), end = '')
                for src in src_set :
                    print(' {}'.format(src), end = '')
                print()

    # OP2 のファンインのセレクタ生成
    src_list_map_dict = dict()
    for node in dfg.op2node_list :
        src_list = list()
        for inode in node.fanin_list :
            op1_id = inode.op_id
            src_list.append(op1_id)
        op_id = node.op_id
        if op_id not in src_list_map_dict :
            src_list_map_dict[op_id] = dict()
        src_list_map_dict[op_id][node.cstep] = src_list

    for op_id in range(dfg.op2_num) :
        assert op_id in src_list_map_dict
        # ファンインのOP1番号のリストのリスト
        src_list_map = src_list_map_dict[op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_list_map, 15)
        n = 0
        for src_dict in sel_src_list :
            src_set = set()
            for src in src_dict.values() :
                src_set.add(src)
            n += len(src_set)
        total_num += n
        if debug :
            print('OP2#{}: # of inputs: {}'.format(op_id, n))
            for i, src_dict in enumerate(sel_src_list) :
                src_set = set()
                for src in src_dict.values() :
                    src_set.add(src)
                print('INPUT#{}'.format(i), end = '')
                for src in src_set :
                    print(' {}'.format(src), end = '')
                print()

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

    print('Total inputs: {}'.format(total_num))


def bind(dfg) :
    # 演算器はとりあえずナイーブに割り当てる．
    op1_map = dict()
    op1_count = [ 0 for i in range(dfg.total_step) ]
    for node in dfg.op1node_list :
        step = node.cstep
        op_id = op1_count[step]
        node.bind(op_id)
        op1_count[step] += 1

    op2_map = dict()
    op2_count = [ 0 for i in range(dfg.total_step) ]
    for node in dfg.op2node_list :
        step = node.cstep
        op_id = op2_count[step]
        node.bind(op_id)
        op2_count[step] += 1

    # レジスタは単純なレフトエッジ法で割り当てる．
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

    mem_conf = ((24, 16), (24, 32), (12, 16), (12, 32), (6, 16), (6, 32))
    mem_conf = ((24, 32), )
    op1_conf = (16, 32, 64, 128)
    op1_conf = (128, )
    m_conf = (1, 2)
    s_conf = (1, 2, 3)
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
                    bind(dfg)
