#! /usr/bin/env python3

### @file op.py
### @brief
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019 Yusuke Matsunaga
### All rights reserved.


import re
import sys
import os

### @brief 演算子を表すクラス
class Op :

    ### @brief 初期化
    ### @param[in] id 番号
    def __init__(self, id) :
        self.__id = id
        self.__fanin_list = []
        self.__double_num = 0
        self.__negative = False

    ### @brief 番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief ファンイン番号のリストを返す．
    @property
    def fanin_list(self) :
        return self.__fanin_list

    ### @brief 必要なブロック数を計算する．
    @property
    def block_size(self) :
        size = len(self.__fanin_list)
        size += self.__double_num
        if self.__negative :
            size += 1
        return size // 16

    ### @brief ファンインを追加する．
    ### @param[in] i_id ファンイン番号
    ### @param[in] w 重み
    def add_fanin(self, i_id, w) :
        if w == 0.125 :
            i_type = 0
        elif w == 0.25 :
            i_type = 1
            self.__double_num += 1
        elif w == -0.125 :
            i_type = 2
            self.__negative = True
        else :
            assert False
        self.__fanin_list.append( (i_id, w) )

    ### @brief 内容をダンプする．
    def dump(self, fout) :
        print('{}:'.format(self.__id), file = fout, end = '')
        comma = ''
        for i_id, w in self.__fanin_list :
            print('{} ({}, {})'.format(comma, i_id, w), file = fout, end = '')
            comma = ','
        print('', file = fout)


### @brief dump したファイルを読み込む．
def read_op(fin) :
    pID = re.compile(R'(\d*):')
    pBODY = re.compile(R'\s*\((\d*), (-?\d*.\d*)\)')
    pCOMMA = re.compile(R',')
    op_list = list()
    while True :
        line = fin.readline()
        if line == '' :
            # EOF
            break

        line = line.rstrip()
        if line == '' :
            continue

        m = pID.match(line)
        assert m is not None
        id = int(m.group(1))
        op = Op(id)
        start = m.end(0)
        while True :
            m = pBODY.match(line, start)
            assert m is not None
            i_id = int(m.group(1))
            w = float(m.group(2))
            op.add_fanin(i_id, w)
            start = m.end(0)
            m = pCOMMA.match(line, start)
            if not m :
                break
            start = m.end(0)
        op_list.append(op)
    return op_list


if __name__ == '__main__' :
    # テストプログラム
    # dump ファイルを読み込んで標準出力に再び dump する．
    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    with open(filename, 'rt') as fin :
        op_list = read_op(fin)

        for op in op_list :
            op.dump(sys.stdout)

        fanin_deg = dict()
        total_fanin = 0
        for op in op_list :
            d = len(op.fanin_list)
            if d in fanin_deg :
                fanin_deg[d] += 1
            else :
                fanin_deg[d] = 1
            total_fanin += d

        #for d in sorted(fanin_deg.keys()) :
        #    print('{}, {}'.format(d, fanin_deg[d]))
        print('total fanin: {}'.format(total_fanin))
        ave = total_fanin / len(op_list)
        print('ave: {}'.format(ave))
