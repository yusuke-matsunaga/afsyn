#! /usr/bin/env python3

### @file op.py
### @brief Op クラスの定義を行う
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019, 2020 Yusuke Matsunaga
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

    ### @brief 番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief ファンイン番号と重みのリストを返す．
    @property
    def fanin_list(self) :
        return self.__fanin_list

    ### @brief ファンインを追加する．
    ### @param[in] i_id ファンイン番号
    ### @param[in] w 重み
    def add_fanin(self, i_id, w) :
        self.__fanin_list.append( (i_id, w) )

    ### @brief 値の計算を行う．
    ### @param[in] ivals 入力の値のリスト
    ###
    ### ivals は ivals[x] で値が取得できればなんでもよい．
    def eval(self, ivals) :
        ans = 0
        for i_id, w in self.fanin_list :
            ival = ivals[i_id]
            ans += ival * w
        return ans

    ### @brief 内容をダンプする．
    def dump(self, fout) :
        fout.write('{}:'.format(self.__id))
        comma = ''
        for i_id, w in self.__fanin_list :
            fout.write('{} ({}, {})'.format(comma, i_id, w))
            comma = ','
        fout.write('\n')


    ### @brief dump したファイルを読み込む．
    ### @param[in] fin 入力のファイルオブジェクト
    ### @return Op のリストを返す．
    @staticmethod
    def read(fin) :
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

            if line[0] == '#' :
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
        op_list = Op.read(fin)

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
