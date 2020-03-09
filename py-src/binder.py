#! /usr/bin/env python3

### @file binder.py
### @brief バインディングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


from scheduling import scheduling
from bipartite import bipartite_matching
from unit import LoadUnit, StoreUnit, Op1Unit, Op2Unit, RegUnit

debug = False


### @brief OP1の仕様を表すクラス
class Op1Spec :

    ### @brief 初期化
    ### @param[in] input_num 入力数
    def __init__(self, input_num) :
        self.__input_num = input_num
        self.__mux_spec = [ MuxSpec() for i in range(input_num) ]
        self.__inv_cond_list = [ list() for i in range(input_num) ]

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] cstep コントロールステップ
    ### @param[in] src_id ソースのレジスタ番号
    ### @param[in] inv 反転する時に True にするフラグ
    def add_src(self, i, cstep, src_id, inv) :
        self.__mux_spec[i].add_src(cstep, src_id)
        if inv :
            self.__inv_cond_list[i].append(cstep)

    ### @brief 入力のセレクタ情報を返す．
    ### @param[in] i 入力番号
    def mux_spec(self, i) :
        return self.__mux_spec[i]

    ### @brief 入力の反転条件(コントロールステップ)を返す．
    def inv_cond(self, i) :
        return self.__inv_cond_list[i]


### @brief OP2の仕様を表すクラス
class Op2Spec :

    ### @brief 初期化
    ### @param[in] input_num 入力数
    def __init__(self, input_num) :
        self.__input_num = input_num
        self.__mux_spec = [ MuxSpec() for i in range(input_num) ]
        self.__bias_map = dict()

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] cstep コントロールステップ
    ### @param[in] src_id ソースのレジスタ番号
    def add_src(self, i, cstep, src_id) :
        self.__mux_spec[i].add_src(cstep, src_id)

    ### @brief cstep ごとの bias 値を設定する．
    def add_bias(self, cstep, bias) :
        self.__bias_map[cstep] = bias

    ### @brief 入力のセレクタ情報を返す．
    ### @param[in] i 入力番号
    def mux_spec(self, i) :
        return self.__mux_spec[i]

    ### @brief bias値の辞書を返す．
    @property
    def bias_map(self) :
        return self.__bias_map


### @brief レジスタの仕様を表すクラス
class RegSpec :

    ### @brief 初期化
    ### @param[in] id レジスタ番号
    def __init__(self, id) :
        self.__id = id
        self.__memsrc_map = dict()
        self.__opsrc_map = dict()

    ### @brief レジスタ番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief ソースの情報を追加する(メモリブロック)．
    def add_memsrc(self, cstep, mem_block, mem_bank, mem_offset) :
        key = mem_block, mem_offset
        if key not in self.__memsrc_map :
            self.__memsrc_map[key] = list()
        self.__memsrc_map[key].append( (cstep, mem_bank) )

    ### @brief ソースの情報を追加する(演算器)
    def add_opsrc(self, cstep, op_id) :
        if op_id not in self.__opsrc_map :
            self.__opsrc_map[op_id] = list()
        self.__opsrc_map[op_id].append(cstep)

    ### @brief メモリブロックソースの辞書を返す．
    ###
    ### (mem_block, mem_offset) をキーとして，そのブロックを使う
    ### コントロールステップとオフセットのペアのリストを格納する．
    def memsrc_map(self) :
        return self.__memsrc_map

    ### @brief 演算器ブロックソースの辞書を返す．
    ###
    ### 演算器番号をキーとしてそのブロックを使う
    ### コントロールステップのリストを格納する．
    def opsrc_map(self) :
        return self.__opsrc_map


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

    # 各レジスタに割り当てられた変数のソースとなっている演算器番号のセットのリスト
    opsrc_list = list()
    # 各レジスタに割り当てられた変数のソースとなっているメモリブロックのセットのリスト
    memsrc_list = list()

    # すべての変数に割り当てを行うまでループを繰り返す．
    while len(var_list) > 0 :
        # 最初の変数と line-time が重複している変数を取り出す．
        seed_var = var_list[0]
        seed_start = seed_var.start
        seed_end = seed_var.end
        cur_var_list = list()
        new_var_list = list()
        for var in var_list :
            res = is_overlap(seed_start, seed_end, var.start, var.end)
            if res is not None :
                seed_start, seed_end = res
                cur_var_list.append(var)
            else :
                new_var_list.append(var)
        var_list = new_var_list

        # cur_var_list の変数に関連付けられたノードのリスト
        cur_node_list = [ dfg.node_list[var.src_id] for var in cur_var_list ]
        n2 = len(cur_node_list)

        # cur_var_list に含まれる変数にレジスタ割り当てを行う．
        # 各変数に関連付けられたノードとバインドしている演算器
        # が共通のレジスタを優先的に割り当てる．
        edge_list = list()
        for reg_id in range(reg_num) :
            opsrc = opsrc_list[reg_id]
            memsrc = memsrc_list[reg_id]
            for i, node in enumerate(cur_node_list) :
                compatible = False
                if node.is_mem :
                    if (node.block_id, node.offset) in memsrc :
                        compatible = True
                else :
                    if node.op_id in opsrc :
                        compatible = True
                if compatible :
                    edge_list.append( (reg_id, i) )

        # 2部グラフの最大マッチングを求める．
        match = bipartite_matching(reg_num, n2, edge_list)

        bound_vars = set()
        bound_regs = set()

        # マッチング結果に基づいて割り当てを行う．
        for reg_id, var_id in match :
            var = cur_var_list[var_id]
            var.bind(reg_id)
            varmap_list[reg_id].append(var)
            node = dfg.node_list[var.src_id]
            if node.is_mem :
                memsrc_list[reg_id].add( (node.block_id, node.offset) )
            else :
                opsrc_list[reg_id].add(node.op_id)
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
                node = dfg.node_list[var.src_id]
                if node.is_mem :
                    memsrc_list[reg_id].add( (node.block_id, node.offset) )
                else :
                    opsrc_list[reg_id].add(node.op_id)
                bound_regs.add(reg_id)
                break
            else :
                # 未割り当てレジスタを見つけられなかった．
                reg_id = reg_num
                reg_num += 1
                varmap_list.append(list())
                memsrc_list.append(set())
                opsrc_list.append(set())
                var.bind(reg_id)
                varmap_list[reg_id].append(var)
                node = dfg.node_list[var.src_id]
                if node.is_mem :
                    memsrc_list[reg_id].add( (node.block_id, node.offset) )
                else :
                    opsrc_list[reg_id].add(node.op_id)
                bound_regs.add(reg_id)

    # varmap_list から RegSpec の情報を作る．
    reg_spec_list = list()
    for reg_id, varmap in enumerate(varmap_list) :
        reg_spec = RegSpec(reg_id)
        for var in varmap :
            src_id = var.src_id
            cstep = var.start
            node = dfg.node_list[src_id]
            if node.is_mem :
                reg_spec.add_memsrc(cstep, node.block_id, node.bank_id, node.offset)
            else :
                reg_spec.add_opsrc(cstep, node.op_id)
        reg_spec_list.append(reg_spec)

    return reg_spec_list


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
        bound_src_list = [ (None, False) for i in range(max_fanin) ]
        dup_list = list()
        for src, w in src_list :
            inv = True if w == -0.125 else False
            if w == 0.25 :
                dup_list.append(src)
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
                    assert False
        for src in dup_list :
            for i in range(max_fanin) :
                if i not in used :
                    bound_src_list[i] = src, False
                    used.add(i)
                    if last_i < i :
                        last_i = i
                    break
            else :
                assert False
        # 未使用の入力ソースを -1 にしておく
        for i in range(max_fanin) :
            if i not in used :
                bound_src_list[i] = -1, False
        # bound_src_list の内容を sel_src_list に移す．
        for i, (src, inv) in enumerate(bound_src_list) :
            sel_src_list[i][cstep] = src, inv
    return sel_src_list[:last_i + 1]


### @brief セレクタを生成する．
### @param[in] dfg 対象のDFG
def alloc_selecter(dfg) :

    # OP1 のファンインのセレクタ生成
    src_list_map_dict = dict()
    for node in dfg.op1node_list :
        src_list = list()
        for i, inode in enumerate(node.fanin_list) :
            var = inode.var
            reg_id = var.reg_id
            w = node.weight_list[i]
            src_list.append( (reg_id, w) )
        op_id = node.op_id
        if op_id not in src_list_map_dict :
            src_list_map_dict[op_id] = dict()
        src_list_map_dict[op_id][node.cstep] = src_list

    op1_list = list()
    for op_id in range(dfg.op1_num) :
        assert op_id in src_list_map_dict
        # cstep をキーにしたファンインのレジスタ番号のリストの辞書
        src_list_map = src_list_map_dict[op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_list_map, 16)
        n = len(sel_src_list)
        op1_spec = Op1Spec(n)
        for i, sel_src in enumerate(sel_src_list) :
            for cstep, (src_id, inv) in sel_src.items() :
                op1_spec.add_src(i, cstep, src_id, inv)

        op1_list.append(op1_spec)

        if debug :
            print('OP1#{}: # of inputs: {}'.format(op_id, n))
            for i, src_dict in enumerate(sel_src_list) :
                src_set = set()
                for src, inv in src_dict.values() :
                    src_set.add(src)
                print('INPUT#{}'.format(i), end = '')
                for src in src_set :
                    print(' {}'.format(src), end = '')
                print()

    # OP2 のファンインのセレクタ生成
    src_list_map_dict = dict()
    bias_map_dict = dict()
    for node in dfg.op2node_list :
        src_list = list()
        for inode in node.fanin_list :
            op1_id = inode.op_id
            src_list.append( (op1_id, 1) )
        op_id = node.op_id
        if op_id not in src_list_map_dict :
            src_list_map_dict[op_id] = dict()
            bias_map_dict[op_id] = dict()
        src_list_map_dict[op_id][node.cstep] = src_list
        bias_map_dict[op_id][node.cstep] = node.bias

    op2_list = list()
    for op_id in range(dfg.op2_num) :
        assert op_id in src_list_map_dict
        # ファンインのOP1番号のリストのリスト
        src_list_map = src_list_map_dict[op_id]
        # 入力のバインディングを行う．
        sel_src_list = input_binding(src_list_map, 15)
        n = len(sel_src_list)
        op2_spec = Op2Spec(n)
        for i, sel_src in enumerate(sel_src_list) :
            for cstep, (src_id, inv) in sel_src.items() :
                op2_spec.add_src(i, cstep, src_id)
        for cstep, bias in bias_map_dict[op_id].items() :
            op2_spec.add_bias(cstep, bias)

        op2_list.append(op2_spec)

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

    return op1_list, op2_list


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
    reg_spec_list = bind_register(dfg)

    # セレクタの生成を行う．
    op1_list, op2_list = alloc_selecter(dfg)

    return reg_spec_list, op1_list, op2_list


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
    op1_conf = (128, )
    m_conf = (1, 2)
    s_conf = (1, 2, 3)
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
                    bind(dfg)
