#! /usr/bin/env python3

### @file dfg.py
### @brief DFG を表すクラス
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


### @brief DFG のノードを表すクラス
###
### このクラス自体は他のクラスの基底クラスで
### 継承クラスが実装するメンバ関数の雛形を定義している．
class Node :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] fanin_list ファンインノードのリスト
    def __init__(self, id, fanin_list) :
        self.__id = id
        self.__fanin_list = fanin_list
        self.__cstep = -1
        self.__var = None

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief ファンインノードのリスト
    @property
    def fanin_list(self) :
        return self.__fanin_list

    ### @brief メモリノードのとき True を返す．
    @property
    def is_mem(self) :
        return False

    ### @brief OP1ノードのとき True を返す．
    @property
    def is_op1(self) :
        return False

    ### @brief OP2ノードのとき True を返す．
    @property
    def is_op2(self) :
        return False

    ### @brief スケジューリングを行う．
    ### @param[in] cstep このノードの cstep
    def set_schedule(self, cstep) :
        self.__cstep = cstep

    ### @brief cstep を返す．
    @property
    def cstep(self) :
        return self.__cstep

    ### @brief 関連する変数をセットする．
    ### @param[in] var 関連する変数
    ###
    ### OP2 ノードにはない．
    def attach_var(self, var) :
        self.__var = var

    ### @brief 関連する変数を返す．
    @property
    def var(self) :
        return self.__var


### @brief メモリノード
class MemNode(Node) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def __init__(self, id, block_id, bank_id, offset) :
        super().__init__(id, [])
        self.__block_id = block_id
        self.__bank_id = bank_id
        self.__offset = offset

    ### @brief メモリノードのとき True を返す．
    @property
    def is_mem(self) :
        return True

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block_id

    ### @brief バンク番号を返す．
    @property
    def bank_id(self) :
        return self.__bank_id

    ### @brief オフセットを返す．
    @property
    def offset(self) :
        return self.__offset


### @brief 演算ノード
class OpNode(Node) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] fanin_list ファンインノードのリスト
    ### @param[in] level レベル(1 or 2)
    ### @param[in] weight_list 重みのリスト
    ###
    ### level == 2 のときは weight_list はない．
    def __init__(self, id, fanin_list, level, weight_list = None) :
        super().__init__(id, fanin_list)
        self.__level = level
        self.__weight_list = weight_list
        self.__op_id = -1

    ### @brief OP1ノードのとき True を返す．
    @property
    def is_op1(self) :
        return self.__level == 1

    ### @brief OP2ノードのとき True を返す．
    @property
    def is_op2(self) :
        return self.__level == 2

    ### @brief レベルを返す．
    @property
    def level(self) :
        return self.__level

    ### @brief 重みのリストを返す．
    @property
    def weight_list(self) :
        return self.__weight_list

    ### @brief 演算器に割り当てる．
    ### @param[in] op_id 演算器ID
    def bind(self, op_id) :
        self.__op_id = op_id

    ### @brief 演算器番号を返す．
    @property
    def op_id(self) :
        return self.__op_id


### @brief 変数を表すクラス
class Var :

    ### @brief 初期化
    ### @param[in] src_id ソースID
    ### @param[in] start src_id の cstep
    def __init__(self, src_id, start) :
        self.__src_id = src_id
        self.__tgt_id_list = []
        self.__start = start
        self.__end = -1
        self.__reg_id = -1

    ### @brief ターゲットIDを追加する．
    ### @param[in] tgt_id 追加するターゲットID
    ### @param[in] end tgt_id の cstep
    def add_tgt_id(self, tgt_id, end) :
        self.__tgt_id_list.append(tgt_id)
        if self.__end < end :
            self.__end = end

    ### @brief ソースIDを返す．
    @property
    def src_id(self) :
        return self.__src_id

    ### @brief ターゲットIDのリストを返す．
    @property
    def tgt_id_list(self) :
        return self.__tgt_id_list

    ### @brief 開始時刻を返す．
    @property
    def start(self) :
        return self.__start

    ### @brief 終了時刻を返す．
    @property
    def end(self) :
        return self.__end

    ### @brief レジスタIDを返す．
    @property
    def reg_id(self) :
        return self.__reg_id

    ### @brief レジスタに割り当てる．
    ### @param[in] reg_id レジスタID
    def bind(self, reg_id) :
        self.__reg_id = reg_id

    ### @brief 比較演算子
    def __lt__(self, other) :
        if self.__start < other.__start :
            return True
        elif self.__start > other.__start :
            return False
        elif self.__end < other.__end :
            return True
        else :
            return False


### @brief DFG を表すクラス
class DFG :

    ### @brief 初期化
    ###
    ### 空のグラフを生成する．
    def __init__(self) :
        self.__node_list = []
        self.__memnode_list = []
        self.__op1node_list = []
        self.__op2node_list = []
        self.__total_step = 0
        self.__op1_num = 0
        self.__op2_num = 0
        self.__reg_num = 0
        self.__var_list = []

    ### @brief メモリノードを作る．
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def make_mem(self, block_id, bank_id, offset) :
        id = len(self.__node_list)
        node = MemNode(id, block_id, bank_id, offset)
        self.__node_list.append(node)
        self.__memnode_list.append(node)
        return node

    ### @brief 演算ノードを作る．
    ### @param[in] fanin_list ファンインノードのリスト
    ### @param[in] level レベル(1 or 2)
    ### @param[in] weight_list 重みのリスト
    def make_op(self, fanin_list, level, weight_list = None) :
        id = len(self.__node_list)
        node = OpNode(id, fanin_list, level, weight_list)
        self.__node_list.append(node)
        if level == 1 :
            self.__op1node_list.append(node)
        elif level == 2 :
            self.__op2node_list.append(node)
        else :
            assert False
        return node

    ### @brief 全ノードのリストを返す．
    @property
    def node_list(self) :
        return self.__node_list

    ### @brief メモリノードのリストを返す．
    @property
    def memnode_list(self) :
        return self.__memnode_list

    ### @brief OP1ノードのリストを返す．
    @property
    def op1node_list(self) :
        return self.__op1node_list

    ### @brief OP2ノードのリストを返す．
    @property
    def op2node_list(self) :
        return self.__op2node_list

    ### @brief 総ステップ数を得る．
    ###
    ### 事前に eval_resource() を呼ぶ必要がある．
    @property
    def total_step(self) :
        return self.__total_step

    ### @brief OP1の個数を返す．
    @property
    def op1_num(self) :
        return self.__op1_num

    ### @brief OP1の個数を返す．
    @property
    def op2_num(self) :
        return self.__op2_num

    ### @brief 変数のリストを得る．
    ###
    ### 事前に eval_resource() を呼ぶ必要がある．
    @property
    def var_list(self) :
        # コピーを渡す．
        return list(self.__var_list)

    ### @brief リソース量の見積もりを行う．
    ###
    ### 各ノードのスケジュールが済んでいる必要がある．
    def eval_resource(self) :
        # 総ステップ数の計算
        max_step = 0
        for node in self.node_list :
            cstep = node.cstep
            if max_step < cstep :
                max_step = cstep
        self.__total_step = max_step + 1

        # op1, op2 のリソース量の計算
        op1_num_list = [ 0 for i in range(self.total_step) ]
        op2_num_list = [ 0 for i in range(self.total_step) ]
        for node in self.node_list :
            step = node.cstep
            if node.is_op1 :
                op1_num_list[step] += 1
            elif node.is_op2 :
                op2_num_list[step] += 1
        self.__op1_num = 0
        self.__op2_num = 0
        for step in range(self.total_step) :
            if self.__op1_num < op1_num_list[step] :
                self.__op1_num = op1_num_list[step]
            if self.__op2_num < op2_num_list[step] :
                self.__op2_num = op2_num_list[step]

        # 変数を作る．
        # MEM ノードに対しては複数のノードが一つの変数に対応する．
        memvar_map = dict()
        for node in self.memnode_list :
            step = node.cstep
            # 同じブロック，同じオフセット，同じcstepなら共有する．
            # （＝同じバンク)
            key = (node.block_id, node.offset, step)
            if key not in memvar_map :
                var = Var(node.id, step)
                memvar_map[key] = var
                self.__var_list.append(var)
            else :
                var = memvar_map[key]
            node.attach_var(var)

        for node in self.op1node_list :
            for inode in node.fanin_list :
                key = (inode.block_id, inode.offset, inode.cstep)
                var = memvar_map[key]
                var.add_tgt_id(node.id, node.cstep)

        # OP1ノードは一対一
        for node in self.op1node_list :
            step = node.cstep
            var = Var(node.id, step)
            self.__var_list.append(var)
            node.attach_var(var)

        # レジスタのリソース量の計算
        reg_map_list = [ set() for i in range(self.total_step) ]
        for node in self.node_list :
            ostep = node.cstep
            for inode in node.fanin_list :
                istep = inode.cstep
                if inode.is_mem :
                    for step in range(istep + 1, ostep) :
                        reg_map_list[step].add( (inode.block_id, inode.bank_id, inode.offset) )
        reg_num = 0
        for step in range(self.total_step) :
            n = len(reg_map_list[step])
            if reg_num < n :
                reg_num = n

        return self.__op1_num, self.__op2_num, reg_num, self.__total_step


### @brief DFG を作る
### @param[in] op_list 演算リスト
### @param[in] mem_layout メモリレイアウト
### @return DFG を返す．
def make_graph(op_list, mem_layout) :
    dfg = DFG()
    for op in op_list :
        l1_fanin_list = []
        l1_fanin_num = 0
        l1_weight_list = []
        l2_fanin_list = []
        for i_id, w in op.fanin_list :
            block_id = mem_layout.block_id(i_id)
            bank_id = mem_layout.bank_id(i_id)
            offset = mem_layout.offset(i_id)
            node = dfg.make_mem(block_id, bank_id, offset)
            l1_fanin_list.append(node)
            l1_weight_list.append(w)
            l1_fanin_num += 1
            if l1_fanin_num == 16 :
                node = dfg.make_op(l1_fanin_list, 1, l1_weight_list)
                l2_fanin_list.append(node)
                l1_fanin_list = []
                l1_fanin_num = 0
                l1_weight_list = []
        if l1_fanin_num > 0 :
            node = dfg.make_op(l1_fanin_list, 1, l1_weight_list)
            l2_fanin_list.append(node)
        node = dfg.make_op(l2_fanin_list, 2)

    return dfg


if __name__ == '__main__' :
    # テストプログラム
    # Op.dump() ファイルを読み込んで DFG を作る．
    import sys
    import os
    from op import read_op
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

    memory_size = 1500
    block_num = 24
    bank_size = 16
    print('Block num: {}'.format(block_num))
    print('Bank Size: {}'.format(bank_size))
    mem_layout = MemLayout(memory_size, block_num, bank_size)
    dfg = make_graph(op_list, mem_layout)
    print('# of nodes: {}'.format(len(dfg.node_list)))
    print('# of OP1 nodes: {}'.format(len(dfg.op1_list)))
    print('# of OP2 nodes: {}'.format(len(dfg.op2_list)))
