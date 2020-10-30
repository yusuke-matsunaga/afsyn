#! /usr/bin/env python3

### @file scheduling.py
### @brief スケジューリングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

import random


def mem_scheduling(node, step, mem_usage) :
    mem_undo_list = []
    schedule_undo_list = []
    for inode in node.fanin_list :
        assert inode.is_memsrc
        block_id = inode.block_id
        bank_id = inode.bank_id
        for istep in range(step - inode.latency, -1, -1) :
            if (block_id, istep) in mem_usage :
                if mem_usage[(block_id, istep)] != bank_id :
                    # 他のバンクが使っている．
                    pass
                else :
                    # OK
                    break
            else :
                mem_usage[(block_id, istep)] = bank_id
                mem_undo_list.append( (block_id, istep) )
                break
        else :
            for block_id, step in mem_undo_list :
                del mem_usage[(block_id, step)]
            for node in schedule_undo_list :
                node.set_schedule(-1)
            return False
        inode.set_schedule(istep)
        schedule_undo_list.append(inode)
    return True


def list_scheduling(dfg, node_list, op_limit) :
    mem_usage = dict()
    op1_usage = dict()
    op2_usage = dict()
    last_step = 0
    for node in node_list :
        if node.is_memsrc :
            block_id = node.block_id
            bank_id = node.bank_id
            for step in range(lastt_step) :
                if (block_id, step) in mem_usage :
                    if mem_usage[(block_id, step)] != bank_id :
                        # 他のバンクが使っている．
                        pass
                    else :
                        # OK
                        break
                else :
                    mem_usage[(block_id, step)] = bank_id
                    break
            else :
                step = lastt_step
                last_step += 1
                mem_usage[(block_id, step)] = bank_id
            node.set_schedule(step)
        elif node.is_op1 :
            max_step = 0
            for inode in node.fanin_list :
                step = inode.next_step
                if max_step < step :
                    max_step = step
            for step in range(max_step, last_step) :
                if step in op1_usage :
                    num = op1_usage[step]
                    if num >= op_limit :
                        pass
                    else :
                        op1_usage[step] += 1
                        break
                else :
                    op1_usage[step] = 1
                    break
            else :
                step = last_step
                last_step += 1
                op1_usage[step] = 1
            node.set_schedule(step)
        elif node.is_op2 :
            max_step = 0
            for inode in node.fanin_list :
                step = inode.next_step
                if max_step < step :
                    max_step = step
            step = max_step
            if step in op2_usage :
                op2_usage[step] += 1
            else :
                op2_usage[step] = 1
            node.set_schedule(step)
            if last_step < node.next_step :
                last_step = node.next_step


def list_scheduling2(dfg, node_list, op_limit) :
    mem_usage = dict()
    op1_usage = dict()
    op2_usage = dict()
    memsink_usage = dict()
    last_step = 0
    for node in node_list :
        if node.is_op1 :
            # op1 をおけるステップを探す．
            for step in range(1, last_step) :
                if step in op1_usage :
                    num = op1_usage[step]
                    if num >= op_limit :
                        pass
                    else :
                        if mem_scheduling(node, step, mem_usage) :
                            op1_usage[step] += 1
                            break
                else :
                    if mem_scheduling(node, step, mem_usage) :
                        op1_usage[step] = 1
                        break
            else :
                while True :
                    step = last_step
                    last_step += 1
                    if mem_scheduling(node, step, mem_usage) :
                        op1_usage[step] = 1
                        break
            node.set_schedule(step)
        elif node.is_op2 :
            max_step = 0
            for inode in node.fanin_list :
                step = inode.next_step
                if max_step < step :
                    max_step = step
            step = max_step
            node.set_schedule(step)
            if step in op2_usage :
                op2_usage[step] += 1
            else :
                op2_usage[step] = 1

            step = node.next_step
            onode = node.fanout
            while True :
                key = onode.block_id, step
                if key not in memsink_usage :
                    break
                step += 1
            memsink_usage[key] = onode.bank_id
            onode.set_schedule(step)
            step = onode.next_step
            if last_step < step :
                lastt_step = step


def group_scheduling(op2node_list, base_step) :
    total_num = 0
    for node in op2node_list :
        for op1node in node.fanin_list :
            total_num += op1node.fanin_num

    mem_usage = dict()
    memsink_usage = dict()
    max_step = 0
    for node in op2node_list :
        last_step = 0
        for op1node in node.fanin_list :
            for memnode in op1node.fanin_list :
                # memnode のスケジュールを決める．
                block_id = memnode.block_id
                bank_id = memnode.bank_id
                for step in range(base_step, base_step + total_num) :
                    if (block_id, step) in mem_usage :
                        if mem_usage[(block_id, step)] != bank_id :
                            # 他のバンクが使っている．
                            pass
                        else :
                            # OK
                            break
                    else :
                        mem_usage[(block_id, step)] = bank_id
                        break
                memnode.set_schedule(step)
                step = memnode.next_step
                if last_step < step :
                    last_step = step
        op1_step = last_step
        op2_step = 0
        for op1node in node.fanin_list :
            op1node.set_schedule(op1_step)
            step1 = op1node.next_step
            if op2_step < step1 :
                op2_step = step1
        node.set_schedule(op2_step)

        memsink_step = node.next_step
        onode = node.fanout
        while True :
            key = onode.block_id, memsink_step
            if key not in memsink_usage :
                break
            step += 1
        memsink_usage[key] = onode.bank_id
        onode.set_schedule(memsink_step)
        step1 = onode.next_step
        if max_step < step1 :
            max_step = step1

    return max_step


def list_scheduling3(dfg, op_limit) :
    base_step = 0
    op2node_list = list()
    op1_num = 0
    for op2node in dfg.op2node_list :
        n = op2node.fanin_num
        if op1_num + n <= op_limit :
            op2node_list.append(op2node)
            op1_num += n
            continue
        # 今の op2node_list でひとかたまりにする．
        base_step = group_scheduling(op2node_list, base_step)
        op2node_list.clear()
        op1_num = 0
        op2node_list.append(op2node)
    assert len(op2node_list) > 0
    group_scheduling(op2node_list, base_step)


### @brief スケジューリング結果を評価する．
### @return op1, op2, レジスタ数を返す．
def eval_schedule(dfg) :
    total_step = 0
    for node in dfg.node_list :
        cstep = node.cstep
        if total_step < cstep :
            total_step = cstep
    total_step += 1
    # op1, op2 のリソース量の計算
    op1_num_list = [ 0 for i in range(total_step) ]
    op2_num_list = [ 0 for i in range(total_step) ]
    for node in dfg.node_list :
        step = node.cstep
        if node.is_op1 :
            op1_num_list[step] += 1
        elif node.is_op2 :
            op2_num_list[step] += 1
    op1_num = 0
    op2_num = 0
    for step in range(total_step) :
        if op1_num < op1_num_list[step] :
            op1_num = op1_num_list[step]
        if op2_num < op2_num_list[step] :
            op2_num = op2_num_list[step]

    # レジスタのリソース量の計算
    reg_map_list = [ set() for i in range(total_step) ]
    for node in dfg.node_list :
        ostep = node.cstep
        for inode in node.fanin_list :
            istep = inode.cstep
            if inode.is_mem :
                for step in range(istep + 1, ostep) :
                    reg_map_list[step].add( (inode.block_id, inode.bank_id, inode.offset) )
            else :
                for step in range(istep, ostep - 1) :
                    reg_map_list[step].add(inode.id)
    reg_num = 0
    for step in range(total_step) :
        n = len(reg_map_list[step])
        if reg_num < n :
            reg_num = n

    return op1_num, op2_num, reg_num, total_step


### @brief スケジューリングを行う．
### @param[in] method メソッド名
### @return スケジューリング後の DFG を返す．
def scheduling(dfg, op_limit, s_method) :

    print("my_scheduling")

    # スケジューリングを行う．
    if s_method == 1 :
        list_scheduling(dfg, dfg.node_list, op_limit)
    elif s_method == 2 :
        list_scheduling2(dfg, dfg.node_list, op_limit)
    elif s_method == 3 :
        list_scheduling3(dfg, op_limit)
    else :
        print('error in scheduling: method should be 1 or 2 or 3.')
        exit(1)
    dfg.eval_resource()
    return dfg

def print_schedule(dfg, fout) :
    for node in dfg.memsinknode_list :
        print(file = fout)
        print('[@{}] Node#{}: {}-{}-{}'.format(node.cstep, node.id, node.block_id, node.bank_id, node.offset), file = fout)
        op2 = node.src
        print('[@{}] OP2: #{}'.format(op2.cstep, op2.id), file = fout)
        for op1 in op2.fanin_list :
            print('[@{}]   OP1: #{}'.format(op1.cstep, op1.id), file = fout)
            for mem in op1.fanin_list :
                print('[@{}]    MEMSRC: #{}: {}-{}-{}'.format(mem.cstep, mem.id, mem.block_id, mem.bank_id, mem.offset))


if __name__ == '__main__' :
    import sys
    import os
    from op import Op
    from mem_layout import MemLayout

    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    op_list = None
    with open(filename, 'rt') as fin :
        op_list = Op.read(fin)

    if op_list is None :
        print('read failed.')
        exit(1)

    imem_size = 0
    for op in op_list :
        for i_id, w in op.fanin_list :
            if imem_size < i_id :
                imem_size = i_id
    imem_size += 1

    iblock_num = 12
    iblock_size = 128
    ibank_size = 32
    imem_layout = MemLayout(imem_size, iblock_num, iblock_size, ibank_size)

    omem_size = len(op_list)
    oblock_num = 8
    oblock_size = 125
    obank_size = 1
    omem_layout = MemLayout(omem_size, oblock_num, oblock_size, obank_size)

    # 演算の分割を行い DFG を作る．
    op1_limit = 16
    op2_limit = 15
    for op_limit in (16, 32, 64, 128) :
        for s_method in (3,) :
            dfg = make_graph(op_list, op1_limit, op2_limit, imem_layout, omem_layout)
            dfg = scheduling(dfg, op_limit, s_method)
            print('{}, {}, {}: {} steps'.format(dfg.op1_num, dfg.op2_num, dfg.reg_num, dfg.total_step))
            print_schedule(dfg, sys.stdout)
