#! /usr/bin/env python3

### @file unit.py
### @brief Unit の定義ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

import sys

debug_out = None

### @brief セレクタの仕様を表すクラス
class MuxSpec :

    ### @brief 初期化
    def __init__(self) :
        self.__src_cond_dict = dict()
        self.__src_list = list()
        self.__src_dict = dict()

    ### @brief 入力を追加する．
    ### @param[in] src ソースのユニット
    ### @param[in] cstep コントロールステップ
    def add_src(self, src, cstep) :
        src_id = src.id
        if src_id not in self.__src_cond_dict :
            self.__src_cond_dict[src_id] = list()
            self.__src_list.append(src)
        self.__src_cond_dict[src_id].append(cstep)
        if cstep in self.__src_dict :
            print('Error in MuxSpec.add_src({}, {})'.format(src_id, cstep))
            for src_id, cond_list in self.__src_cond_dict.items() :
                print('{}: '.format(src_id), end = '')
                for cond in cond_list :
                    print(' {}'.format(cond), end = '')
                print()
        assert cstep not in self.__src_dict
        self.__src_dict[cstep] = src

    ### @brief ソースのリストを返す．
    @property
    def src_list(self) :
        return self.__src_list

    ### @brief ソースの条件(cstep)のリストを返す．
    def src_cond(self, src) :
        return self.__src_cond_dict[src.id]

    ### @brief cstep をキーにしてソースを得る．
    ###
    ### その時刻のソースがない場合には None を返す．
    def src(self, cstep) :
        if cstep in self.__src_dict :
            return self.__src_dict[cstep]
        else :
            return None


### @brief 演算器を表すクラス
class Unit :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] input_num 入力数
    def __init__(self, id, input_num) :
        self.__id = id
        self.__input_num = input_num
        self.__mux_list = [ MuxSpec() for i in range(input_num) ]
        self.__bind_map = dict()

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief バインドする．
    def bind(self, node, cstep) :
        assert cstep not in self.__bind_map
        self.__bind_map[cstep] = node

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] src ソース
    ### @param[in] cstep コントロールステップ
    def _add_src(self, i, src, cstep) :
        if src is None :
            return
        assert not src.is_store_unit
        self.__mux_list[i].add_src(src, cstep)

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 入力のセレクタ情報を返す．
    ### @param[in] i 入力番号
    def mux_spec(self, i) :
        return self.__mux_list[i]

    ### @brief DFG上のノードを返す．
    def node(self, cstep) :
        if cstep in self.__bind_map :
            return self.__bind_map[cstep]
        else :
            return None

    ### @brief ロードユニットのときに True を返す．
    @property
    def is_load_unit(self) :
        return False

    ### @brief ストアユニットのときに True を返す．
    @property
    def is_store_unit(self) :
        return False

    ### @brief OP1ユニットのときに True を返す．
    @property
    def is_op1_unit(self) :
        return False

    ### @brief OP2ユニットのときに True を返す．
    @property
    def is_op2_unit(self) :
        return False

    ### @brief レジスタのときに True を返す．
    @property
    def is_reg_unit(self) :
        return False


### @brief メモリを表すクラス
###
### cstep 毎にどのバンクを選択するかの辞書と
### bank_id 毎に選択している cstep を保持する辞書を持つ．
class MemoryBlock :

    ### @brief 初期化
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_num バンク数
    ### @param[in] bank_size バンクサイズ
    def __init__(self, block_id, bank_num, bank_size) :
        self.__block_id = block_id
        self.__bank_dict = dict()
        self.__cond_dict = dict()
        self.__vals = dict()
        for bank_id in range(bank_num) :
            for offset in range(bank_size) :
                key = bank_id, offset
                self.__vals[key] = None

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block_id

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'MemoryBlock[{}]'.format(self.block_id)

    ### @brief バンク選択条件を追加する．
    def add_cond(self, cstep, bank_id) :
        if cstep in self.__bank_dict :
            assert self.__bank_dict[cstep] == bank_id
        else :
            self.__bank_dict[cstep] = bank_id
        if bank_id not in self.__cond_dict :
            self.__cond_dict[bank_id] = list()
        if cstep not in self.__cond_dict[bank_id] :
            self.__cond_dict[bank_id].append(cstep)

    ### @brief バンクの辞書を返す．
    ###
    ### cstep をキーとしてそのときに選択されて
    ### いるバンク番号を格納している．
    @property
    def bank_dict(self) :
        return self.__bank_dict

    ### @brief バンクが選ばれる条件の辞書を返す．
    @property
    def cond_dict(self) :
        return self.__cond_dict

    ### @brief 値を設定する．
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    ### @param[in] val 値
    def set_val(self, bank_id, offset, val) :
        key = bank_id, offset
        #print('set_val[{}:{}:{}] = {}'.format(self.block_id, bank_id, offset, val))
        self.__vals[key] = val

    ### @brief 値を取得する．
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def get_val(self, bank_id, offset) :
        key = bank_id, offset
        #print('get_val[{}:{}:{}] = {}'.format(self.block_id, bank_id, offset, self.__vals[key]))
        return self.__vals[key]


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
        self.__value = None
        self.__next_value = None

    ### @brief ロード条件を追加する．
    def add_cond(self, cstep, bank_id) :
        self.__block.add_cond(cstep, bank_id)

    ### @brief ロードユニットのときに True を返す．
    @property
    def is_load_unit(self) :
        return True

    ### @brief メモリブロックを返す．
    @property
    def block(self) :
        return self.__block

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block.block_id

    ### @brief オフセットを返す．
    @property
    def offset(self) :
        return self.__offset

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'LoadUnit[{}][{}]'.format(self.block_id, self.offset)

    ### @brief バンク選択条件の辞書を返す．
    ###
    ### cstep をキーとしてそのときに選択されて
    ### いるバンク番号を格納している．
    @property
    def bank_dict(self) :
        return self.__block.bank_dict

    ### @brief シミュレーションを行う．
    ### @param[in] step
    def eval_on(self, step) :
        if step in self.__block.bank_dict :
            if debug_out :
                debug_out.write('{}.eval_on({})\n'.format(self.name, step))
            bank_id = self.__block.bank_dict[step]
            val = self.__block.get_val(bank_id, self.offset)
            self.__next_value = val
            if debug_out :
                debug_out.write('  bank = {}\n'.format(bank_id))
                debug_out.write('  next_value = {}\n'.format(self.__next_value))

    ### @brief シミュレーション時刻を進める．
    def sync(self) :
        if self.__next_value is not None :
            self.__value = self.__next_value
            self.__next_value = None
            if debug_out :
                debug_out.write('{}.sync() <= {}\n'.format(self.name, self.value))

    ### @brief シミュレーション結果を返す．
    @property
    def value(self) :
        return self.__value


### @brief ストアユニット
class StoreUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] mem_block ブロック
    def __init__(self, id, mem_block) :
        super().__init__(id, 1)
        self.__block = mem_block
        self.__next_bank_id = None
        self.__next_value = None

    ### @brief ストア条件を追加する．
    def add_src(self, src, cstep, bank_id) :
        super()._add_src(0, src, cstep)
        self.__block.add_cond(cstep, bank_id)

    ### @brief ストアユニットのときに True を返す．
    @property
    def is_store_unit(self) :
        return True

    ### @brief メモリブロックを返す．
    @property
    def block(self) :
        return self.__block

    ### @brief ブロック番号を返す．
    @property
    def block_id(self) :
        return self.__block.block_id

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'StoreUnit[{}]'.format(self.block_id)

    ### @brief バンク選択条件の辞書を返す．
    ###
    ### cstep をキーとしてそのときに選択されて
    ### いるバンク番号を格納している．
    @property
    def bank_dict(self) :
        return self.__block.bank_dict

    ### @brief シミュレーションを行う．
    ### @param[in] step
    def eval_on(self, step) :
        if step in self.bank_dict :
            if debug_out :
                debug_out.write('{}.eval_on({})\n'.format(self.name, step))
            src = self.mux_spec(0).src(step)
            val = src.eval_on(step)
            bank_id = self.bank_dict[step]
            if debug_out :
                debug_out.write('  bank = {}\n'.format(bank_id))
                debug_out.write('  val  = {}\n'.format(val))
            self.__next_bank_id = bank_id
            self.__next_value = val

    ### @brief シミュレーション時刻を進める．
    def sync(self) :
        if self.__next_value is not None :
            self.__block.set_val(self.__next_bank_id, 0, self.__next_value)
            self.__next_bank_id = None
            self.__next_value = None


### @brief THROUGHユニット
class ThroughUnit(Unit) :

    ### @brief 初期化
    def __init__(self, id, src) :
        super().__init__(id, 0)
        self.__src = src

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'THROUGH'

    ### @brief シミュレーションを行う．
    ### @param[in] step
    def eval_on(self, step) :
        return self.__src.value


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
    ### @param[in] src ソース
    ### @param[in] inv 反転する時に True にするフラグ
    def add_src(self, i, src, cstep, inv) :
        super()._add_src(i, src, cstep)
        if inv :
            self.__inv_cond_list[i].append(cstep)

    ### @brief OP1ユニットのときに True を返す．
    @property
    def is_op1_unit(self) :
        return True

    ### @brief 演算器番号を返す．
    @property
    def op_id(self) :
        return self.__op_id

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'OP1[{}]'.format(self.op_id)

    ### @brief 入力の反転条件(コントロールステップ)を返す．
    def inv_cond(self, i) :
        return self.__inv_cond_list[i]

    ### @brief シミュレーションを行う．
    ### @param[in] step
    def eval_on(self, step) :
        if self.node(step) is None :
            return None
        if debug_out :
            debug_out.write("  {}.eval_on({}): DFG's {}\n".format(self.name, step, self.node(step).name))
        val = 0
        for i in range(self.input_num) :
            mux = self.mux_spec(i)
            src = mux.src(step)
            if src is None :
                continue
            if debug_out :
                debug_out.write('   #{}: {}:{}\n'.format(i, src.name, src.value))
            if step in self.__inv_cond_list[i] :
                val += ~src.value
            else :
                val += src.value
        if debug_out :
            debug_out.write('  => {}\n'.format(val))
        return val


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
    ### @param[in] src ソース
    def add_src(self, i, src, cstep) :
        super()._add_src(i, src, cstep)

    ### @brief cstep ごとの bias 値を設定する．
    def add_bias(self, bias, cstep) :
        self.__bias_map[cstep] = bias

    ### @brief OP2ユニットのときに True を返す．
    @property
    def is_op2_unit(self) :
        return True

    ### @brief 演算器番号を返す．
    @property
    def op_id(self) :
        return self.__op_id

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'OP2[{}]'.format(self.op_id)

    ### @brief bias値の辞書を返す．
    @property
    def bias_map(self) :
        return self.__bias_map

    ### @brief シミュレーションを行う．
    ### @param[in] step
    def eval_on(self, step) :
        if self.node(step) is None :
            return None
        assert step in self.__bias_map
        if debug_out :
            debug_out.write('{}.eval_on({})\n'.format(self.name, step))
        val = 0
        for i in range(self.input_num) :
            mux = self.mux_spec(i)
            src = mux.src(step)
            if src is None :
                continue
            if debug_out :
                debug_out.write('    #{}: src = {}: {}\n'.format(i, src.name, src.value))
            assert src.value is not None
            val += src.value
        val += self.__bias_map[step]
        if debug_out :
            debug_out.write('  => {}\n'.format(val))
        return val


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
        self.__cond_map = dict()
        self.__src_map = dict()
        self.__value = None
        self.__next_value = None

    ### @brief ソースの情報を追加する．
    def add_src(self, node) :
        var = node.var
        self.__var_list.append(var)
        if self.__last_step < var.end :
            self.__last_step = var.end
        var.bind(self)
        if node.is_memsrc :
            cstep = node.cstep + 1
        else :
            cstep = node.cstep
        op = node.unit
        if op.id not in self.__cond_map :
            self.__cond_map[op.id] = list()
        self.__cond_map[op.id].append(cstep)
        assert cstep not in self.__src_map
        self.__src_map[cstep] = op

    ### @brief レジスタのときに True を返す．
    @property
    def is_reg_unit(self) :
        return True

    ### @brief レジスタ番号を返す．
    @property
    def reg_id(self) :
        return self.__reg_id

    ### @brief 名前を返す．
    @property
    def name(self) :
        return 'REG[{}]'.format(self.reg_id)

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
        return node.unit.id in self.__cond_map

    ### @brief ソースの条件の辞書を返す．
    ###
    ### キーはユニット番号で値は cstep のリスト
    @property
    def cond_map(self) :
        return self.__cond_map

    ### @brief シミュレーションを行う．
    ### @param[in] step
    def eval_on(self, step) :
        if debug_out :
            debug_out.write('{}.eval_on({})\n'.format(self.name, step))
        if step in self.__src_map :
            src = self.__src_map[step]
            if src.is_load_unit :
                val = src.value
            else :
                val = src.eval_on(step)
            self.__next_value = val
            if debug_out :
                debug_out.write('  src = {}\n'.format(src.name))
                debug_out.write('  {}.next_value <= {}\n'.format(self.name, val))

    ### @brief シミュレーションの終了処理
    def sync(self) :
        if self.__next_value is not None :
            self.__value = self.__next_value
            self.__next_value = None
            if debug_out :
                debug_out.write('{}.sync(). value <= {}\n'.format(self.name, self.value))

    ### @brief シミュレーション結果を返す．
    @property
    def value(self) :
        return self.__value


### @brief 演算器を管理するマネージャ
class UnitMgr :

    ### @brief 初期化
    def __init__(self, imem_layout, omem_layout) :
        self.__imem_layout = imem_layout
        self.__omem_layout = omem_layout
        self.__unit_list = list()
        self.__lm_dict = dict()
        self.__lu_dict = dict()
        self.__lu_list = list()
        self.__sm_dict = dict()
        self.__su_dict = dict()
        self.__su_list = list()
        self.__through_list = list()
        self.__op1_list = list()
        self.__op2_list = list()
        self.__reg_list = list()

    ### @brief 全てのユニットのリストを返す．
    @property
    def unit_list(self) :
        for unit in self.__unit_list :
            yield unit

    ### @brief ユニット番号からユニットを取り出す．
    def unit(self, unit_id) :
        return self.__unit_list[unit_id]

    ### @brief Load Memory のリストを返す．
    @property
    def load_memory_list(self) :
        return self.__lm_dict.values()

    ### @brief block_id から Load Memory を取り出す．
    def load_memory(self, block_id) :
        return self.__lm_dict[block_id]

    ### @brief Load Unit のリストを返す．
    @property
    def load_unit_list(self) :
        for unit in self.__lu_list :
            yield unit

    ### @brief Store Memory のリストを返す．
    @property
    def store_memory_list(self) :
        return self.__sm_dict.values()

    ### @brief block_id から Store Memory を取り出す．
    def store_memory(self, block_id) :
        return self.__sm_dict[block_id]

    ### @brief Store Unit のリストを返す．
    @property
    def store_unit_list(self) :
        for unit in self.__su_list :
            yield unit

    ### @brief OP1 Unit の数を返す．
    @property
    def op1_num(self) :
        return len(self.__op1_list)

    ### @brief OP2 Unit を返す．
    def op1(self, pos) :
        return self.__op1_list[pos]

    ### @brief OP1 Unit のリストを返す．
    @property
    def op1_list(self) :
        for unit in self.__op1_list :
            yield unit

    ### @brief OP2 Unit の数を返す．
    @property
    def op2_num(self) :
        return len(self.__op2_list)

    ### @brief OP2 Unit を返す．
    def op2(self, pos) :
        return self.__op2_list[pos]

    ### @brief OP2 Unit のリストを返す．
    @property
    def op2_list(self) :
        for unit in self.__op2_list :
            yield unit

    ### @brief レジスタの数を返す．
    @property
    def reg_num(self) :
        return len(self.__reg_list)

    ### @brief レジスタを返す．
    def reg(self, pos) :
        return self.__reg_list[pos]

    ### @brief レジスタのリストを返す．
    @property
    def reg_list(self) :
        for reg in self.__reg_list :
            yield reg

    ### @brief Load Unit を作る．
    ### @param[in] block_id ブロック番号
    ### @param[in] offset オフセット
    def new_load_unit(self, block_id, offset) :
        key = block_id, offset
        if key not in self.__lu_dict :
            id = len(self.__unit_list)
            lm = self.new_load_memory(block_id)
            lu = LoadUnit(id, lm, offset)
            self.__unit_list.append(lu)
            self.__lu_dict[key] = lu
            self.__lu_list.append(lu)
        else :
            lu = self.__lu_dict[key]
        return lu

    ### @biref Load Memory を作る．
    ### @param[in] block_id ブロック番号
    def new_load_memory(self, block_id) :
        if block_id not in self.__lm_dict :
            bank_num = self.__imem_layout.bank_num
            bank_size = self.__imem_layout.bank_size
            lm = MemoryBlock(block_id, bank_num, bank_size)
            self.__lm_dict[block_id] = lm
        return self.__lm_dict[block_id]

    ### @brief Store Unit を作る．
    ### @param[in] block_id ブロック番号
    def new_store_unit(self, block_id) :
        if block_id not in self.__su_dict :
            id = len(self.__unit_list)
            sm = self.new_store_memory(block_id)
            su = StoreUnit(id, sm)
            self.__unit_list.append(su)
            self.__su_dict[block_id] = su
            self.__su_list.append(su)
        else :
            su = self.__su_dict[block_id]
        return su

    ### @biref Store Memory を作る．
    ### @param[in] block_id ブロック番号
    def new_store_memory(self, block_id) :
        if block_id not in self.__sm_dict :
            bank_num = self.__omem_layout.bank_num
            sm = MemoryBlock(block_id, bank_num, 1)
            self.__sm_dict[block_id] = sm
        return self.__sm_dict[block_id]

    ### @brief THROUGH Unit を作る．
    def new_through_unit(self, src) :
        id = len(self.__unit_list)
        unit = ThroughUnit(id, src)
        self.__unit_list.append(unit)
        self.__through_list.append(unit)
        return unit

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
    ### @param[in] ivals 入力値
    ### @return 出力値を納めた辞書を返す．
    def simulate(self, ivals, oaddr_list, total_step, debug) :
        global debug_out
        if debug :
            debug_out = sys.stdout
        else :
            debug_out = None

        # 入力値を load memory にセットする．
        for addr, val in ivals.items() :
            block_id, bank_id, offset = self.__imem_layout.decode(addr)
            lm = self.load_memory(block_id)
            lm.set_val(bank_id, offset, val)

        for step in range(total_step) :
            if debug_out :
                debug_out.write('simulate@{}\n'.format(step))
            for unit in self.load_unit_list :
                unit.eval_on(step)

            for unit in self.store_unit_list :
                unit.eval_on(step)

            for unit in self.reg_list :
                unit.eval_on(step)

            if debug_out :
                debug_out.write('sync@{}\n'.format(step))
            for unit in self.load_unit_list :
                unit.sync()

            for unit in self.store_unit_list :
                unit.sync()

            for unit in self.reg_list :
                unit.sync()

        # 出力値を store memory から取り出す．
        ovals = dict()
        for addr in oaddr_list :
            block_id, bank_id, offset = self.__omem_layout.decode(addr)
            sm = self.store_memory(block_id)
            val = sm.get_val(bank_id, offset)
            ovals[addr] = val

        return ovals

    ### @brief 内容を出力する．
    def print(self, fout) :
        # Load Memory の内容を出力する．
        fout.write('Load Memory\n')
        for lm in self.load_memory_list :
            fout.write('{}\n'.format(lm.name))
            for bank_id, cond_list in lm.cond_dict.items() :
                fout.write('  bank#{} @ ('.format(bank_id))
                for cond in cond_list :
                    fout.write(' {}'.format(cond))
                fout.write('\n')
        fout.write('\n')

        # Load Unit の内容を出力する．
        fout.write('Load Unit\n')
        for lu in self.load_unit_list :
            fout.write('{}: = {}[{}]\n'.format(lu.name, lu.block.name, lu.offset))

        # Op1 Unit の内容を出力する．
        fout.write('OP1 Unit\n')
        for op1 in self.op1_list :
            fout.write('{}\n'.format(op1.name))
            for i in range(op1.input_num) :
                first = True
                mux_spec = op1.mux_spec(i)
                for src in mux_spec.src_list :
                    if src == None :
                        continue
                    if first :
                        fout.write('  Input#{}\n'.format(i))
                        first = False
                    fout.write('    {}@ ('.format(src.name))
                    cond_list = mux_spec.src_cond(src)
                    for cond in cond_list :
                        fout.write(' {}'.format(cond))
                    fout.write(')\n')
            fout.write('\n')
        fout.write('\n')

        # Op2 Unit の内容を出力する．
        fout.write('OP2 Unit\n')
        for op2 in self.op2_list :
            fout.write('{}\n'.format(op2.name))
            for i in range(op2.input_num) :
                first = True
                mux_spec = op2.mux_spec(i)
                for src in mux_spec.src_list :
                    if src == None :
                        continue
                    if first :
                        fout.write('  Input#{}\n'.format(i))
                        first = False
                    assert src.is_reg_unit
                    fout.write('    {} @ ('.format(src.name))
                    cond_list = mux_spec.src_cond(src)
                    for cond in cond_list :
                        fout.write(' {}'.format(cond))
                    fout.write(')\n')
            fout.write('  Bias\n')
            for cstep, bias in op2.bias_map.items() :
                fout.write('    {}@{}\n'.format(bias, cstep))
            fout.write('\n')
        fout.write('\n')

        # Store Unit の内容を出力する．
        fout.write('Store Memory\n')
        for sm in self.store_memory_list :
            fout.write('{}\n'.format(sm.name))
            for bank_id, cond_list in sm.cond_dict.items() :
                fout.write('  bank#{}@ ('.format(bank_id))
                for cond in cond_list :
                    fout.write(' {}'.format(cond))
                fout.write(')\n')
        fout.write('\n')

        fout.write('Store Unit\n')
        for su in self.store_unit_list :
            fout.write('{}: {}'.format(su.name, su.block.name))
            mux_spec = su.mux_spec(0)
            for src in mux_spec.src_list :
                if src == None :
                    continue
                fout.write('    {}@ ('.format(src.name))
                cond_list = mux_spec.src_cond(src)
                for cond in cond_list :
                    fout.write(' {}'.format(cond))
                fout.write(')\n')
            fout.write('\n')
        fout.write('\n')

        fout.write('Register Unit\n')
        for reg in self.reg_list :
            fout.write('{}: '.format(reg.name))
            for var in reg.var_list :
                fout.write(' {}'.format(var.name))
            fout.write('\n')
            for unit_id, cstep_list in reg.cond_map.items() :
                src = self.__unit_list[unit_id]
                fout.write('    {}@ ('.format(src.name))
                for cstep in cstep_list :
                    fout.write(' {}'.format(cstep))
                fout.write(')\n')
            fout.write('\n')
