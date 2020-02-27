#! /usr/bin/env python3

### @file scheduling.py
### @brief
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

import random
from schedule import Schedule


def mem_scheduling(node, step, mem_usage, schedule) :
    mem_undo_list = []
    schedule_undo_list = []
    for inode in node.fanin_list :
        assert inode.is_mem
        block_id = inode.block_id
        bank_id = inode.bank_id
        for istep in range(step - 1, -1, -1) :
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
            for node_id in schedule_undo_list :
                schedule.clear(node_id)
            return False
        schedule.set(inode.id, istep)
        schedule_undo_list.append(inode.id)
    return True


def list_scheduling(dfg, node_list, op_limit) :
    mem_usage = dict()
    op1_usage = dict()
    op2_usage = dict()
    schedule = Schedule()
    next_step = 0
    for node in node_list :
        if node.is_mem :
            block_id = node.block_id
            bank_id = node.bank_id
            for step in range(next_step) :
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
                step = next_step
                next_step += 1
                mem_usage[(block_id, step)] = bank_id
            schedule.set(node.id, step)
        elif node.is_op1 :
            max_step = 0
            for inode in node.fanin_list :
                step = schedule.get(inode.id)
                if max_step < step :
                    max_step = step
            for step in range(max_step + 1, next_step) :
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
                step = next_step
                next_step += 1
                op1_usage[step] = 1
            schedule.set(node.id, step)
        elif node.is_op2 :
            max_step = 0
            for inode in node.fanin_list :
                step = schedule.get(inode.id)
                if max_step < step :
                    max_step = step
            step = max_step + 1
            if step in op2_usage :
                op2_usage[step] += 1
            else :
                op2_usage[step] = 1
            schedule.set(node.id, step)
            if next_step < step + 1:
                next_step = step + 1

    return schedule


def list_scheduling2(dfg, node_list, op_limit) :
    mem_usage = dict()
    op1_usage = dict()
    op2_usage = dict()
    schedule = Schedule()
    next_step = 0
    for node in node_list :
        if node.is_mem :
            pass
        elif node.is_op1 :
            # op1 をおけるステップを探す．
            for step in range(1, next_step) :
                if step in op1_usage :
                    num = op1_usage[step]
                    if num >= op_limit :
                        pass
                    else :
                        if mem_scheduling(node, step, mem_usage, schedule) :
                            op1_usage[step] += 1
                            break
                else :
                    if mem_scheduling(node, step, mem_usage, schedule) :
                        op1_usage[step] = 1
                        break
            else :
                while True :
                    step = next_step
                    next_step += 1
                    if mem_scheduling(node, step, mem_usage, schedule) :
                        op1_usage[step] = 1
                        break
            schedule.set(node.id, step)
        elif node.is_op2 :
            max_step = 0
            for inode in node.fanin_list :
                step = schedule.get(inode.id)
                if max_step < step :
                    max_step = step
            step = max_step + 1
            if step in op2_usage :
                op2_usage[step] += 1
            else :
                op2_usage[step] = 1
            schedule.set(node.id, step)
            if next_step < step + 1:
                next_step = step + 1


    return schedule


### @brief スケジューリング結果を評価する．
### @return op1, op2, レジスタ数を返す．
def eval_schedule(dfg, schedule) :
    total_step = schedule.total_step
    # op1, op2 のリソース量の計算
    op1_num_list = [ 0 for i in range(total_step) ]
    op2_num_list = [ 0 for i in range(total_step) ]
    for node in dfg.node_list :
        step = schedule.get(node.id)
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
        ostep = schedule.get(node.id)
        for inode in node.fanin_list :
            istep = schedule.get(inode.id)
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

    return op1_num, op2_num, reg_num



def scheduling(dfg, op_limit, method) :
    if method == 1 :
        schedule = list_scheduling(dfg, dfg.node_list, op_limit)
    elif method == 2 :
        schedule = list_scheduling2(dfg, dfg.node_list, op_limit)
    else :
        print('error in scheduling: method should be 1 or 2.')
        exit(1)
    op1_num, op2_num, reg_num = eval_schedule(dfg, schedule)
    print('{}, {}, {}: {} steps'.format(op1_num, op2_num, reg_num, schedule.total_step))


if __name__ == '__main__' :
    import sys
    import os
    from op import Op, read_op
    from dfg import make_graph
    from mem_layout import MemLayout

    if len(sys.argv) != 2 :
        print('USAGE: {} <filename>'.format(os.path.basename(sys.argv[0])))
        exit(1)

    filename = sys.argv[1]
    op_list = None
    with open(filename, 'rt') as fin :
        op_list = read_op(fin)

    if op_list is None :
        print('read failed.')
        exit(1)

    mem_size = 0
    for op in op_list :
        for i_id, w in op.fanin_list :
            if mem_size < i_id :
                mem_size = i_id
    mem_size += 1

    for block_num, bank_size in ((24, 16), (24, 32), (12, 16), (12, 32), (6, 16), (6, 32)) :
        print()
        print('Block Num: {}'.format(block_num))
        print('Bank Size: {}'.format(bank_size))
        for method in (1, 2) :
            mem_layout = MemLayout(mem_size, block_num, bank_size, method)
            dfg = make_graph(op_list, mem_layout)

            #print('# of nodes: {}'.format(len(dfg.node_list)))
            #print('# of outputs: {}'.format(len(dfg.output_list)))
            print()
            print('Memory model #{}'.format(method))
            for op_limit in (16, 32, 64, 128) :
                for s_method in (1, 2) :
                    scheduling(dfg, op_limit, s_method)
