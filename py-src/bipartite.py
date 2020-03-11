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
        self.__alt_edge = None
        self.__value = 0
        self.__index = -1

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

    ### @brief 選択されている枝を返す．
    ###
    ### ない時は None を返す．
    @property
    def selected_edge(self) :
        for edge in self.__edge_list :
            if edge.is_selected :
                return edge
        else :
            return None

    ### @brief 選択されている時に True を返す．
    @property
    def is_selected(self) :
        if self.selected_edge :
            return True
        else :
            return False

    ### @brief 代わりの枝を返す．
    @property
    def alt_edge(self) :
        return self.__alt_edge

    ### @brief 現在の価値を返す．
    @property
    def value(self) :
        return self.__value

    ### @brief ヒープ関係の変数を初期化する．
    def init_heap(self) :
        self.__value = -1
        self.__alt_edge = None
        self.__index = -1

    ### @brief 代わりの枝と価値を登録する．
    def update(self, alt_edge, value) :
        self.__value = value
        self.__alt_edge = alt_edge

    ### @brief ヒープ上のインデックスを返す．
    @property
    def index(self) :
        return self.__index

    ### @brief ヒープ上のインデックスを設定する．
    def set_index(self, index) :
        self.__index = index


### @brief 二部グラフの枝を表すクラス
class BiEdge :

    ### @brief 初期化
    ### @param[in] node1, node2 両端のノード
    ### @param[in] w 枝の重み
    def __init__(self, node1, node2, w) :
        self.__node1 = node1
        self.__node2 = node2
        self.__weight = w
        self.__selected = False

    ### @brief ノード1を返す．
    @property
    def node1(self) :
        return self.__node1

    ### @brief ノード2を返す．
    @property
    def node2(self) :
        return self.__node2

    ### @brief 重みを返す．
    @property
    def weight(self) :
        return self.__weight

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


### @brief 増加路用のヒープ木
class Heap :

    ### @brief 初期化
    ### @param[in] max_size 最大サイズ
    def __init__(self, max_size) :
        self.__num = 0
        self.__heap = [ None for i in range(max_size) ]

    ### @brief 要素数を得る．
    @property
    def num(self) :
        return self.__num

    ### @brief 要素を追加する．
    ### @param[in] node 対象のノード
    ### @param[in] alt_edge 代わりの枝
    ### @param[in] value 価値
    def put(self, node, alt_edge, value) :
        if node.value >= value :
            return
        pos = node.index
        if pos == -1 :
            node.update(alt_edge, value)
            pos = self.__num
            self.__num += 1
            self.__heap[pos] = node
            node.set_index(pos)
        else :
            node.update(alt_edge, value)
        self.move_up(pos)

    ### @brief 最大の要素を取り出す．
    def get(self) :
        assert self.num > 0
        node = self.__heap[0]
        self.__num -= 1
        tmp = self.__heap[self.__num]
        self.__heap[0] = tmp
        tmp.set_index(0)
        self.move_down(0)
        return node

    ### @brief 要素を適切な位置まで上げる．
    def move_up(self, pos) :
        while pos > 0 :
            p_pos = ((pos + 1) // 2) - 1
            node = self.__heap[pos]
            p_node = self.__heap[p_pos]
            if p_node.value < node.value :
                self.locate(p_pos, node)
                self.locate(pos, p_node)
                pos = p_pos
            else :
                break

    ### @brief 要素を適切な位置まで下げる．
    def move_down(self, pos) :
        while True :
            l_pos = (pos + 1) * 2 - 1
            r_pos = l_pos + 1
            if l_pos >= self.__num :
                break
            node = self.__heap[pos]
            l_node = self.__heap[l_pos]
            if r_pos >= self.__num :
                # 右の子供はいない．
                if l_node.value > node.value :
                    self.locate(pos, l_node)
                    self.locate(l_pos, node)
                break
            else :
                r_node = self.__heap[r_pos]
                if l_node.value > r_node.value :
                    if l_node.value > node.value :
                        self.locate(pos, l_node)
                        self.locate(l_pos, node)
                        pos = l_pos
                    break
                else :
                    if r_node.value > node.value :
                        self.locate(pos, r_node)
                        self.locate(r_pos, node)
                        pos = r_pos
                    break

    ### @brief ノードをヒープに置く．
    def locate(self, pos, node) :
        self.__heap[pos] = node
        node.set_index(pos)


### @brief 枝をたどって経路を作る．
def make_path(edge1, node1) :
    edge2 = node1.selected_edge
    if edge2 is None :
        return [ edge1 ]
    else :
        node2 = edge2.node2
        edge3 = node1.alt_edge
        assert edge3.node2 == node2
        path = make_path(edge3, edge3.node1)
        return path + [ edge2, edge1 ]


### @brief 重み最大の増加路を求める．
### @param[in] l_nodes Node1 のリスト
### @param[in] r_nodes Node2 のリスト
### @param[in] edge_list 枝のリスト
### 増加路は選ばれた枝と選ばれていない枝が交互に現れる
### 経路のうち，選ばれていない枝の重みの和から選ばれた
### 枝の重みの和を引いたものが正のもの．
###
### このアルゴリズムの性質上，片方の端が選ばれていない
### 枝から始まり，片方の端が選ばれていない枝で終わる
### 奇数長の経路のみ考えればよい．
def find_path(l_nodes, r_nodes, edge_list) :
    for node in l_nodes :
        node.init_heap()

    queue = Heap(len(l_nodes))

    for node1 in l_nodes :
        if not node1.is_selected :
            # 選択されていないノードをキューに積む．
            queue.put(node1, None, 0)

    # queue から値を大きいノードを取り出して BFS を行う．
    max_value = 0
    max_path = None
    not_found = True
    while not_found and queue.num > 0 :
        node1 = queue.get()
        for edge1 in node1.edge_list :
            if edge1.is_selected :
                continue
            value = node1.value + edge1.weight
            node2 = edge1.node2
            if not node2.is_selected :
                # edge1 の端は未選択だった．
                if max_value < value :
                    # 増加路になっていれば終わる．
                    max_value = value
                    max_path = make_path(edge1, node1)
                    not_found = False
            else :
                edge2 = node2.selected_edge
                node3 = edge2.node1
                value -= edge2.weight
                queue.put(node3, edge1, value)
    return max_path


### @brief 二部グラフの最大重みマッチングを行う．
### @param[in] n_l 左の節点数
### @param[in] n_r 右の節点数
### @param[in] edge_list 枝のリスト
### @return 選ばれた枝のリストを返す．
###
### 枝は (l, r, w) のタプルで表される．
### l は左の節点番号 ( 0 <= l < n_l )
### r は右の節点番号 ( 0 <= r < n_r )
### w は枝の重み
def bipartite_matching(n_l, n_r, src_edge_list) :
    if len(src_edge_list) == 0 :
        return list()
    assert n_l > 0
    assert n_r > 0

    # 二部グラフの構造を表すオブジェクトを作る．
    l_nodes = [ BiNode(i) for i in range(n_l) ]
    r_nodes = [ BiNode(i) for i in range(n_r) ]
    edge_list = list()
    for l, r, w in src_edge_list :
        l_node = l_nodes[l]
        r_node = r_nodes[r]
        edge = BiEdge(l_node, r_node, w)
        l_node.add_edge(edge)
        r_node.add_edge(edge)
        edge_list.append(edge)

    # 初期マッチングを求める．
    ne0 = 0
    v0 = 0
    for edge in sorted(edge_list, key = lambda edge: edge.weight, reverse = True) :
        if edge.node1.is_selected or edge.node2.is_selected :
            continue
        edge.select()
        ne0 += 1
        v0 += edge.weight

    # 増加路を見つける．
    while True :
        a_path = find_path(l_nodes, r_nodes, edge_list)
        if a_path :
            for edge in a_path :
                edge.flip_select()
        else :
            break

    return [ (edge.node1.id, edge.node2.id) for edge in edge_list if edge.is_selected ]


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

    for l, r in ans_list :
        print('{} - {}'.format(l, r))

    ans2_list = bipartite_matching(3, 3, [(0, 2, 1), (1, 0, 1), (1, 1, 1), (2, 1, 1)])

    print()
    for l, r in ans2_list :
        print('{} - {}'.format(l, r))

    ans3_list = bipartite_matching(2, 2, [(0, 0, 1), (1, 0, 3), (1, 1, 1)])

    print()
    for l, r in ans3_list :
        print('{} - {}'.format(l, r))
