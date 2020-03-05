#! /usr/bin/env python3

### @file bipartite.py
### @brief 二部グラフの最大マッチング
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


### @brief 二部グラフのノードを表すクラス
class BiNode :

    ### @brief 初期化
    ### @param[in] id ID番号
    def __init__(self, id) :
        self.__id = id
        self.__edge_list = list()

    ### @brief 枝を追加する．
    def add_edge(self, edge) :
        self.__edge_list.append(edge)

    ### @brief ID番号を返す．
    @property
    def id(self) :
        return self.__id

    ### @brief 枝のリストを返す．
    @property
    def edge_list(self) :
        return self.__edge_list

    ### @brief 選択されている時に True を返す．
    @property
    def is_selected(self) :
        for edge in self.__edge_list :
            if edge.is_selected :
                return True
        else :
            return False


### @brief 二部グラフの枝を表すクラス
class BiEdge :

    ### @brief 初期化
    ### @param[in] node1, node2 両端のノード
    def __init__(self, node1, node2) :
        self.__node1 = node1
        self.__node2 = node2
        self.__selected = False

    ### @brief ノード1を返す．
    @property
    def node1(self) :
        return self.__node1

    ### @brief ノード2を返す．
    @property
    def node2(self) :
        return self.__node2

    ### @brief 選択されている時 True を返す．
    @property
    def is_selected(self) :
        return self.__selected

    ### @brief 選択済みの印を付ける．
    def select(self) :
        self.__selected = True

    ### @brief 選択済みの印を消す．
    def unselect(self) :
        self.__selected = False

    ### @brief 選択済みの印を反転させる．
    def flip_select(self) :
        self.__selected = not self.__selected


def dfs(l_node, path, visited) :
    # l_node に接続している枝を調べる．
    for edge in l_node.edge_list :
        if edge.is_selected :
            continue
        r_node = edge.node2
        if r_node.id in visited :
            continue
        visited.add(r_node.id)
        if r_node.is_selected :
            # 選択されている枝を見つける．
            r_edge = None
            for edge1 in r_node.edge_list :
                if edge1.is_selected :
                    r_edge = edge1
                    break
            else :
                assert False
            path1 = path + [edge, r_edge]
            path1 = dfs(r_edge.node1, path1, visited)
            if path1 :
                return path1
        else :
            # 見つけた．
            return path + [edge]
    return None


### @brief 増加路を求める．
def find_path(l_nodes, r_nodes, edge_list) :
    for l_node in l_nodes :
        if l_node.is_selected :
            # 選択されているノードはスキップ
            continue
        visited = set()
        path = dfs(l_node, [], visited)
        if path :
            return path
    else :
        return None


### @brief 二部グラフの最大マッチングを行う．
### @param[in] n_l 左の節点数
### @param[in] n_r 右の節点数
### @param[in] edge_list 枝のリスト
### @return 選ばれた枝のリストを返す．
###
### 枝は (l, r) のタプルで表される．
### l は左の節点番号 ( 0 <= l < n_l )
### r は右の節点番号 ( 0 <= r < n_r )
def bipartite_matching(n_l, n_r, src_edge_list) :
    if len(src_edge_list) == 0 :
        return list()
    assert n_l > 0
    assert n_r > 0
    l_nodes = [ BiNode(i) for i in range(n_l) ]
    r_nodes = [ BiNode(i) for i in range(n_r) ]
    edge_list = list()
    for l, r in src_edge_list :
        l_node = l_nodes[l]
        r_node = r_nodes[r]
        edge = BiEdge(l_node, r_node)
        l_node.add_edge(edge)
        r_node.add_edge(edge)
        edge_list.append(edge)

    # 初期マッチングを求める．
    path1 = list()
    cost1 = 0
    for edge in edge_list :
        if not edge.node1.is_selected and not edge.node2.is_selected :
            path1.append(edge)
            edge.select()
            cost1 += 1

    # 増加路を見つける．
    while True :
        a_path = find_path(l_nodes, r_nodes, edge_list)
        if a_path :
            for edge in a_path :
                edge.flip_select()
        else :
            break

    return [ (edge.node1.id, edge.node2.id) for edge in path1 ]


if __name__ == '__main__' :
    n_l = 4
    n_r = 4
    edge_list = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (3, 3)
        ]

    ans_list = bipartite_matching(n_l, n_r, edge_list)

    for l, r in ans_list :
        print('{} - {}'.format(l, r))

    ans2_list = bipartite_matching(3, 3, [(0, 2), (1, 0), (1, 1), (2, 1)])

    print()
    for l, r in ans2_list :
        print('{} - {}'.format(l, r))
