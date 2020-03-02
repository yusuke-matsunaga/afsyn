#! /usr/bin/env python3

### @file mem_layout.py
### @brief MemLayout の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


### @brief メモリブロックの管理を行うクラス
class MemLayout :

    ### @brief 初期化
    ### @param[in] memory_size トータルのメモリサイズ
    ### @param[in] block_num ブロック数
    ### @param[in] bank_size バンクサイズ
    ### @param[in] method メソッド
    def __init__(self, memory_size, block_num, bank_size, method = 1) :
        self.__memory_size = memory_size
        self.__block_num = block_num
        self.__block_size = (memory_size + block_num - 1) // block_num
        self.__bank_size = bank_size
        self.__method = method
        if self.__method == 2 :
            self.__slice_size = self.__bank_size * self.__block_num
        #print('memory_size = {}'.format(self.__memory_size))
        #print('block_num   = {}'.format(self.__block_num))
        #print('block_size  = {}'.format(self.__block_size))
        #print('bank_size   = {}'.format(self.__bank_size))

    ### @brief ブロック番号を返す．
    ### @param[in] i_id アドレス
    def block_id(self, i_id) :
        if self.__method == 1 :
            return i_id // self.__block_size
        elif self.__method == 2 :
            return (i_id % self.__slice_size) // self.__bank_size
        else :
            assert False

    ### @brief バンク番号を返す．
    ### @param[in] i_id アドレス
    def bank_id(self, i_id) :
        if self.__method == 1 :
            return (i_id % self.__block_size) // self.__bank_size
        elif self.__method == 2 :
            return i_id // self.__slice_size
        else :
            assert False

    ### @brief バンク内オフセットを返す．
    ### @param[in] i_id アドレス
    def offset(self, i_id) :
        if self.__method == 1 :
            return i_id % self.__bank_size
        elif self.__method == 2 :
            return i_id % self.__bank_size
        else :
            assert False


if __name__ == '__main__' :
    import sys
    import os

    memory_size = 1500
    for block_num, bank_size in ((24, 16), (24, 32), (12, 16), (12, 32), (6, 16), (6, 32)) :
        print()
        print('Block Num: {}'.format(block_num))
        print('Bank Size: {}'.format(bank_size))
        for method in (1, 2) :
            mem_layout = MemLayout(memory_size, block_num, bank_size, method)
            print('Method: {}'.format(method))
            for addr in range(1500) :
                print('{:04d}: ({}, {}, {})'.format(addr, mem_layout.block_id(addr), mem_layout.bank_id(addr), mem_layout.offset(addr)))
