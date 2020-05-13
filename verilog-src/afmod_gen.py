#! /usr/bin/env python3

### @file afmod_gen.py
### @brief
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

for i in range(12) :
    print('                 .imem{0:02d}_bank(imem{0:02d}_bank),'.format(i))
    print('                 .imem{0:02d}_rd(imem{0:02d}_rd),'.format(i))
    print('                 .imem{0:02d}_in(imem{0:02d}_in),'.format(i))
for i in range(8) :
    print('                 .omem{0:02d}_bank(omem{0:02d}_bank),'.format(i))
    print('                 .omem{0:02d}_wr(omem{0:02d}_wr),'.format(i))
    print('                 .omem{0:02d}_out(omem{0:02d}_out),'.format(i))
