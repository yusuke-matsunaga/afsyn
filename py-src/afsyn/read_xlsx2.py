#! /usr/bin/env python3

### @file read_xlsx.py
### @brief エクセルファイルを読み込む関数
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2019, 2020 Yusuke Matsunaga
### All rights reserved.

import openpyxl as px


### @brief エクセルシートを読み込み演算リストを作る．
def read_xlsx2(filename) :
    book = px.load_workbook(filename)
    sheet = book.active

    # A: 入力番号
    # B: 重み値

    i_min = None
    i_max = None
    o_min = None
    o_max = None
    w_set = set()
    fanin_list = list()
    op = Op(0)
    for cols in sheet.rows :
        if not isinstance(cols[0].value, int) :
            # 凡例の行はスキップ
            continue
        iid = cols[0].value
        w = cols[1].value
        if i_min == None :
            # 初回
            i_min = iid
            i_max = iid
        else :
            if i_min > iid :
                i_min = iid
            if i_max < iid :
                i_max = iid
        w_set.add(w)
        fanin_list.append(iid)
        op.add_fanin(iid, w)

    #assert i_min == 0
    print('# i_min = {}'.format(i_min))
    print('# i_max = {}'.format(i_max))
    print('# weights =', end = '')
    for w in sorted(w_set) :
        print(' {}'.format(w), end = '')
    print()

    op_list = [ op ]

    return op_list


if __name__ == '__main__' :
    import sys
    import os

    # テストプログラム
    # エクセルファイルを読み込んで標準出力に dump() する．
    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    op_list = read_xlsx(filename)

    for op in op_list :
        op.dump(sys.stdout)
