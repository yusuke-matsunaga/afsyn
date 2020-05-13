#! /usr/bin/env python3

### @file imem_gen.py
### @brief
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

for i in range(8) :
    print('   // {} 番目の出力用メモリブロック'.format(i))
    print('   wire [6:0] omem{:02d}_bank;'.format(i))
    print('   wire       omem{:02d}_rd;'.format(i))
    print('   wire       omem{:02d}_wr;'.format(i))
    print('   wire [7:0] omem{:02d}_in;'.format(i))
    print('   wire [7:0] omem{:02d}_out;'.format(i))
    print('   omem omem{:02d}(.clock(clock)'.format(i))
    print('               .bank(omem{:02d}_bank),'.format(i))
    print('               .rd(omem{:02d}_rd),'.format(i))
    print('               .wr(omem{:02d}_wr),'.format(i))
    print('               .in(omem{:02d}_in),'.format(i))
    print('               .out(omem{:02d}_out));'.format(i))
    print()
