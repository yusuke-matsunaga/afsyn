#! /usr/bin/env python3

### @file codegen.py
### @brief Verilog-HDL 記述を出力するクラス
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

class CodeGen :

    ### @brief 初期化
    def __init__(self, fout) :
        self.__fout = fout

    ### @brief コード出力
    def generate(self, unit_mgr, module_name, op1_module_name, op2_module_name) :
        io_list = [
            'input clock',
            'input reset',
            'input start',
            'output busy',
            ]

        # 入力用メモリの諸元
        iblock_num = unit_mgr.imem_layout.block_num
        ibank_num = unit_mgr.imem_layout.bank_num
        ibank_bw = 0
        while (1 << ibank_bw) < ibank_num :
            ibank_bw += 1
        ibank_size = unit_mgr.imem_layout.bank_size

        # imem の i 番目のバンク選択信号線名
        imem_bank_name_list = [ 'imem{:02d}_bank'.format(i) for i in range(iblock_num) ]

        # imem の i 番目の読み出し制御信号
        imem_rd_name_list = [ 'imem{:02d}_rd'.format(i) for i in range(iblock_num) ]

        # imem の i 番目の出力ポート
        imem_in_name_list = [ 'imem{:02d}_in'.format(i) for i in range(iblock_num) ]
        for i in range(iblock_num) :
            if ibank_bw > 0 :
                io_list.append('output [{}:0] {}'.format(ibank_bw - 1, imem_bank_name_list[i]))
            io_list.append('output {}'.format(imem_rd_name_list[i]))
            io_list.append('input [255:0] {}'.format(imem_in_name_list[i]))

        # 出力用メモリの諸元
        oblock_num = unit_mgr.omem_layout.block_num
        obank_num = unit_mgr.omem_layout.bank_num
        obank_bw = 0
        while (1 << obank_bw) < obank_num :
            obank_bw += 1
        obank_size = unit_mgr.omem_layout.bank_size

        # omem の i 番目のバンク選択信号線名
        omem_bank_name_list = [ 'omem{:02d}_bank'.format(i) for i in range(oblock_num) ]

        # omem の i 番目の書込み制御信号
        omem_wr_name_list = [ 'omem{:02d}_wr'.format(i) for i in range(oblock_num) ]

        # omem の i 番目の入力ポート
        omem_out_name_list = [ 'omem{:02d}_out'.format(i) for i in range(oblock_num) ]
        for i in range(oblock_num) :
            if obank_bw > 0 :
                io_list.append('output [{}:0] {}'.format(obank_bw - 1, omem_bank_name_list[i]))
            io_list.append('output {}'.format(omem_wr_name_list[i]))
            io_list.append('output [7:0] {}'.format(omem_out_name_list[i]))

        # モジュールの開始
        self.__begin_module(module_name, io_list)

        # unit との対応付け
        src_name_dict = dict()

        # 入力メモリ用の信号線名の登録
        for lu in unit_mgr.load_unit_list :
            block_id = lu.block_id
            offset = lu.offset
            msb = offset * 8 + 7
            lsb = offset * 8
            in_name = '{}[{}:{}]'.format(imem_in_name_list[block_id], msb, lsb)
            src_name_dict[lu.id] = in_name

        # OP1 モジュールのインスタンス宣言
        nop1 = unit_mgr.op1_num
        # i 番目の OP1 のインスタンス名
        op1_name_list = list()
        # i 番目の OP1 の j 番目の入力信号線
        op1_in_name_list = list()
        # i 番目の OP1 の j 番目の入力反転制御信号線
        op1_inv_name_list = list()

        for i in range(nop1) :
            op1 = unit_mgr.op1(i)
            self.__fout.write('\n')
            self.__fout.write('  // {} 番目の OP1\n'.format(i))
            in_name_list = list()
            inv_name_list = list()
            for j in range(op1.input_num) :
                in_name = 'op1_{:02d}_in{:02d}'.format(i, j)
                in_name_list.append(in_name)
                inv_name = 'op1_{:02d}_inv{:02d}'.format(i, j)
                inv_name_list.append(inv_name)
                self.__fout.write('  reg [7:0] {};\n'.format(in_name))
                self.__fout.write('  reg       {};\n'.format(inv_name))
            op1_in_name_list.append(in_name_list)
            op1_inv_name_list.append(inv_name_list)
            out_name = 'op1_{:02d}_out'.format(i)
            self.__fout.write('  wire [11:0] {};\n'.format(out_name))
            op1_name = 'op1_{:02d}'.format(i)
            op1_name_list.append(op1_name)
            self.__fout.write('  {} {}(\n'.format(op1_module_name, op1_name))
            for j in range(op1.input_num) :
                self.__fout.write('    .data{}_in({}),\n'.format(j, op1_in_name_list[i][j]))
                self.__fout.write('    .inv{}_in({}),\n'.format(j, op1_inv_name_list[i][j]))
            self.__fout.write('    .data_out({}));\n'.format(out_name))
            src_name_dict[op1.id] = out_name

        # OP2 モジュールのインスタンス宣言
        nop2 = unit_mgr.op2_num
        # i 番目の OP2 のインスタンス名
        op2_name_list = list()
        # i 番目の OP2 の j 番目の入力信号線
        op2_in_name_list = list()
        # i 番目の OP2 のバイアス信号線
        op2_bias_name_list = list()

        for i in range(nop2) :
            op2 = unit_mgr.op2(i)
            self.__fout.write('\n')
            self.__fout.write('  // {} 番目の OP2\n'.format(i))
            in_name_list = list()
            for j in range(op2.input_num) :
                in_name = 'op2_{:02d}_in{:02d}'.format(i, j)
                in_name_list.append(in_name)
                self.__fout.write('  reg [11:0] {};\n'.format(in_name))
            op2_in_name_list.append(in_name_list)
            bias_name = 'op2_{:02d}_bias'.format(i)
            op2_bias_name_list.append(bias_name)
            self.__fout.write('  reg [11:0] {};\n'.format(bias_name))
            out_name = 'op2_{:02d}_out'.format(i)
            self.__fout.write('  wire [11:0] {};\n'.format(out_name))
            op2_name = 'op2_{:02d}'.format(i)
            op2_name_list.append(op2_name)
            self.__fout.write('  {} {}(\n'.format(op2_module_name, op2_name))
            for j in range(op2.input_num) :
                self.__fout.write('    .data{}_in({}),\n'.format(j, op2_in_name_list[i][j]))
            self.__fout.write('    .data{}_in({}),\n'.format(op2.input_num, bias_name))
            self.__fout.write('    .data_out({}));\n'.format(out_name))
            src_name_dict[op2.id] = out_name

        # レジスタの宣言
        nreg = unit_mgr.reg_num
        # i 番目のレジスタ名
        reg_name_list = [ ]
        self.__fout.write('\n')
        self.__fout.write('  // 中間レジスタ\n')
        for i in range(nreg) :
            reg_name = 'reg_{:04d}'.format(i)
            reg_name_list.append(reg_name)
            self.__fout.write('  reg [11:0] {};\n'.format(reg_name))
            reg = unit_mgr.reg(i)
            src_name_dict[reg.id] = reg_name

        # 制御マシンの状態
        nstep = unit_mgr.total_step
        state_bw = 0
        while (1 << state_bw) < nstep :
            state_bw += 1
        self.__fout.write('\n')
        self.__fout.write('  // 制御マシンの状態\n')
        self.__fout.write('  reg [{}:0] state;\n'.format(state_bw - 1))
        self.__fout.write('  reg _busy;\n')
        self.__fout.write('  assign busy = _busy;\n')
        self.__fout.write('  // 制御マシンの動作\n')
        self.__fout.write('  always @ ( posedge clock or negedge reset ) begin\n')
        self.__fout.write('    if ( !reset ) begin\n')
        self.__fout.write('      _busy <= 0;\n')
        self.__fout.write('      state <= 0;\n')
        self.__fout.write('    end\n')
        self.__fout.write('    else if ( _busy ) begin\n')
        self.__fout.write('      if ( state < {} ) begin\n'.format(nstep - 1))
        self.__fout.write('        state <= state + 1;\n')
        self.__fout.write('      end\n')
        self.__fout.write('      else begin\n')
        self.__fout.write('        _busy <= 0;\n')
        self.__fout.write('        state <= 0;\n')
        self.__fout.write('      end\n')
        self.__fout.write('    end\n')
        self.__fout.write('    else if ( start ) begin\n')
        self.__fout.write('      _busy <= 1;\n')
        self.__fout.write('    end\n')
        self.__fout.write('  end\n')

        # 入力用メモリの制御
        for lm in unit_mgr.load_memory_list :
            bank_name = imem_bank_name_list[lm.block_id]
            tmp_name = '_{}'.format(bank_name)
            self.__fout.write('\n')
            self.__fout.write('  // {}番目の入力用メモリブロックの制御\n'.format(lm.block_id))
            self.__fout.write('  reg [{}:0] {};\n'.format((ibank_bw - 1), tmp_name))
            src_dict = dict()
            for step, bank in lm.bank_dict.items() :
                src_dict[step] = bank
            self.__gen_control(tmp_name, src_dict, 0)
            self.__fout.write('  assign {} = {};\n'.format(bank_name, tmp_name))

            rd_name = imem_rd_name_list[lm.block_id]
            tmp_name = '_{}'.format(rd_name)
            self.__fout.write('  reg {};\n'.format(tmp_name))
            src_dict = dict()
            for step, bank in lm.bank_dict.items() :
                src_dict[step] = 1
            self.__gen_control(tmp_name, src_dict, 0)
            self.__fout.write('  assign {} = {};\n'.format(rd_name, tmp_name))

        # 出力用メモリの制御
        for sm in unit_mgr.store_memory_list :
            bank_name = omem_bank_name_list[sm.block_id]
            tmp_name = '_{}'.format(bank_name)
            self.__fout.write('\n')
            self.__fout.write('  // {}番目の出力用メモリブロックの制御\n'.format(sm.block_id))
            self.__fout.write('  reg [{}:0] {};\n'.format((obank_bw - 1), tmp_name))
            src_dict = dict()
            for step, bank in sm.bank_dict.items() :
                src_dict[step] = bank
            self.__gen_control(tmp_name, src_dict, 0)
            self.__fout.write('  assign {} = {};\n'.format(bank_name, tmp_name))

            wr_name = omem_wr_name_list[sm.block_id]
            tmp_name = '_{}'.format(wr_name)
            self.__fout.write('  reg {};\n'.format(tmp_name))
            src_dict = dict()
            for step, bank in sm.bank_dict.items() :
                src_dict[step] = 1
            self.__gen_control(tmp_name, src_dict, 0)
            self.__fout.write('  assign {} = {};\n'.format(wr_name, tmp_name))

        for su in unit_mgr.store_unit_list :
            sm = su.block
            out_name = omem_out_name_list[sm.block_id]
            tmp_name = '_{}'.format(out_name)
            self.__fout.write('  reg [11:0] {};\n'.format(tmp_name))
            src_dict = dict()
            mux = su.mux_spec(0)
            for src in mux.src_list :
                for step in mux.src_cond(src) :
                    if src.name == 'THROUGH' :
                        src_name = src_name_dict[src.src.id]
                    else :
                        src_name = src_name_dict[src.id]
                    src_dict[step] = src_name
            self.__gen_control(tmp_name, src_dict, 0)
            self.__fout.write('  assign {} = {}[7:0];\n'.format(out_name, tmp_name))

        # OP1 の制御
        for op_id in range(nop1) :
            op1 = unit_mgr.op1(op_id)
            for i in range(op1.input_num) :
                self.__fout.write('\n')
                self.__fout.write('  // OP1#{}の{}番目の入力\n'.format(op_id, i))
                mux = op1.mux_spec(i)
                in_name = op1_in_name_list[op_id][i]
                src_dict = dict()
                for src in mux.src_list :
                    for step in mux.src_cond(src) :
                        src_name = src_name_dict[src.id]
                        src_dict[step] = src_name
                self.__gen_control(in_name, src_dict, 0);

                self.__fout.write('\n')
                self.__fout.write('  // OP1#{}の{}番目の入力反転\n'.format(op_id, i))
                inv_name = op1_inv_name_list[op_id][i]
                src_dict = dict()
                for step in op1.inv_cond(i) :
                    src_dict[step] = 1
                self.__gen_control(inv_name, src_dict, 0)

        # OP2 の制御
        for op2 in unit_mgr.op2_list :
            for i in range(op2.input_num) :
                self.__fout.write('\n')
                self.__fout.write('  // OP2#{}の{}番目の入力\n'.format(op2.op_id, i))
                mux = op2.mux_spec(i)
                in_name = op2_in_name_list[op2.op_id][i]
                src_dict = dict()
                for src in mux.src_list :
                    for step in mux.src_cond(src) :
                        src_name = src_name_dict[src.id]
                        src_dict[step] = src_name
                self.__gen_control(in_name, src_dict, 0)

            self.__fout.write('\n')
            self.__fout.write('  // OP2#{}のバイアス入力\n'.format(op2.op_id))
            bias_name = op2_bias_name_list[op2.op_id]
            src_dict = dict()
            for step, bias in op2.bias_map.items() :
                src_dict[step] = bias
            self.__gen_control(bias_name, src_dict, 0)

        # レジスタの制御
        for reg in unit_mgr.reg_list :
            self.__fout.write('\n')
            self.__fout.write('  // REG#{}の入力\n'.format(reg.reg_id))
            self.__fout.write('  always @ ( posedge clock ) begin\n')
            self.__fout.write('    case ( state )\n')
            reg_name = src_name_dict[reg.id]
            for step, src in reg.src_map.items() :
                src_name = src_name_dict[src.id]
                self.__fout.write('    {}: {} <= {};\n'.format(step, reg_name, src_name))
            self.__fout.write('    endcase\n')
            self.__fout.write('  end\n')

        # モジュールの終了
        self.__end_module()

    ### @brief テストベンチの生成を行う．
    def gen_testbench(self, unit_mgr) :
        self.__begin_module('affine_test', list())

        self.__fout.write('  // クロック周期(ns)\n')
        self.__fout.write('  integer clock_length = 100;\n')
        self.__fout.write('\n')
        self.__fout.write('  // クロックエッジからのマージン\n')
        self.__fout.write('  integer clock_margin = 10;\n')
        self.__fout.write('\n')
        self.__fout.write('  reg clock;\n')
        self.__fout.write('  reg reset;\n')
        self.__fout.write('  reg start;\n')
        self.__fout.write('  wire busy;\n')

        # 入力用メモリの諸元
        iblock_num = unit_mgr.imem_layout.block_num
        ibank_num = unit_mgr.imem_layout.bank_num
        ibank_bw = 0
        while (1 << ibank_bw) < ibank_num :
            ibank_bw += 1
        ibank_size = unit_mgr.imem_layout.bank_size

        # affine モジュールのインスタンス
        for i in range(iblock_num) :
            self.__fout.write('  wire [{}:0] {};\n'.format(ibank_bw - 1, imem_bank_name_list[i]))
            self.__fout.write('  wire [7:0] {};\n'.format(imem_in_name_list[i][j]))

        self.__end_module()


    ### @brief モジュールの先頭
    def __begin_module(self, module_name, io_list) :
        self.__fout.write('module {}('.format(module_name))
        nio = len(io_list)
        if nio > 0 :
            self.__fout.write('\n')
            for i, io in enumerate(io_list) :
                self.__fout.write('  {}'.format(io))
                if i < nio - 1 :
                    self.__fout.write(',\n')
        self.__fout.write(');\n')
        self.__fout.write('\n')


    ### @brief モジュールの終了
    def __end_module(self) :
        self.__fout.write('endmodule\n')

    ### @brief step をパラメータにした組み合わせ回路記述
    def __gen_control(self, target_name, src_dict, default) :
        self.__fout.write('  always @ ( * ) begin\n')
        self.__fout.write('    case ( state )\n')
        for step, src_name in src_dict.items() :
            self.__fout.write('    {}: {} = {};\n'.format(step, target_name, src_name))
        if default is not None :
            self.__fout.write('    default: {} = {};\n'.format(target_name, default))
        self.__fout.write('    endcase\n')
        self.__fout.write('  end // always @ ( * )\n')


if __name__ == '__main__' :
    import sys
    import os
    import random
    import argparse
    from op import Op
    from scheduling import scheduling
    from mem_layout import MemLayout
    from binder import bind

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type = int, default = 1000)
    parser.add_argument('file', type = argparse.FileType('rt'))

    args = parser.parse_args()
    if not args :
        exit(1)

    op_list = Op.read(args.file)
    if op_list is None :
        print('read failed.')
        exit(1)

    # メモリサイズの計算
    mem_size = 0
    for op in op_list :
        for i_id, w in op.fanin_list :
            if mem_size < i_id :
                mem_size = i_id
    mem_size += 1

    #block_num = 24
    block_num = 12
    bank_size = 32
    #print('Block num: {}'.format(block_num))
    #print('Bank Size: {}'.format(bank_size))

    bsize = block_num * bank_size
    imemory_size = ((mem_size + bsize - 1) // bsize) * bsize
    imem_layout = MemLayout(imemory_size, block_num, bank_size)
    omemory_size = len(op_list)
    oblock_num = 8
    obank_size = 1
    omem_layout = MemLayout(omemory_size, oblock_num, obank_size)
    oaddr_list = [ i for i in range(omemory_size) ]

    op_limit = 16
    s_method = 2
    dfg = scheduling(op_list, op_limit, imem_layout, omem_layout, s_method)
    #dfg.print()
    unit_mgr = bind(dfg)
    #unit_mgr.print(sys.stdout)

    codegen = CodeGen(sys.stdout)
    module_name = 'affine'
    codegen.generate(unit_mgr, module_name)
