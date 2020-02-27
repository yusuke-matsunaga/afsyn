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


### @brief DFG を表すクラス
class DFG :

    ### @brief 初期化
    ###
    ### 空のグラフを生成する．
    def __init__(self) :
        self.__node_list = []
        self.__output_list = []

    ### @brief メモリノードを作る．
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def make_input(self, block_id, bank_id, offset) :
        id = len(self.__node_list)
        node = MemNode(id, block_id, bank_id, offset)
        self.__node_list.append(node)
        return node

    ### @brief 演算ノードを作る．
    ### @param[in] fanin_list ファンインノードのリスト
    ### @param[in] level レベル(1 or 2)
    ### @param[in] weight_list 重みのリスト
    def make_op(self, fanin_list, level, weight_list = None) :
        id = len(self.__node_list)
        node = OpNode(id, fanin_list, level, weight_list)
        self.__node_list.append(node)
        if level == 2 :
            self.__output_list.append(node)
        return node

    ### @brief 全ノードのリストを返す．
    @property
    def node_list(self) :
        return self.__node_list

    ### @brief 出力(OP2)ノードのリストを返す．
    @property
    def output_list(self) :
        return self.__output_list


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
            node = dfg.make_input(block_id, bank_id, offset)
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
    print('# of outputs: {}'.format(len(dfg.output_list)))
