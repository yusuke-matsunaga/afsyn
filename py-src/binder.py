#! /usr/bin/env python3

### @file binder.py
### @brief バインディングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


from scheduling import scheduling
from bipartite import bipartite_matching

debug = False


### @brief life-time がオーバーラップしているか調べる．
def is_overlap(start1, end1, start2, end2) :
    # 順序を正規化する．
    if start1 > start2 :
        start1, start2 = start2, start1
        end1, end2 = end2, end1

    if start2 < end1 :
        if end1 < end2 :
            return start2, end1
        else :
            return start2, end2
    else :
        return None


def is_compatible(node1, node2) :
    if node1.is_mem :
        if node2.is_mem :
            if node1.block_id == node2.block_id and node1.offset == node2.offset :
                return True
        return False
    elif node1.is_op1 :
        if node2.is_op1 :
            if node1.op_id == node2.op_id :
                return True
            return False
        return False
    return False


### @brief レジスタ割り当てを行う．
def bind_register(dfg) :
    # 全変数のリスト
    var_list = list(dfg.var_list)
    # start, end でソートする．
    var_list.sort()

    # 現在のレジスタ数
    reg_num = 0

    # 各レジスタに割り当てられた変数のリストを持つ配列
    # サイズは reg_num
    varmap_list = list()

    # すべての変数に割り当てを行うまでループを繰り返す．
    while len(var_list) > 0 :
        # 最初の変数と line-time が重複している変数を取り出す．
        seed_var = var_list[0]
        seed_start = seed_var.start
        seed_end = seed_var.end
        cur_var_list = list()
        for var in var_list :
            res = is_overlap(seed_start, seed_end, var.start, var.end)
            if res :
                seed_start, seed_end = res
                cur_var_list.append(var)
            elif seed_end < var.start :
                # これ以降は絶対にオーバーラップしない．
                break

        # cur_var_list の変数に関連付けられたノードのリスト
        cur_node_list = [ dfg.node_list[var.src_id] for var in cur_var_list ]
        n2 = len(cur_node_list)

        # cur_var_list に含まれる変数にレジスタ割り当てを行う．
        # 各変数に関連付けられたノードとバインドしている演算器
        # が共通のレジスタを優先的に割り当てる．
        edge_list = list()
        for reg_id in range(reg_num) :
            node_list1 = [ dfg.node_list[var.src_id] for var in varmap_list[reg_id] ]
            for i, node in enumerate(cur_node_list) :
                for node1 in node_list1 :
                    if is_compatible(node, node1) :
                        edge_list.append( (reg_id, i) )
                        break

        # 2部グラフの最大マッチングを求める．
        match = bipartite_matching(reg_num, n2, edge_list)

        bound_vars = set()
        bound_regs = set()

        # マッチング結果に基づいて割り当てを行う．
        for reg_id, var_id in match :
            var = cur_var_list[var_id]
            var.bind(reg_id)
            varmap_list[reg_id].append(var)
            bound_vars.add(var_id)
            bound_regs.add(reg_id)

        # 残りの変数は適当に割り当てる．
        for i, var in enumerate(cur_var_list) :
            if i in bound_vars :
                continue
            # 未割り当てのレジスタを見つける．
            for reg_id in range(reg_num) :
                if reg_id in bound_regs :
                    continue
                # 空きを見つけた．
                var.bind(reg_id)
                varmap_list[reg_id].append(var)
                bound_regs.add(reg_id)
                break
            else :
                # 未割り当てレジスタを見つけられなかった．
                reg_id = reg_num
                reg_num += 1
                varmap_list.append(list())
                var.bind(reg_id)
                varmap_list[reg_id].append(var)
                bound_regs.add(reg_id)

        return reg_num


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

    # レジスタ割り当てを行う．
    reg_num = bind_register(dfg)

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
