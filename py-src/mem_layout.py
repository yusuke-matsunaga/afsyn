#! /usr/bin/env python3

### @file mem_layout.py
### @brief MemLayout の実装ファイル
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


### @brief メモリブロックの管理を行うクラス
###
### method = 1 の時，最初のブロックに 0 〜 (block_size - 1)
### の内容が入る．
### method = 2 の時，最初のブロックのバンク1に 0 〜 (bank_size - 1)
### の内容が入り，2番めのブロックのバンク1に bank_size 〜 (bank_size * 2 - 1)
### の内容が入る．
class MemLayout :

    ### @brief 初期化
    ### @param[in] memory_size トータルのメモリサイズ
    ### @param[in] block_num ブロック数
    ### @param[in] block_size ブロックサイズ
    ### @param[in] bank_size バンクサイズ
    ### @param[in] method メソッド
    def __init__(self, memory_size, block_num, block_size, bank_size, method = 1) :
        self.__memory_size = memory_size
        self.__block_num = block_num
        self.__block_size = block_size
        self.__bank_num = (block_size + bank_size - 1) // bank_size
        self.__bank_size = bank_size

        self.__method = method
        if self.__method == 2 :
            self.__slice_size = self.__bank_size * self.__block_num
        debug = False
        if debug :
            print('memory_size = {}'.format(self.__memory_size))
            print('block_num   = {}'.format(self.__block_num))
            print('block_size  = {}'.format(self.__block_size))
            print('bank_num    = {}'.format(self.__bank_num))
            print('bank_size   = {}'.format(self.__bank_size))

    ### @brief メモリサイズを返す．
    @property
    def memory_size(self) :
        return self.__memory_size

    ### @brief ブロック数を返す．
    @property
    def block_num(self) :
        return self.__block_num

    ### @brief ブロックサイズを返す．
    @property
    def block_size(self) :
        return self.__block_size

    ### @brief バンク数を返す．
    @property
    def bank_num(self) :
        return self.__bank_num

    ### @brief バンクサイズを返す．
    @property
    def bank_size(self) :
        return self.__bank_size

    ### @brief メソッドを返す．
    @property
    def method(self) :
        return self.__method

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
            return (i_id % self.__block_size) % self.__bank_size
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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--memory_size', type = int, required = True)
    parser.add_argument('-n', '--block_num', type = int, required = True)
    parser.add_argument('-b', '--block_size', type = int, required = True)
    parser.add_argument('-c', '--bank_size', type = int, required = True)
    parser.add_argument('-t', '--method', type = int, required = True)


    args = parser.parse_args()
    if not args :
        exit(1)

    memory_size = args.memory_size
    block_num = args.block_num
    block_size = args.block_size
    bank_size = args.bank_size
    method = args.method

    print('block_size = {}'.format(block_size))

    mem_layout = MemLayout(memory_size, block_num, block_size, bank_size, method)

    print('Memory Size: {}'.format(mem_layout.memory_size))
    print('Block Num:   {}'.format(mem_layout.block_num))
    print('Block Size:  {}'.format(mem_layout.block_size))
    print('Bank Num:    {}'.format(mem_layout.bank_num))
    print('Bank Size:   {}'.format(mem_layout.bank_size))
    print('Method:      {}'.format(mem_layout.method))

    for addr in range(mem_layout.memory_size) :
        print('{:04d}: ({}, {}, {})'.format(addr, mem_layout.block_id(addr), mem_layout.bank_id(addr), mem_layout.offset(addr)))
        block_id, bank_id, offset = mem_layout.decode(addr)
        addr1 = mem_layout.encode(block_id, bank_id, offset)
        if addr1 != addr :
            print('Error: addr1 = {}'.format(addr1))
            assert addr == addr1
