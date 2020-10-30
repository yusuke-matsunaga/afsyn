#! /usr/bin/env python3

### @file dfg.py
### @brief DFG を表すクラス
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


from afsyn.unit import Unit

### @brief DFG のノードを表すクラス
###
### このクラス自体は他のクラスの基底クラスで
### 継承クラスが実装するメンバ関数の雛形を定義している．
class Node :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] fanin_list ファンインノードのリスト
    def __init__(self, id, fanin_list, latency = 1) :
        self.__id = id
        self.__fanin_list = list(fanin_list)
        self.__cstep = -1
        self.__latency = latency
        self.__var = None
        self.__unit = None

    ### @brief Unit に割り当てる．
    ### @param[in] unit ユニット
    def bind(self, unit) :
        self.__unit = unit

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief 対応する Unit を返す．
    @property
    def unit(self) :
        return self.__unit

    ### @brief ファンイン数を返す．
    @property
    def fanin_num(self) :
        return len(self.__fanin_list)

    ### @brief ファンインを返す．
    def fanin(self, pos) :
        return self.__fanin_list[pos]

    ### @brief ファンインノードのリスト
    @property
    def fanin_list(self) :
        for inode in self.__fanin_list :
            yield inode

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

    ### @brief このノードの結果を利用可能なステップを返す．
    @property
    def next_step(self) :
        return self.__cstep + self.__latency

    ### @brief このノードのレイテンシを返す．
    @property
    def latency(self) :
        return self.__latency

    ### @brief 関連する変数をセットする．
    ### @param[in] var 関連する変数
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
    ### @param[in] addr アドレス
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def __init__(self, id, latency, addr, block_id, bank_id, offset) :
        super().__init__(id, [], latency)
        self.__addr = addr
        self.__block_id = block_id
        self.__bank_id = bank_id
        self.__offset = offset

    ### @brief アドレスを返す．
    @property
    def addr(self) :
        return self.__addr

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
    ### @param[in] addr アドレス
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def __init__(self, id, addr, block_id, bank_id, offset) :
        super().__init__(id, 2, addr, block_id, bank_id, offset)

    ### @brief メモリソースノードのとき True を返す．
    @property
    def is_memsrc(self) :
        return True

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'imem[{}:{},{},{}]'.format(self.addr, self.block_id, self.bank_id, self.offset)

    ### @brief 内容を出力する．
    def print(self) :
        print('{}'.format(self.name))

    ### @brief シミュレーションを行う．
    ### @param[in] ivals 入力値を収めた辞書
    ### @param[in] val_dict ノードの値を格納する辞書
    def simulate(self, ivals, val_dict, debug = False) :
        addr = self.addr
        val = ivals[addr]
        val_dict[self.id] = val
        if debug :
            print('{}: {}'.format(self.name, val))


### @brief メモリシンクノード
class MemSinkNode(MemNode) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] addr アドレス
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    ### @param[in] src 入力ソース
    def __init__(self, id, addr, block_id, bank_id, offset, src) :
        super().__init__(id, 1, addr, block_id, bank_id, offset)
        self.__src = src

    ### @brief メモリシンクノードのとき True を返す．
    @property
    def is_memsink(self) :
        return True

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'omem[{}]'.format(self.addr)

    ### @brief 入力ソースを返す．
    @property
    def src(self) :
        return self.__src

    ### @brief 内容を出力する．
    def print(self) :
        print('{}'.format(self.name))

    ### @brief シミュレーションを行う．
    ### @param[in] val_dict ノードの値を格納する辞書
    ### @param[in] ovals 出力値を収める辞書
    def simulate(self, val_dict, ovals, debug = False) :
        inode = self.src
        assert inode.id in val_dict
        val = val_dict[inode.id]
        addr = self.addr
        ovals[addr] = val
        if debug :
            print('{} <= {}'.format(self.name, val))


### @brief 演算ノード
class OpNode(Node) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] op_id 演算器番号
    ### @param[in] fanin_list ファンインノードのリスト
    def __init__(self, id, op_id, fanin_list) :
        super().__init__(id, fanin_list)
        self.__op_id = op_id
        self.__fanout = None

    ### @brief 演算器番号を返す．
    @property
    def op_id(self) :
        return self.__op_id

    ### @brief ファンアウトをセットする．
    def set_fanout(self, onode) :
        self.__fanout = onode

    ### @brief ファンアウトを返す．
    @property
    def fanout(self) :
        return self.__fanout


### @brief タイプ1演算ノード
class Op1Node(OpNode) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] op_id 演算器番号
    ### @param[in] fanin_list ファンインノードのリスト
    ### @param[in] weight_list 重みのリスト
    def __init__(self, id, op_id, fanin_list, weight_list) :
        super().__init__(id, op_id, fanin_list)
        self.__weight_list = list(weight_list)

    ### @brief OP1ノードのとき True を返す．
    @property
    def is_op1(self) :
        return True

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'op1[{}]'.format(self.op_id)

    ### @brief 重みを返す．
    def weight(self, pos) :
        return self.__weight_list[pos]

    ### @brief 重みのリストを返す．
    @property
    def weight_list(self) :
        for w in self.__weight_list :
            yield w

    ### @brief 内容を出力する．
    def print(self) :
        print('{}: @{}'.format(self.name, self.cstep))
        for i, inode in enumerate(self.fanin_list) :
            print('  Input#{}: {} x {}'.format(i, inode.name, self.weight(i)))

    ### @brief シミュレーションを行う．
    ### @param[in] val_dict ノードの値を格納する辞書
    def simulate(self, val_dict, debug = False) :
        val = 0
        for i, inode in enumerate(self.fanin_list) :
            assert inode.id in val_dict
            ival = val_dict[inode.id]
            w = self.weight(i)
            if w == 0.125 :
                ival1 = ival
            elif w == -0.125 :
                ival1 = ~ival
            elif w == 0.25 :
                ival1 = ival + ival
            elif w == -0.25 :
                ival1 = ~ival + ~ival
            elif w == 0.375 :
                ival1 = ival + ival + ival
            elif w == -0.375 :
                ival1 = ~ival + ~ival + ~ival
            else :
                print('w = {}'.format(w))
                assert False
            val += ival1
        val_dict[self.id] = val
        if debug :
            print('{}:'.format(self.name))
            for i, inode in enumerate(self.fanin_list) :
                ival = val_dict[inode.id]
                w = self.weight(i)
                if w == 0.125 :
                    ival1 = ival
                elif w == -0.125 :
                    ival1 = ~ival
                elif w == 0.25 :
                    ival1 = ival + ival
                elif w == -0.25 :
                    ival1 = ~ival + ~ival
                elif w == 0.375 :
                    ival1 = ival + ival + ival
                elif w == -0.375 :
                    ival1 = ~ival + ~ival + ~ival
                print('  {}: {} => {}'.format(inode.name, ival, ival1))
            print(' => {}'.format(val))


### @brief タイプ2演算ノード
class Op2Node(OpNode) :

    ### @brief 初期化
    ### @param[in] id ID番号
    ### @param[in] op_id 演算器番号
    ### @param[in] fanin_list ファンインノードのリスト
    def __init__(self, id, op_id, fanin_list) :
        super().__init__(id, op_id, fanin_list)
        bias = 0
        for inode in self.fanin_list :
            for w in inode.weight_list :
                if w == -0.125 :
                    bias += 1
                elif w == -0.25 :
                    bias += 2
                elif w == -0.375 :
                    bias += 3
        self.__bias = bias

    ### @brief OP2ノードのとき True を返す．
    @property
    def is_op2(self) :
        return True

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'op2[{}]'.format(self.op_id)

    ### @brief 負の重みを持つ入力数
    @property
    def bias(self) :
        return self.__bias

    ### @brief 内容を出力する．
    def print(self) :
        print('{}: @{}'.format(self.name, self.cstep))
        for i, inode in enumerate(self.fanin_list) :
            print('  Input#{}: {}'.format(i, inode.name))
        print('  Bias: {}'.format(self.bias))

    ### @brief シミュレーションを行う．
    ### @param[in] val_dict ノードの値を格納する辞書
    def simulate(self, val_dict, debug) :
        val = self.bias
        for i, inode in enumerate(self.fanin_list) :
            assert inode.id in val_dict
            ival = val_dict[inode.id]
            val += ival
        val *= 0.125
        val_dict[self.id] = val
        if debug :
            print('{}:'.format(self.name))
            for i, inode in enumerate(self.fanin_list) :
                ival = val_dict[inode.id]
                print('  {}: {}'.format(inode.name, ival))
            print('  BIAS: {}'.format(self.bias))
            print(' => {}'.format(val))


### @brief 変数を表すクラス
class Var :

    ### @brief 初期化
    ### @param[in] src ソースノード
    ### @param[in] start 開始ステップ
    def __init__(self, src, start) :
        self.__src = src
        self.__tgt_list = []
        self.__start = start
        self.__end = -1
        self.__unit = None

    ### @brief ターゲットIDを追加する．
    ### @param[in] tgt 追加するターゲット
    def add_tgt(self, tgt) :
        self.__tgt_list.append(tgt)
        cstep = tgt.cstep
        if self.__end < cstep :
            self.__end = cstep
        assert self.__start <= self.__end

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'var#[{}]'.format(self.src.name)

    ### @brief ソースノードを返す．
    @property
    def src(self) :
        return self.__src

    ### @brief ターゲットIDのリストを返す．
    @property
    def tgt_list(self) :
        for tgt in self.__tgt_list :
            yield tgt

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

    ### @brief バインドしている Unit を返す．
    ###
    ### 普通はレジスタだが Load Unit の場合がある．
    @property
    def unit(self) :
        return self.__unit

    ### @brief Unit に割り当てる．
    ### @param[in] unit ユニット
    ###
    ### 普通はレジスタだが Load Unit の場合がある．
    def bind(self, unit) :
        assert isinstance(unit, Unit)
        self.__unit = unit

    ### @brief 内容を出力する．
    def print(self) :
        print('{}@{}'.format(self.name, self.start))
        for tgt in self.tgt_list :
            print('  {}@{}'.format(tgt.name, tgt.cstep))

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
    def __init__(self, op1_limit, op2_limit, imem_layout, omem_layout) :
        self.__op1_limit = op1_limit
        self.__op2_limit = op2_limit
        self.__imem_layout = imem_layout
        self.__omem_layout = omem_layout
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

    ### @brief OP1ノードのファンイン数制約を返す．
    @property
    def op1_limit(self) :
        return self.__op1_limit

    ### @brief OP2ノードのファンイン数制約を返す．
    @property
    def op2_limit(self) :
        return self.__op2_limit

    ### @brief 入力用メモリレイアウトを返す．
    @property
    def imem_layout(self) :
        return self.__imem_layout

    ### @brief 出力用メモリレイアウトを返す．
    @property
    def omem_layout(self) :
        return self.__omem_layout

    ### @brief メモリソースノードを作る．
    ### @param[in] i_id 入力番号
    def make_memsrc(self, i_id) :
        id = len(self.__node_list)
        block_id, bank_id, offset = self.__imem_layout.decode(i_id)
        node = MemSrcNode(id, i_id, block_id, bank_id, offset)
        self.__node_list.append(node)
        self.__memsrcnode_list.append(node)
        return node

    ### @brief メモリシンクノードを作る．
    ### @param[in] o_id 出力番号
    ### @param[in] src 入力ソース
    def make_memsink(self, o_id, src) :
        id = len(self.__node_list)
        block_id, bank_id, offset = self.__omem_layout.decode(o_id)
        node = MemSinkNode(id, o_id, block_id, bank_id, offset, src)
        self.__node_list.append(node)
        self.__memsinknode_list.append(node)
        return node

    ### @brief タイプ1演算ノードを作る．
    ### @param[in] fanin_list ファンインノードのリスト
    ### @param[in] weight_list 重みのリスト
    def make_op1(self, fanin_list, weight_list) :
        id = len(self.__node_list)
        op_id = len(self.__op1node_list)
        node = Op1Node(id, op_id, fanin_list, weight_list)
        self.__node_list.append(node)
        self.__op1node_list.append(node)
        return node

    ### @brief タイプ2演算ノードを作る．
    ### @param[in] fanin_list ファンインノードのリスト
    def make_op2(self, fanin_list) :
        id = len(self.__node_list)
        op_id = len(self.__op2node_list)
        node = Op2Node(id, op_id, fanin_list)
        self.__node_list.append(node)
        self.__op2node_list.append(node)
        return node

    ### @brief 入力のメモリレイアウトを返す．
    @property
    def imem_layout(self) :
        return self.__imem_layout

    ### @brief 出力のメモリレイアウトを返す．
    @property
    def omem_layout(self) :
        return self.__omem_layout

    ### @brief 全ノード数を返す．
    @property
    def node_num(self) :
        return len(self.__node_list)

    ### @brief 全ノードのリストを返す．
    @property
    def node_list(self) :
        for node in self.__node_list :
            yield node

    ### @brief メモリソースノード数を返す．
    @property
    def memsrcnode_num(self) :
        return len(self.__memsrcnode_list)

    ### @brief メモリソースノードのリストを返す．
    @property
    def memsrcnode_list(self) :
        for node in self.__memsrcnode_list :
            yield node

    ### @brief メモリシンクノード数を返す．
    @property
    def memsinknode_num(self) :
        return len(self.__memsinknode_list)

    ### @brief メモリシンクノードのリストを返す．
    @property
    def memsinknode_list(self) :
        for node in self.__memsinknode_list :
            yield node

    ### @brief OP1ノード数を返す．
    @property
    def op1node_num(self) :
        return len(self.__op1node_list)

    ### @brief OP1ノードのリストを返す．
    @property
    def op1node_list(self) :
        for node in self.__op1node_list :
            yield node

    ### @brief OP2ノード数を返す．
    @property
    def op2node_num(self) :
        return len(self.__op2node_list)

    ### @brief OP2ノードのリストを返す．
    @property
    def op2node_list(self) :
        for node in self.__op2node_list :
            yield node

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
        # 実際にはジェネレータを返す．
        for var in self.__var_list :
            yield var

    ### @brief リソース量の見積もりを行う．
    ###
    ### 各ノードのスケジュールが済んでいる必要がある．
    def eval_resource(self) :
        assert len(self.__var_list) == 0

        # 総ステップ数の計算
        max_step = 0
        for node in self.node_list :
            step = node.next_step
            assert step >= 0
            if max_step < step :
                max_step = step
        self.__total_step = max_step

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
            # 同じブロック，同じオフセット，同じcstepなら共有する．
            # （＝同じバンク)
            key = (node.block_id, node.offset, node.cstep)
            if key not in memvar_map :
                var = Var(node, node.cstep + 1) # メモリ読み出しに1クロックかかる
                memvar_map[key] = var
                self.__var_list.append(var)
            else :
                var = memvar_map[key]
            node.attach_var(var)

        # OP1ノードに対しては一対一で変数が対応する．
        for node in self.op1node_list :
            for inode in node.fanin_list :
                # ファンインのノードの変数のターゲットを追加する．
                key = (inode.block_id, inode.offset, inode.cstep)
                var = memvar_map[key]
                var.add_tgt(node)
            ovar = Var(node, node.cstep)
            opvar_map[node.id] = ovar
            self.__var_list.append(ovar)
            node.attach_var(ovar)

        # OP2ノードに対しては一対一で変数が対応する．
        for node in self.op2node_list :
            for inode in node.fanin_list :
                # ファンインのノードの変数のターゲットを追加する．
                var = opvar_map[inode.id]
                var.add_tgt(node)
            ovar = Var(node, node.cstep)
            opvar_map[node.id] = ovar
            self.__var_list.append(ovar)
            node.attach_var(ovar)

        # メモリシンクノード自体は変数を持たない．
        # そのソースのターゲットを設定する．
        for node in self.memsinknode_list :
            inode = node.src
            var = opvar_map[inode.id]
            var.add_tgt(node)

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

    ### @brief 内容を出力する．
    def print(self) :
        for node in self.op1node_list :
            node.print()
        for node in self.op2node_list :
            node.print()
        for node in self.memsinknode_list :
            node.print()
        for var in self.var_list :
            var.print()

    ### @brief シミュレーションを行う．
    ### @param[in] ivals 入力の値のリスト
    ### @return 出力値を格納した辞書を返す．
    ###
    ### ivals は ivals[x] で値が取得できればなんでもよい．
    def simulate(self, ivals, debug = False) :
        ovals = dict()
        val_dict = dict()

        for node in self.memsrcnode_list :
            node.simulate(ivals, val_dict, debug)

        for node in self.op1node_list :
            node.simulate(val_dict, debug)

        for node in self.op2node_list :
            node.simulate(val_dict, debug)

        for node in self.memsinknode_list :
            inode = node.src
            assert inode.id in val_dict
            val = val_dict[inode.id]
            block_id = node.block_id
            bank_id = node.bank_id
            offset = node.offset
            addr = self.__omem_layout.encode(block_id, bank_id, offset)
            ovals[addr] = val

        return ovals
