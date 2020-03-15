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
        self.__bank_size = bank_size
        block_size = (memory_size + block_num - 1) // block_num
        # block_size は bank_size の倍数にする．
        self.__block_size = ((block_size + bank_size - 1) // bank_size) * bank_size
        self.__method = method
        if self.__method == 2 :
            self.__slice_size = self.__bank_size * self.__block_num
        debug = False
        if debug :
            print('memory_size = {}'.format(self.__memory_size))
            print('block_num   = {}'.format(self.__block_num))
            print('block_size  = {}'.format(self.__block_size))
            print('bank_size   = {}'.format(self.__bank_size))

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

    ### @brief 番地からブロック番号，バンク番号，オフセットを返す．
    def decode(self, addr) :
        return self.block_id(addr), self.bank_id(addr), self.offset(addr)

    ### @brief ブロック番号，バンク番号，オフセットから番地を返す．
    def encode(self, block_id, bank_id, offset) :
        if self.__method == 1 :
            return block_id * self.__block_size + bank_id * self.__bank_size + offset
        elif self.__method == 2:
            return block_id * self.__bank_size + bank_id * self.__slice_size + offset
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
                block_id, bank_id, offset = mem_layout.decode(addr)
                addr1 = mem_layout.encode(block_id, bank_id, offset)
                if addr1 != addr :
                    print('Error: addr1 = {}'.format(addr1))
                assert addr == addr1
