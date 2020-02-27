#! /usr/bin/env python3

### @file binder.py
### @brief バインディングを行うプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.



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


class Var :

    def __init__(self, start, end) :
        self.__start = start
        self.__end = end
        self.__reg_id = -1

    @property
    def start(self) :
        return self.__start

    @property
    def end(self) :
        return self.__end

    @property
    def reg_id(self) :
        return self.__reg_id

    def assign(self, reg_id) :
        self.__reg_id = reg_id

    def __lt__(self, other) :
        if self.__start < other.__start :
            return True
        elif self.__start > other.__start :
            return False
        elif self.__end < other.__end :
            return True
        else :
            return False


def bind(dfg, schedule) :
    op1_num, op2_num, reg_num = eval_schedule(dfg, schedule)

    # 演算器はとりあえずナイーブに割り当てる．
    total_step = schedule.total_step
    op1_map = dict()
    op2_map = dict()

    op1_count = [ 0 for i in range(total_step) ]
    op2_count = [ 0 for i in range(total_step) ]

    for node in dfg.node_list :
        step = schedule.get(node.id)
        if node.is_op1 :
            c = op1_count[step]
            op1_map[node.id] = c
            op1_count[step] = c + 1
        elif node.is_op2 :
            c = op2_count[step]
            op2_map[node.id] = c
            op2_count[step] = c + 1

    # レジスタはレフトエッジ法を用いる．
    # まず変数の定義を行う．
    var_list = list()
    for node in dfg.node_list :
        ostep = schedule.get(node.id)
        for inode in node.fanin_list :
            istep = schedule.get(inode.id)
            if inode.is_mem :
                if istep < ostep - 1 :
                    # (istep + 1) - ostep
                    var = Var(istep + 1, ostep)
                    var_list.append(var)
            else :
                # istep - ostep
                var = Var(istep, ostep)
                var_list.append(var)

    # start, end でソートする．
    var_list.sort()

    reg_count = 0
    last = 0
    while True :
        new_var_list = list()
        for var in var_list :
            if var.start >= last :
                var.assign(reg_count)
                last = var.end
            else :
                new_var_list.append(var)
        if new_var_list == [] :
            break
        reg_count += 1
        last = 0
