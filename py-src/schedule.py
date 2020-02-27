#! /usr/bin/env python3

### @file schedule.py
### @brief スケジューリング結果を表すクラス
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.

class Schedule :

    ### @brief 初期化
    def __init__(self) :
        self.__total_step = 0
        self.__cstep_dict = dict()
        self.__node_list_array = list()

    ### @brief スケジュールを設定する．
    ### @param[in] node_id ノード番号
    ### @param[in] cstep スケジュールするコントロールステップ
    def set(self, node_id, cstep) :
        self.__cstep_dict[node_id] = cstep
        n = cstep + 1
        if self.__total_step < n :
            self.__total_step = n
        while len(self.__node_list_array) < n :
            self.__node_list_array.append(list())
        self.__node_list_array[cstep].append(node_id)

    ### @brief スケジュールを削除する．
    ### @param[in] node_id ノード番号
    def clear(self, node_id) :
        s = self.__cstep_dict[node_id]
        del self.__cstep_dict[node_id]
        # self.__node_list_array[s] から node_id を削除する．

    ### @brief 総ステップ数を返す．
    @property
    def total_step(self) :
        return self.__total_step

    ### @brief 指定されたコントロールステップにスケジュールされたノードのリストを返す．
    ### @param[in] cstep コントロールステップ
    def node_list(self, cstep) :
        return self.__node_list_array[cstep]

    ### @brief スケジュールされているコントロールステップを返す．
    ### @param[in] node_id ノード番号
    def get(self, node_id) :
        return self.__cstep_dict[node_id]
