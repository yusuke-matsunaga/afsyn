#! /usr/bin/env python3

### @file bipartite.py
### @brief 二部グラフの最大マッチング
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


def find_path(cur_path, l_nodes, r_nodes) :
    l_used = set()
    r_used = set()
    for l, r, w in cur_path :
        l_used.add(l)
        r_used.add(r)

    n_l = len(l_nodes)
    n_r = len(r_nodes)
    for l in range(n_l) :
        if l in l_used :
            continue


### @brief 二部グラフの最大マッチングを行う．
### @param[in] n_l 左の節点数
### @param[in] n_r 右の節点数
### @param[in] edge_list 枝のリスト
### @return 選ばれた枝のリストを返す．n
###
### 枝は (l, r, w) のタプルで表される．
### l は左の節点番号 ( 0 <= l < n_l )
### r は右の節点番号 ( 0 <= r < n_r )
### w は重み
def bipartite_matching(n_l, n_r, edge_list) :
    if len(edge_list) == 0 :
        return []
    assert n_l > 0
    assert n_r > 0
    left_nodes = [ [] for i in range(n_l) ]
    right_nodes = [ [] for i in range(n_r) ]
    for l, r, w in edge_list :
        l_node = l_nodes[l]
        r_node = r_nodes[r]
        l_node.append( (r_node, w) )
        r_node.append( (l_node, w) )

    # 初期マッチングを求める．
    path1 = list()
    cost1 = 0
    l_used = set()
    r_used = set()
    for l, r, w in edge_list :
        if l is not in l_used and r is not in r_used :
            path1.append( (l, r, w) )
            cost1 += w
            l_used.add(l)
            r_used.add(r)

    # path1 に対する増加路を見つける．
    while True :
        a_path = find_path(path1, l_nodes, r_nodes)
        if a_path is not None :
            path1 = modify_path(path1, a_path)

    return path1


if __name__ == '__main__' :
    n_l = 4
    n_r = 4
    edge_list = [
        (0, 0, 1),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 1),
        (1, 2, 1),
        (2, 1, 1),
        (2, 2, 1),
        (3, 1, 1),
        (3, 2, 1),
        (3, 3, 1)
        ]

    ans_list = bipartite_matching(n_l, n_r, edge_list)

    for l, r, w in ans_list :
        print('{} - {}: {}'.format(l, r, w))
