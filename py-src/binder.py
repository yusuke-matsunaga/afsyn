#! /usr/bin/env python3

### @file binder.py
### @brief バインディングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


from scheduling import scheduling
from bipartite import bipartite_matching
from unit import UnitMgr

debug = False


def reg_bind1(dfg, unit_mgr, var_list) :
    # cur_var_list に含まれる変数にレジスタ割り当てを行う．
    # 各変数に関連付けられたノードとバインドしている演算器
    # が共通のレジスタを優先的に割り当てる．
    edge_list = list()
    for reg in unit_mgr.reg_list :
        for i, var in enumerate(var_list) :
            if reg.last_step > var.start :
                # life-time がオーバラップしている．
                continue
            if reg.has_samesrc(var.src) :
                w = 2
            else :
                w = 1
            edge_list.append( (reg.reg_id, i, w) )

    #print('matching begin: {}, {}, {}'.format(len(unit_mgr.reg_list), len(var_list), len(edge_list)))
    # 2部グラフの最大マッチングを求める．
    match = bipartite_matching(len(unit_mgr.reg_list), len(var_list), edge_list)
    #print('matching end. total {} matches'.format(len(match)))

    bound_vars = set()
    bound_regs = set()

    # マッチング結果に基づいて割り当てを行う．
    for reg_id, var_id in match :
        reg = unit_mgr.reg_list[reg_id]
        var = cur_var_list[var_id]
        reg.add_src(var.src)
        bound_vars.add(var_id)
        bound_regs.add(reg_id)

    # 残りの変数は適当に割り当てる．
    for i, var in enumerate(var_list) :
        if i in bound_vars :
            continue
        reg = unit_mgr.new_reg_unit()
        node = dfg.node_list[var.src_id]
        if node.is_memsrc :
            thr_unit = unit_mgr.new_through_unit(node.unit)
        else :
            thr_unit = None
        reg.add_src(node)


def reg_bind2(dfg, unit_mgr, var_list) :
    nvars = len(var_list)

    # cur_var_list に含まれる変数にレジスタ割り当てを行う．
    # 各変数に関連付けられたノードとバインドしている演算器
    # が共通のレジスタを優先的に割り当てる．
    edge_list = list()
    for i, var in enumerate(var_list) :
        for reg in unit_mgr.reg_list :
            if reg.last_step > var.start :
                # life-time がオーバラップしている．
                continue
            if reg.has_samesrc(var.src) :
                edge_list.append( (reg.reg_id, i, 1) )

    #print('matching begin: {}, {}, {}'.format(unit_mgr.reg_num, nvars, len(edge_list)))
    # 2部グラフの最大マッチングを求める．
    match = bipartite_matching(unit_mgr.reg_num, nvars, edge_list)
    #print('matching end. total {} matches'.format(len(match)))

    bound_vars = set()
    bound_regs = set()

    # マッチング結果に基づいて割り当てを行う．
    for reg_id, var_id in match :
        reg = unit_mgr.reg(reg_id)
        var = var_list[var_id]
        reg.add_src(var.src)
        bound_vars.add(var_id)
        bound_regs.add(reg_id)

    if len(bound_vars) == nvars :
        return

    # 残ったレジスタの割り当てを行う．
    edge_list = list();
    for i, var in enumerate(var_list) :
        if i in bound_vars :
            continue
        for reg in unit_mgr.reg_list :
            if reg.reg_id in bound_regs :
                continue
            if reg.last_step > var.start :
                # life-time がオーバラップしている．
                continue
            edge_list.append( (reg.reg_id, i, 1) )

    #print('matching begin: {}, {}, {}'.format(unit_mgr.reg_num, nvars, len(edge_list)))
    # 2部グラフの最大マッチングを求める．
    match = bipartite_matching(unit_mgr.reg_num, nvars, edge_list)
    #print('matching end. total {} matches'.format(len(match)))

    # マッチング結果に基づいて割り当てを行う．
    for reg_id, var_id in match :
        reg = unit_mgr.reg(reg_id)
        var = var_list[var_id]
        reg.add_src(var.src)
        bound_vars.add(var_id)
        bound_regs.add(reg_id)

    if len(bound_vars) == nvars :
        return

    # 残りの変数は適当に割り当てる．
    for i, var in enumerate(var_list) :
        if i in bound_vars :
            continue
        reg = unit_mgr.new_reg_unit()
        reg.add_src(var.src)


### @brief レジスタ割り当てを行う．
def bind_register(dfg, unit_mgr) :
    # 全変数のリストを (start, end) でソートしたもの
    # ただし MemNode が直接 OpNode につながっている場合
    # にはレジスタを使わない．
    var_list = list()
    for var in dfg.var_list :
        inode = var.src
        if inode.is_memsrc and var.start + 1 == var.end :
            var.bind(inode.unit)
        else :
            var_list.append(var)
    var_list.sort()

    # すべての変数に割り当てを行うまでループを繰り返す．
    while len(var_list) > 0 :
        # 最初の変数と line-time が重複している変数を取り出す．
        seed_var = var_list[0]
        seed_start = seed_var.start
        seed_end = seed_var.end
        cur_var_list = list()
        rest_var_list = list()
        for var in var_list :
            res = var.check_overlap(seed_start, seed_end)
            if res is not None :
                seed_start, seed_end = res
                cur_var_list.append(var)
            else :
                rest_var_list.append(var)
        var_list = rest_var_list

        #print()
        #print('cluster: {} | {} vars remain'.format(len(cur_var_list), len(var_list)))
        reg_bind2(dfg, unit_mgr, cur_var_list)


### @brief セレクタの入力のバインディングを行う．
### @param[in] src_set_dict cstep をキーにしてセレクタの入力のリストを入れる辞書
### @param[in] max_fanin セレクタの入力数
def input_binding(src_set_dict, max_fanin) :
    # 各入力の担当するレジスタ番号のセット
    sel_src_set = [ set() for i in range(max_fanin) ]
    # cstep をキーにして個々のセレクタのソースを入れた辞書
    sel_src_list = [ dict() for i in range(max_fanin) ]
    last_i = -1
    for cstep, src_list in src_set_dict.items() :
        used = set()
        bound_src_list = [ (None, False) for i in range(max_fanin) ]
        dup_list = list()
        for src, w in src_list :
            assert w == -0.25 or -0.125 or 0.125 or 0.25
            inv = True if w < 0 else False
            if w == 0.25 or w == -0.25 :
                dup_list.append( (src, inv) )
            # すでに同じレジスタを持つ入力があったらそこに割り当てる．
            for i in range(max_fanin) :
                if src in sel_src_set[i] :
                    bound_src_list[i] = src, inv
                    used.add(i)
                    if last_i < i :
                        last_i = i
                    break
            else :
                # 未使用の入力に割り当てる．
                for i in range(max_fanin) :
                    if i not in used :
                        bound_src_list[i] = src, inv
                        used.add(i)
                        if last_i < i :
                            last_i = i
                        break
                else :
                    print('max_fanin = {}'.format(max_fanin))
                    for i, (src, w) in enumerate(src_list) :
                        print('#{}  {}:{}'.format(i, src.name, w))
                    assert False
        for src, inv in dup_list :
            for i in range(max_fanin) :
                if i not in used :
                    bound_src_list[i] = src, inv
                    used.add(i)
                    if last_i < i :
                        last_i = i
                    break
            else :
                assert False

        # bound_src_list の内容を sel_src_list に移す．
        for i, (src, inv) in enumerate(bound_src_list) :
            sel_src_list[i][cstep] = src, inv
    return sel_src_list[:last_i + 1]


### @brief OP1の入力のセレクタを生成する．
### @param[in] dfg 対象のDFG
def alloc_op1_selecter(dfg, unit_mgr) :

    # 演算器毎に cstep をキーにしてソースのセットを記録する．
    src_set_list = [ dict() for i in range(unit_mgr.op1_num) ]
    for node in dfg.op1node_list :
        src_list = list()
        for i, inode in enumerate(node.fanin_list) :
            if inode.cstep + 1 == node.cstep and inode.is_memsrc :
                unit = inode.unit
            else :
                var = inode.var
                unit = var.unit
            w = node.weight(i)
            src_list.append( (unit, w) )
        op = node.unit
        src_set = src_set_list[op.op_id]
        assert node.cstep not in src_set
        src_set[node.cstep] = src_list

    for op in unit_mgr.op1_list :
        # cstep をキーにしたファンインのレジスタ番号のリストの辞書
        src_set_dict = src_set_list[op.op_id]
        # 入力のバインディングを行う．
        sel_src_dict = input_binding(src_set_dict, dfg.op1_limit)
        n = len(sel_src_dict)
        for i, sel_src in enumerate(sel_src_dict) :
            for cstep, (src, inv) in sel_src.items() :
                op.add_src(i, src, cstep, inv)

        if debug :
            print('OP1#{}: # of inputs: {}'.format(op.id, n))
            for i, src_dict in enumerate(sel_src_list) :
                src_set = set()
                for src, inv in src_dict.values() :
                    src_set.add(src)
                print('INPUT#{}'.format(i), end = '')
                for src in src_set :
                    print(' {}'.format(src), end = '')
                print()


### @brief OP2の入力のセレクタを生成する．
### @param[in] dfg 対象のDFG
def alloc_op2_selecter(dfg, unit_mgr) :

    # 演算器毎に cstep をキーにしてソースとバイアスの
    # セットを記録する．
    src_set_list = [ dict() for i in range(unit_mgr.op2_num) ]
    bias_set_list = [ dict() for i in range(unit_mgr.op2_num) ]
    for node in dfg.op2node_list :
        src_list = list()
        for inode in node.fanin_list :
            var = inode.var
            unit = var.unit
            assert not unit.is_store_unit
            src_list.append( (unit, 1) )
        op = node.unit
        src_set = src_set_list[op.op_id]
        assert node.cstep not in src_set
        src_set[node.cstep] = src_list
        bias_set = bias_set_list[op.op_id]
        bias_set[node.cstep] = node.bias

    # 演算器毎にセレクタの入力数が少なくなるように入力の並び替えをする．
    for op in unit_mgr.op2_list :
        src_set = src_set_list[op.op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_set, dfg.op2_limit)
        n = len(sel_src_list)
        assert n <= dfg.op2_limit
        for i, sel_src in enumerate(sel_src_list) :
            for cstep, (src, inv) in sel_src.items() :
                op.add_src(i, src, cstep)
        for cstep, bias in bias_set_list[op.op_id].items() :
            op.add_bias(bias, cstep)

        if debug :
            print('OP2#{}: # of inputs: {}'.format(op.id, n))
            for i, src_dict in enumerate(sel_src_list) :
                src_set = set()
                for src in src_dict.values() :
                    src_set.add(src)
                print('INPUT#{}'.format(i), end = '')
                for src in src_set :
                    print(' {}'.format(src), end = '')
                print()


### @brief バインディングを行う．
def bind(dfg) :
    unit_mgr = UnitMgr(dfg.imem_layout, dfg.omem_layout, dfg.total_step)

    # Load Unit は一意に割り当てられる．
    for node in dfg.memsrcnode_list :
        lu = unit_mgr.new_load_unit(node.block_id, node.offset)
        node.bind(lu)
        lu.add_cond(node.cstep, node.bank_id)

    # 演算器はとりあえずナイーブに割り当てる．
    op1_count = [ 0 for i in range(dfg.total_step) ]
    for node in dfg.op1node_list :
        step = node.cstep
        pos = op1_count[step]
        while unit_mgr.op1_num <= pos :
            unit_mgr.new_op1_unit(dfg.op1_limit)
        op = unit_mgr.op1(pos)
        node.bind(op)
        op.bind(node, step)
        op1_count[step] += 1

    op2_count = [ 0 for i in range(dfg.total_step) ]
    for node in dfg.op2node_list :
        step = node.cstep
        pos = op2_count[step]
        while unit_mgr.op2_num <= pos :
            unit_mgr.new_op2_unit(dfg.op2_limit)
        op = unit_mgr.op2(pos)
        node.bind(op)
        op.bind(node, step)
        op2_count[step] += 1

    # レジスタ割り当てを行う．
    bind_register(dfg, unit_mgr)

    # Store Unit も一意に割り当てられる．
    for node in dfg.memsinknode_list :
        su = unit_mgr.new_store_unit(node.block_id)
        node.bind(su)
        inode = node.src
        var = inode.var
        src = var.unit
        if src.is_reg_unit :
            src = unit_mgr.new_through_unit(src)
        su.add_src(src, node.cstep, node.bank_id)

    # セレクタの生成を行う．
    alloc_op1_selecter(dfg, unit_mgr)

    alloc_op2_selecter(dfg, unit_mgr)

    return unit_mgr


if __name__ == '__main__' :
    import sys
    import os
    from op import Op
    from dfg import make_graph
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

    mem_size = 0
    for op in op_list :
        for i_id, w in op.fanin_list :
            if mem_size < i_id :
                mem_size = i_id
    mem_size += 1

    mem_conf = ((24, 16), (24, 32), (12, 16), (12, 32), (6, 16), (6, 32))
    mem_conf = ((24, 32), )
    op1_conf = (16, 32, 64, 128)
    op1_conf = (64, )
    m_conf = (1, 2)
    s_conf = (1, 2, 3)
    s_conf = (2,)

    op1_limit = 16
    op2_limit = 15
    omemory_size = len(op_list)
    oblock_num = 8
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, obank_size)

    for block_num, bank_size in mem_conf :
        print()
        print('Block Num: {}'.format(block_num))
        print('Bank Size: {}'.format(bank_size))
        for m_method in m_conf :
            mem_layout = MemLayout(mem_size, block_num, bank_size, m_method)
            print()
            print('Memory model #{}'.format(m_method))
            dfg = make_graph(op_list, op1_limit, op2_limit, mem_layout, omem_layout)
            for op_limit in op1_conf :
                for s_method in s_conf :
                    dfg = scheduling(dfg, s_method)
                    print('{}, {}, {}: {} steps'.format(dfg.op1_num, dfg.op2_num, dfg.reg_num, dfg.total_step))
                    unit_mgr = bind(dfg)
