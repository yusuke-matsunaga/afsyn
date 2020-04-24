#! /usr/bin/env python3

### @file read_xlsx.py
### @brief エクセルファイルを読み込む関数
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019, 2020 Yusuke Matsunaga
### All rights reserved.

import openpyxl as px
import sys
import os
from op import Op


### @brief エクセルシートを読み込み演算リストを作る．
def read_xlsx(filename) :
    book = px.load_workbook(filename)
    sheet = book.active

    # A: 出力番号
    # B: 入力番号
    # C: 重み値

    i_min = None
    i_max = None
    o_min = None
    o_max = None
    w_set = set()
    fanin_list = dict()
    fanout_list = dict()
    op_dict = dict()
    for cols in sheet.rows :
        if not isinstance(cols[0].value, int) :
            # 凡例の行はスキップ
            continue
        oid = cols[0].value
        iid = cols[1].value
        w = cols[2].value
        if i_min == None :
            # 初回
            i_min = iid
            i_max = iid
            o_min = oid
            o_max = oid
        else :
            if i_min > iid :
                i_min = iid
            if i_max < iid :
                i_max = iid
            if o_min > oid :
                o_min = oid
            if o_max < oid :
                o_max = oid
        w_set.add(w)
        if iid in fanout_list :
            fanout_list[iid].append(oid)
        else :
            fanout_list[iid] = [oid]
        if oid in fanin_list :
            fanin_list[oid].append(iid)
        else :
            fanin_list[oid] = [iid]

        if oid in op_dict :
            op = op_dict[oid]
        else :
            op = Op(oid)
            op_dict[oid] = op
        op.add_fanin(iid, w)

    #assert i_min == 0
    #assert o_min == 0
    print('# i_min = {}'.format(i_min))
    print('# i_max = {}'.format(i_max))
    print('# o_min = {}'.format(o_min))
    print('# o_max = {}'.format(o_max))
    print('# weights =', end = '')
    for w in sorted(w_set) :
        print(' {}'.format(w), end = '')
    print()

    op_list = [ op_dict[oid] for oid in range(o_max + 1) ]

    return op_list


if __name__ == '__main__' :
    # テストプログラム
    # エクセルファイルを読み込んで標準出力に dump() する．
    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    op_list = read_xlsx(filename)

    for op in op_list :
        op.dump(sys.stdout)
