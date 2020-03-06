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
        if src_id not in self.__src_dict :
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

    ### @brief 一つのcstepに関する入力を設定する．
    ### @param[in] i 入力番号
    ### @param[in] src_id ソースのレジスタ番号
    ### @param[in] cstep コントロールステップ
    def add_src(self, i, src_id, cstep) :
        self.__mux_spec[i].add_src(src_id, cstep)

    ### @brief 入力数を返す．
    @property
    def input_num(self) :
        return self.__input_num

    ### @brief 入力のセレクタ情報を返す．
    ### @param[in] i 入力番号
    def mux_spec(self, i) :
        return self.__mux_spec[i]

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
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def __init__(self, id, block_id, bank_id, offset) :
        super().__init__(id, 0)
        self.__block_id = block_id
        self.__bank_id = bank_id
        self.__offset = offset

    ### @brief ロードユニットのときに True を返す．
    def is_load_unit(self) :
        return True

    ### @brief ブロック番号を返す．
    def block_id(self) :
        return self.__block_id

    ### @brief バンク番号を返す．
    def bank_id(self) :
        return self.__bank_id

    ### @brief オフセットを返す．
    def offset(self) :
        return self.__offset


### @brief ストアユニット
class StoreUnit(Unit) :

    ### @brief 初期化
    ### @param[in] id 演算器番号
    ### @param[in] block_id ブロック番号
    ### @param[in] bank_id バンク番号
    ### @param[in] offset オフセット
    def __init__(self, id, block_id, bank_id, offset) :
        super().__init__(id, 1)
        self.__block_id = block_id
        self.__bank_id = bank_id
        self.__offset = offset

    ### @brief ストアユニットのときに True を返す．
    def is_store_unit(self) :
        return True

    ### @brief ブロック番号を返す．
    def block_id(self) :
        return self.__block_id

    ### @brief バンク番号を返す．
    def bank_id(self) :
        return self.__bank_id

    ### @brief オフセットを返す．
    def offset(self) :
        return self.__offset


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
    ### @param[in] id レジスタ番号
    def __init__(self, id) :
        super().__init__(id, 1)

    ### @brief レジスタのときに True を返す．
    def is_reg_unit(self) :
        return True
