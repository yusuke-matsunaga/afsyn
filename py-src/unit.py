#! /usr/bin/env python3

### @file unit.py
### @brief Unit の定義ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

### @brief セレクタの仕様を表すクラス
class MuxSpec :

    ### @brief 初期化
    def __init__(self) :
        self.__src_cond_dict = dict()
        self.__src_list = list()

    ### @brief 入力を追加する．
    ### @param[in] src_id ソースの演算器番号
    ### @param[in] cstep コントロールステップ
    def add_src(self, src_id, cstep) :
        if src_id not in self.__src_cond_dict :
            self.__src_cond_dict[src_id] = list()
            self.__src_list.append(src_id)
        self.__src_cond_dict[src_id].append(cstep)

    ### @brief ソースのリストを返す．
    @property
    def src_list(self) :
        return self.__src_list

    ### @brief ソースの条件(cstep)のリストを返す．
    def src_cond(self, src_id) :
        return self.__src_cond_dict[src_id]


### @brief 演算器を表すクラス
class Unit :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] input_num 入力数
    def __init__(self, id, input_num) :
        self.__id = id
        self.__input_num = input_num
        self.__mux_list = [ MuxSpec() for i in range(input_num) ]

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] src_id ソースのレジスタ番号
    ### @param[in] cstep コントロールステップ
    def add_src(self, i, src_id, cstep) :
        self.__mux_list[i].add_src(src_id, cstep)

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 入力のセレクタ情報を返す．
    ### @param[in] i 入力番号
    def mux_spec(self, i) :
        return self.__mux_list[i]

    ### @brief ロードユニットのときに True を返す．
    def is_load_unit(self) :
        return False

    ### @brief ストアユニットのときに True を返す．
    def is_store_unit(self) :
        return False

    ### @brief OP1ユニットのときに True を返す．
    def is_op1_unit(self) :
        return False

    ### @brief OP2ユニットのときに True を返す．
    def is_op2_unit(self) :
        return False

    ### @brief レジスタのときに True を返す．
    def is_reg_unit(self) :
        return False


### @brief ロードユニット
class LoadUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] block_id ブロック番号
    ### @param[in] offset オフセット
    def __init__(self, id, block_id, offset) :
        super().__init__(id, 0)
        self.__block_id = block_id
        self.__offset = offset

    ### @brief ロードユニットのときに True を返す．
    def is_load_unit(self) :
        return True

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block_id

    ### @brief オフセットを返す．
    @property
    def offset(self) :
        return self.__offset


### @brief ストアユニット
class StoreUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] block_id ブロック番号
    def __init__(self, id, block_id) :
        super().__init__(id, 1)
        self.__block_id = block_id

    ### @brief ストアユニットのときに True を返す．
    def is_store_unit(self) :
        return True

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block_id


### @brief OP1ユニット
class Op1Unit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] input_num 入力番号
    def __init__(self, id, input_num) :
        super().__init__(id, input_num)
        self.__inv_cond_list = [ list() for i in range(input_num) ]

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] cstep コントロールステップ
    ### @param[in] src_id ソースのレジスタ番号
    ### @param[in] inv 反転する時に True にするフラグ
    def add_src(self, i, src_id, cstep, inv) :
        super().add_src(i, src_id, cstep)
        if inv :
            self.__inv_cond_list[i].append(cstep)

    ### @brief OP1ユニットのときに True を返す．
    def is_op1_unit(self) :
        return True

    ### @brief 入力の反転条件(コントロールステップ)を返す．
    def inv_cond(self, i) :
        return self.__inv_cond_list[i]


### @brief OP2ユニット
class Op2Unit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] input_num 入力番号
    def __init__(self, id, input_num) :
        super().__init__(id, input_num)
        self.__bias_map = dict()

    ### @brief cstep ごとの bias 値を設定する．
    def add_bias(self, bias, cstep) :
        self.__bias_map[cstep] = bias

    ### @brief OP2ユニットのときに True を返す．
    def is_op2_unit(self) :
        return True

    ### @brief bias値の辞書を返す．
    @property
    def bias_map(self) :
        return self.__bias_map


### @brief レジスタの仕様を表すクラス
class RegUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id ユニット番号
    ### @param[in] reg_id レジスタ番号
    def __init__(self, id, reg_id) :
        super().__init__(id, 1)
        self.__reg_id = reg_id
        self.__var_list = list()
        self.__last_step = 0
        self.__src_map = dict()

    ### @brief ソースの情報を追加する．
    def add_src(self, node) :
        var = node.var
        self.__var_list.append(var)
        if self.__last_step < var.end :
            self.__last_step = var.end
        var.bind(self.reg_id)
        cstep = var.start
        op_id = node.unit_id
        if op_id not in self.__src_map :
            self.__src_map[op_id] = list()
        self.__src_map[op_id].append(cstep)

    ### @brief レジスタのときに True を返す．
    def is_reg_unit(self) :
        return True

    ### @brief レジスタ番号を返す．
    @property
    def reg_id(self) :
        return self.__reg_id

    ### @brief 割り当てられている変数のリストを返す．
    @property
    def var_list(self) :
        return self.__var_list

    ### @brief 現在の使用されている最後のステップを返す．
    @property
    def last_step(self) :
        return self.__last_step

    ### @brief 同じソースがあったら True を返す．
    def has_samesrc(self, node) :
        return node.unit_id in self.__src_map

    ### @brief ソースの辞書を返す．
    ###
    ### キーはユニット番号で値は cstep のリスト
    @property
    def src_map(self) :
        return self.__src_map


### @brief 演算器を管理するマネージャ
class UnitMgr :

    ### @brief 初期化
    def __init__(self) :
        self.__unit_list = list()
        self.__lu_list = list()
        self.__su_list = list()
        self.__op1_list = list()
        self.__op2_list = list()
        self.__reg_list = list()

    ### @brief 全てのユニットのリストを返す．
    @property
    def unit_list(self) :
        return self.__unit_list

    ### @brief Load Unit のリストを返す．
    @property
    def load_unit_list(self) :
        return self.__lu_list

    ### @brief Store Unit のリストを返す．
    @property
    def store_unit_list(self) :
        return self.__su_list

    ### @brief OP1 Unit のリストを返す．
    @property
    def op1_list(self) :
        return self.__op1_list

    ### @brief OP2 Unit のリストを返す．
    @property
    def op2_list(self) :
        return self.__op2_list

    ### @brief レジスタのリストを返す．
    @property
    def reg_list(self) :
        return self.__reg_list

    ### @brief Load Unit を作る．
    ### @param[in] block_id ブロック番号
    ### @param[in] offset オフセット
    def new_load_unit(self, block_id, offset) :
        id = len(self.__unit_list)
        lu = LoadUnit(id, block_id, offset)
        self.__unit_list.append(lu)
        self.__lu_list.append(lu)
        return lu

    ### @brief Store Unit を作る．
    ### @param[in] block_id ブロック番号
    def new_store_unit(self, block_id) :
        id = len(self.__unit_list)
        su = StoreUnit(id, block_id)
        self.__unit_list.append(su)
        self.__su_list.append(su)
        return su

    ### @brief OP1 Unit を作る．
    ### @param[in] input_num 入力数
    def new_op1_unit(self, input_num) :
        id = len(self.__unit_list)
        op = Op1Unit(id, input_num)
        self.__unit_list.append(op)
        self.__op1_list.append(op)
        return op

    ### @brief OP2 Unit を作る．
    ### @param[in] input_num 入力数
    def new_op2_unit(self, input_num) :
        id = len(self.__unit_list)
        op = Op2Unit(id, input_num)
        self.__unit_list.append(op)
        self.__op2_list.append(op)
        return op

    ### @brief レジスタを作る．
    def new_reg_unit(self) :
        id = len(self.__unit_list)
        reg_id = len(self.__reg_list)
        reg = RegUnit(id, reg_id)
        self.__unit_list.append(reg)
        self.__reg_list.append(reg)
        return reg

    ### @brief 動作シミュレーションを行う．
    ### @param[in] dfg 対象のグラフ
    ### @param[in] ivals 入力値
    ### @return 出力値を納めた辞書を返す．
    def simulate(self, dfg, ivals) :
        for step in range(dfg.total_step) :
            for unit in self.__unit_list :
                pass

    ### @brief 内容を出力する．
    def print(self, fout) :
        # Load Unit の内容を出力する．
        print('Load Unit', file = fout)
        for lu in self.load_unit_list :
            print('Unit#{}'.format(lu.id), file = fout)
            print('  memory block: {}'.format(lu.block_id), file = fout)

        # Op1 Unit の内容を出力する．
        print('Op1 Unit', file = fout)
        for op1 in self.op1_list :
            print('Unit#{}'.format(op1.id), file = fout)
            for i in range(op1.input_num) :
                print('  Input#{}'.format(i), file = fout)
                mux_spec = op1.mux_spec(i)
                for src in mux_spec.src_list :
                    if src == -1 :
                        continue
                    print('    {} @ ('.format(src), end = '', file = fout)
                    cond_list = mux_spec.src_cond(src)
                    for cond in cond_list :
                        print(' {}'.format(cond), end = '', file = fout)
                    print(')', file = fout)
            print(file = fout)

        # Op2 Unit の内容を出力する．
        print('Op2 Unit', file = fout)
        for op2 in self.op2_list :
            print('Unit#{}'.format(op2.id), file = fout)
            for i in range(op2.input_num) :
                print('  Input#{}'.format(i), file = fout)
                mux_spec = op2.mux_spec(i)
                for src in mux_spec.src_list :
                    if src == -1 :
                        continue
                    print('    {} @ ('.format(src), end = '', file = fout)
                    cond_list = mux_spec.src_cond(src)
                    for cond in cond_list :
                        print(' {}'.format(cond), end = '', file = fout)
                    print(')', file = fout)
            print(file = fout)

        # Store Unit の内容を出力する．
        print('Store Unit', file = fout)
        for su in self.store_unit_list :
            print('Unit#{}'.format(su.id), file = fout)
            print('  memory block: {}'.format(su.block_id), file = fout)
            mux_spec = su.mux_spec(0)
            for src in mux_spec.src_list :
                if src == -1 :
                    continue
                print('    {} @ ('.format(src), end = '', file = fout)
                cond_list = mux_spec.src_cond(src)
                for cond in cond_list :
                    print(' {}'.format(cond), end = '', file = fout)
                print(')', file = fout)
            print(file = fout)
