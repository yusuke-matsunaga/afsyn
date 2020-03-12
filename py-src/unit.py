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
    def _add_src(self, i, src_id, cstep) :
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


### @brief メモリを表すクラス
class MemoryBlock :

    ### @brief 初期化
    ### @param[in] block_id ブロック番号
    def __init__(self, block_id) :
        self.__block_id = block_id
        self.__cond_dict = dict()

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block_id

    ### @brief バンク選択条件を追加する．
    def add_cond(self, cstep, bank_id) :
        if cstep in self.__cond_dict :
            assert self.__cond_dict[cstep] == bank_id
        else :
            self.__cond_dict[cstep] = bank_id

    ### @brief バンク選択条件の辞書を返す．
    ###
    ### cstep をキーとしてそのときに選択されて
    ### いるバンク番号を格納している．
    @property
    def cond_dict(self) :
        return self.__cond_dict


### @brief ロードユニット
class LoadUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] mem_block ブロック
    ### @param[in] offset オフセット
    def __init__(self, id, mem_block, offset) :
        super().__init__(id, 0)
        self.__block = mem_block
        self.__offset = offset

    ### @brief ロード条件を追加する．
    def add_cond(self, cstep, bank_id) :
        self.__block.add_cond(cstep, bank_id)

    ### @brief ロードユニットのときに True を返す．
    def is_load_unit(self) :
        return True

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block.block_id

    ### @brief オフセットを返す．
    @property
    def offset(self) :
        return self.__offset

    ### @brief バンク選択条件の辞書を返す．
    ###
    ### cstep をキーとしてそのときに選択されて
    ### いるバンク番号を格納している．
    @property
    def cond_dict(self) :
        return self.__block.cond_dict


### @brief ストアユニット
class StoreUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] mem_block ブロック
    def __init__(self, id, mem_block) :
        super().__init__(id, 1)
        self.__block = mem_block

    ### @brief ストア条件を追加する．
    def add_src(self, src_id, cstep, bank_id) :
        super()._add_src(0, src_id, cstep)
        self.__block.add_cond(cstep, bank_id)

    ### @brief ストアユニットのときに True を返す．
    def is_store_unit(self) :
        return True

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block.block_id

    ### @brief バンク選択条件の辞書を返す．
    ###
    ### cstep をキーとしてそのときに選択されて
    ### いるバンク番号を格納している．
    @property
    def cond_dict(self) :
        return self.__block.cond_dict


### @brief OP1ユニット
class Op1Unit(Unit) :

    ### @brief 初期化
    ### @param[in] id ユニット番号
    ### @param[in] op_id 演算器番号
    ### @param[in] input_num 入力番号
    def __init__(self, id, op_id, input_num) :
        super().__init__(id, input_num)
        self.__op_id = op_id
        self.__inv_cond_list = [ list() for i in range(input_num) ]

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] cstep コントロールステップ
    ### @param[in] src_id ソースのレジスタ番号
    ### @param[in] inv 反転する時に True にするフラグ
    def add_src(self, i, src_id, cstep, inv) :
        super()._add_src(i, src_id, cstep)
        if inv :
            self.__inv_cond_list[i].append(cstep)

    ### @brief OP1ユニットのときに True を返す．
    def is_op1_unit(self) :
        return True

    ### @brief 演算器番号を返す．
    @property
    def op_id(self) :
        return self.__op_id

    ### @brief 入力の反転条件(コントロールステップ)を返す．
    def inv_cond(self, i) :
        return self.__inv_cond_list[i]


### @brief OP2ユニット
class Op2Unit(Unit) :

    ### @brief 初期化
    ### @param[in] id ユニット番号
    ### @param[in] op_id 演算器番号
    ### @param[in] input_num 入力番号
    def __init__(self, id, op_id, input_num) :
        super().__init__(id, input_num)
        self.__op_id = op_id
        self.__bias_map = dict()

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] cstep コントロールステップ
    ### @param[in] src_id ソースのレジスタ番号
    def add_src(self, i, src_id, cstep) :
        super()._add_src(i, src_id, cstep)

    ### @brief cstep ごとの bias 値を設定する．
    def add_bias(self, bias, cstep) :
        self.__bias_map[cstep] = bias

    ### @brief OP2ユニットのときに True を返す．
    def is_op2_unit(self) :
        return True

    ### @brief 演算器番号を返す．
    @property
    def op_id(self) :
        return self.__op_id

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
        super().__init__(id, 0)
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
        var.bind(self.id)
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
        self.__lm_dict = dict()
        self.__lu_list = list()
        self.__sm_dict = dict()
        self.__su_list = list()
        self.__op1_list = list()
        self.__op2_list = list()
        self.__reg_list = list()

    ### @brief 全てのユニットのリストを返す．
    @property
    def unit_list(self) :
        return self.__unit_list

    ### @brief Load Memory のリストを返す．
    @property
    def load_memory_list(self) :
        return self.__lm_dict.values()

    ### @brief Load Unit のリストを返す．
    @property
    def load_unit_list(self) :
        return self.__lu_list

    ### @brief Store Memory のリストを返す．
    @property
    def store_memory_list(self) :
        return self.__sm_dict.values()

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
        lm = self.new_load_memory(block_id)
        lu = LoadUnit(id, lm, offset)
        self.__unit_list.append(lu)
        self.__lu_list.append(lu)
        return lu

    ### @biref Load Memory を作る．
    ### @param[in] block_id ブロック番号
    def new_load_memory(self, block_id) :
        if block_id not in self.__lm_dict :
            lm = MemoryBlock(block_id)
            self.__lm_dict[block_id] = lm
        return self.__lm_dict[block_id]

    ### @brief Store Unit を作る．
    ### @param[in] block_id ブロック番号
    def new_store_unit(self, block_id) :
        id = len(self.__unit_list)
        sm = self.new_store_memory(block_id)
        su = StoreUnit(id, sm)
        self.__unit_list.append(su)
        self.__su_list.append(su)
        return su

    ### @biref Store Memory を作る．
    ### @param[in] block_id ブロック番号
    def new_store_memory(self, block_id) :
        if block_id not in self.__sm_dict :
            sm = MemoryBlock(block_id)
            self.__sm_dict[block_id] = sm
        return self.__sm_dict[block_id]

    ### @brief OP1 Unit を作る．
    ### @param[in] input_num 入力数
    def new_op1_unit(self, input_num) :
        id = len(self.__unit_list)
        op_id = len(self.__op1_list)
        op = Op1Unit(id, op_id, input_num)
        self.__unit_list.append(op)
        self.__op1_list.append(op)
        return op

    ### @brief OP2 Unit を作る．
    ### @param[in] input_num 入力数
    def new_op2_unit(self, input_num) :
        id = len(self.__unit_list)
        op_id = len(self.__op2_list)
        op = Op2Unit(id, op_id, input_num)
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
        print('Load Memory', file = fout)
        for lm in self.load_memory_list :
            print('Load Memory#{}'.format(lm.block_id))
            for cstep, bank_id in lm.cond_dict.items() :
                print('  bank#{} @ {}'.format(bank_id, cstep))

        # Op1 Unit の内容を出力する．
        print('Op1 Unit', file = fout)
        for op1 in self.op1_list :
            print('Op1#{}'.format(op1.op_id), file = fout)
            for i in range(op1.input_num) :
                print('  Input#{}'.format(i), file = fout)
                mux_spec = op1.mux_spec(i)
                for src_id in mux_spec.src_list :
                    if src_id == -1 :
                        continue
                    print('    ', end = '', file = fout)
                    src = self.__unit_list[src_id]
                    UnitMgr.print_src(src, fout)
                    print(' @ (', end = '', file = fout)
                    cond_list = mux_spec.src_cond(src_id)
                    for cond in cond_list :
                        print(' {}'.format(cond), end = '', file = fout)
                    print(')', file = fout)
            print(file = fout)

        # Op2 Unit の内容を出力する．
        print('Op2 Unit', file = fout)
        for op2 in self.op2_list :
            print('Op2#{}'.format(op2.op_id), file = fout)
            for i in range(op2.input_num) :
                print('  Input#{}'.format(i), file = fout)
                mux_spec = op2.mux_spec(i)
                for src_id in mux_spec.src_list :
                    if src_id == -1 :
                        continue
                    src = self.__unit_list[src_id]
                    #assert src.is_reg_unit()
                    UnitMgr.print_src(src, fout)
                    print(' @ (', end = '', file = fout)
                    cond_list = mux_spec.src_cond(src_id)
                    for cond in cond_list :
                        print(' {}'.format(cond), end = '', file = fout)
                    print(')', file = fout)
            print(file = fout)

        # Store Unit の内容を出力する．
        print('Store Memory', file = fout)
        for sm in self.store_memory_list :
            print('Store Memory#{}'.format(sm.block_id), file = fout)
            for cstep, bank_id in sm.cond_dict.items() :
                print('  bank#{} @ {}'.format(bank_id, cstep), file = fout)

        print('Store Unit', file = fout)
        for su in self.store_unit_list :
            print('Store Unit#{}[{}]'.format(su.id, su.block_id))
            mux_spec = su.mux_spec(0)
            for src_id in mux_spec.src_list :
                if src_id == -1 :
                    continue
                print('    ', end = '', file = fout)
                src = self.__unit_list[src_id]
                UnitMgr.print_src(src, fout)
                print(' @ (', end = '', file = fout)
                cond_list = mux_spec.src_cond(src_id)
                for cond in cond_list :
                    print(' {}'.format(cond), end = '', file = fout)
                print(')', file = fout)
            print(file = fout)

        print('Register Unit', file = fout)
        for reg in self.reg_list :
            print('Reg#{}'.format(reg.reg_id))
            for unit_id, cstep in reg.src_map.items() :
                src = self.__unit_list[unit_id]
                print('    ', end = '', file = fout)
                UnitMgr.print_src(src, fout)
                print(' @{}'.format(unit_id, cstep))

    @staticmethod
    def print_src(unit, fout) :
        if unit.is_load_unit() :
            print('Mem#{}[{}]'.format(unit.block_id, unit.offset), end = '', file = fout)
        elif unit.is_reg_unit() :
            print('Reg#{}'.format(unit.reg_id), end = '', file = fout)
        elif unit.is_op1_unit() :
            print('Op1#{}'.format(unit.op_id), end = '', file = fout)
        elif unit.is_op2_unit() :
            print('Op2#{}'.format(unit.op_id), end = '', file = fout)
        else :
            assert False
