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
        self.__unit_id = -1

    ### @brief Unit に割り当てる．
    ### @param[in] unit_id ユニット番号
    def bind(self, unit_id) :
        self.__unit_id = unit_id

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief 対応する Load Unit の番号を返す．
    @property
    def unit_id(self) :
        return self.__unit_id

    ### @brief ファンインノードのリスト
    @property
    def fanin_list(self) :
        return self.__fanin_list

    ### @brief メモリソースノードのとき True を返す．
    @property
    def is_memsrc(self) :
        return False

    ### @brief メモリシンクノードのとき True を返す．
    @property
    def is_memsink(self) :
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


### @brief メモリソースノード
class MemSrcNode(MemNode) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def __init__(self, id, block_id, bank_id, offset) :
        super().__init__(id, block_id, bank_id, offset)

    ### @brief メモリソースノードのとき True を返す．
    @property
    def is_memsrc(self) :
        return True


### @brief メモリシンクノード
class MemSinkNode(MemNode) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    ### @param[in] src 入力ソース
    def __init__(self, id, block_id, bank_id, offset, src) :
        super().__init__(id, block_id, bank_id, offset)
        self.__src = src

    ### @brief メモリシンクノードのとき True を返す．
    @property
    def is_memsink(self) :
        return True

    ### @brief 入力ソースを返す．
    @property
    def src(self) :
        return self.__src

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
        self.__fanout = None

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

    ### @brief 負の重みを持つ入力数
    @property
    def bias(self) :
        ans = 0
        if self.is_op1 :
            for w in self.__weight_list :
                if w < 0 :
                    ans += 1
        else :
            for inode in self.fanin_list :
                ans += inode.bias
        return ans

    ### @brief ファンアウトをセットする．
    def set_fanout(self, onode) :
        self.__fanout = onode

    ### @brief ファンアウトを返す．
    @property
    def fanout(self) :
        return self.__fanout


### @brief 変数を表すクラス
class Var :

    ### @brief 初期化
    ### @param[in] src ソース
    ### @param[in] start src_id の cstep
    def __init__(self, src, start) :
        self.__src = src
        self.__tgt_id_list = []
        self.__start = start
        self.__end = -1
        self.__unit_id = -1

    ### @brief ターゲットIDを追加する．
    ### @param[in] tgt_id 追加するターゲットID
    ### @param[in] end tgt_id の cstep
    def add_tgt_id(self, tgt_id, end) :
        self.__tgt_id_list.append(tgt_id)
        if self.__end < end :
            self.__end = end
        assert self.__start < self.__end

    ### @brief ソースIDを返す．
    @property
    def src(self) :
        return self.__src

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

    ### @brief ライフタイムがオーバーラップしているか調べる．
    ### @param[in] start ライフタイムの始点
    ### @param[in] end ライフタイムの終点
    ###
    ### - オーバーラップしていた場合，共通な区間を返す．
    ### - オーバーラップしていない場合，None を返す．
    def check_overlap(self, start, end) :
        start1 = self.start
        end1 = self.end
        # 順序を正規化する．
        if start1 > start :
            start1, start = start, start1
            end1, end = end, end1

        if start < end1 :
            if end1 < end :
                return start, end1
            else :
                return start, end
        else :
            return None

    ### @brief Unit 番号を返す．
    @property
    def unit_id(self) :
        return self.__unit_id

    ### @brief Unit に割り当てる．
    ### @param[in] unit_id レジスタID
    ###
    ### 普通はレジスタだが Load Unit の場合がある．
    def bind(self, unit_id) :
        self.__unit_id = unit_id

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
        self.__memsrcnode_list = []
        self.__memsinknode_list = []
        self.__op1node_list = []
        self.__op2node_list = []
        self.__total_step = 0
        self.__op1_num = 0
        self.__op2_num = 0
        self.__reg_num = 0
        self.__var_list = []

    ### @brief メモリソースノードを作る．
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def make_memsrc(self, block_id, bank_id, offset) :
        id = len(self.__node_list)
        node = MemSrcNode(id, block_id, bank_id, offset)
        self.__node_list.append(node)
        self.__memsrcnode_list.append(node)
        return node

    ### @brief メモリシンクノードを作る．
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    ### @param[in] src 入力ソース
    def make_memsink(self, block_id, bank_id, offset, src) :
        id = len(self.__node_list)
        node = MemSinkNode(id, block_id, bank_id, offset, src)
        self.__node_list.append(node)
        self.__memsinknode_list.append(node)
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

    ### @brief メモリソースノードのリストを返す．
    @property
    def memsrcnode_list(self) :
        return self.__memsrcnode_list

    ### @brief メモリシンクノードのリストを返す．
    @property
    def memsinknode_list(self) :
        return self.__memsinknode_list

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
    ###
    ### 事前に eval_resource() を呼ぶ必要がある．
    @property
    def op1_num(self) :
        return self.__op1_num

    ### @brief OP1の個数を返す．
    ###
    ### 事前に eval_resource() を呼ぶ必要がある．
    @property
    def op2_num(self) :
        return self.__op2_num

    ### @brief 必要なレジスタの個数を返す．
    ###
    ### 事前に eval_resource() を呼ぶ必要がある．
    @property
    def reg_num(self) :
        return self.__reg_num

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
        assert len(self.__var_list) == 0

        # 総ステップ数の計算
        max_step = 0
        for node in self.node_list :
            cstep = node.cstep
            assert cstep >= 0
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
        opvar_map = dict()
        for node in self.memsrcnode_list :
            step = node.cstep
            # 同じブロック，同じオフセット，同じcstepなら共有する．
            # （＝同じバンク)
            key = (node.block_id, node.offset, step)
            if key not in memvar_map :
                var = Var(node, step)
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
            ovar = Var(node, node.cstep)
            opvar_map[node.id] = ovar
            self.__var_list.append(ovar)
            node.attach_var(ovar)

        for node in self.op2node_list :
            for inode in node.fanin_list :
                var = opvar_map[inode.id]
                var.add_tgt_id(node.id, node.cstep)
            ovar = Var(node, node.cstep)
            opvar_map[node.id] = ovar
            self.__var_list.append(ovar)
            node.attach_var(ovar)

        for node in self.memsinknode_list :
            inode = node.src
            var = opvar_map[inode.id]
            var.add_tgt_id(node.id, node.cstep)

        # OP1ノードは一対一
        for node in self.op1node_list :
            step = node.cstep
            var = Var(node, step)
            self.__var_list.append(var)
            node.attach_var(var)

        for node in self.op2node_list :
            tgt_id = node.id
            step = node.cstep
            for inode in node.fanin_list :
                var = inode.var
                var.add_tgt_id(tgt_id, step)

        # レジスタのリソース量の計算
        svar_list = sorted(self.__var_list)
        max_n = 0
        for step in range(self.total_step) :
            n = 0
            for var in svar_list :
                if var.start +1 == var.end :
                    inode = var.src
                    if inode.is_memsrc or inode.is_op2 :
                        continue
                if var.end <= step :
                    continue
                elif var.start > step :
                    break
                # var.start <= step < var.end
                n += 1
            if max_n < n :
                max_n = n
        self.__reg_num = max_n


### @brief DFG を作る
### @param[in] op_list 演算リスト
### @param[in] imem_layout 入力メモリレイアウト
### @param[in] omem_layout 出力メモリレイアウト
### @return DFG を返す．
def make_graph(op_list, imem_layout, omem_layout) :
    dfg = DFG()
    for o_id, op in enumerate(op_list) :
        l1_fanin_list = []
        l1_fanin_num = 0
        l1_weight_list = []
        l2_fanin_list = []
        for i_id, w in op.fanin_list :
            block_id = imem_layout.block_id(i_id)
            bank_id = imem_layout.bank_id(i_id)
            offset = imem_layout.offset(i_id)
            mem_node = dfg.make_memsrc(block_id, bank_id, offset)
            if w == 0.25 :
                n = 2
            else :
                n = 1
            if l1_fanin_num + n >= 16 :
                op_node = dfg.make_op(l1_fanin_list, 1, l1_weight_list)
                l2_fanin_list.append(op_node)
                l1_fanin_list = []
                l1_fanin_num = 0
                l1_weight_list = []
            l1_fanin_list.append(mem_node)
            l1_weight_list.append(w)
            l1_fanin_num += n

        if l1_fanin_num > 0 :
            op_node = dfg.make_op(l1_fanin_list, 1, l1_weight_list)
            l2_fanin_list.append(op_node)
        node = dfg.make_op(l2_fanin_list, 2)
        for inode in l2_fanin_list :
            inode.set_fanout(node)
        block_id = omem_layout.block_id(o_id)
        bank_id = omem_layout.bank_id(o_id)
        offset = omem_layout.offset(o_id)
        onode = dfg.make_memsink(block_id, bank_id, offset, node)
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
    omem_layout = MemLayout(omemory_size, oblock_num, obank_size)
    dfg = make_graph(op_list, imem_layout, omem_layout)
    print('# of nodes: {}'.format(len(dfg.node_list)))
    print('# of OP1 nodes: {}'.format(len(dfg.op1node_list)))
    print('# of OP2 nodes: {}'.format(len(dfg.op2node_list)))
    print('# of MemSink:   {}'.format(len(dfg.memsinknode_list)))

    for node in dfg.memsrcnode_list :
        print('[MEMSRC] #{}: {}-{}-{}'.format(node.id, node.block_id, node.bank_id, node.offset))

    for node in dfg.memsinknode_list :
        print('[MEMSINK] #{}: {}-{}-{}'.format(node.id, node.block_id, node.bank_id, node.offset))
