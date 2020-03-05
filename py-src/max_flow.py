#! /usr/bin/env python3

### @file max_flow.py
### @brief 最大フローを解くプログラム
### @author Yusuke Matsunaga (松永 裕介)
###
### Copyright (C) 2020 Yusuke Matsunaga
### All rights reserved.


### @brief フローグラフの枝を表すクラス
class FgEdge :

    ### @brief 初期化
    ### @param[in] from_id 始点のノード番号
    ### @param[in] to_id 終点のノード番号
    ### @param[in] cap 容量
    def __init__(self, from_id, to_id, cap) :
        self.__from_id = from_id
        self.__to_id = to_id
        self.__cap = ca;

    ### @brief 始点のノード番号を返す．
    @property
    def from_id(self) :
        return self.__from_id

    ### @brief 終点のノード番号を返す．
    @property
    def to_id(self) :
        return self.__to_id

    ### @brief 容量を返す．
    @property
    def cap(self) :
        return self.__cap


### @brief フローグラフのノードを表すクラス
class FgNode :

    ### @brief 初期化
    ### @param[in] node_id ノード番号
    def __init__(self, node_id) :
        self.__node_id = node_id
        self.__inedge_list = list()
        self.__outedge_list = list()
        self.pos = -1
        self.flow = 0
        self.prev = None

    ### @brief inedge を追加する．
    def add_inedge(self, edge) :
        self.__inedge_list.append(edge)

    ### @brief outedge を追加する．
    def add_outedge(self, edge) :
        self.__outedge_list.append(edge)


### @brief フローグラフを表すクラス
class FlowGraph :

    ### @brief 初期化
    ### @param[in] node_num ノード数
    ### @param[in] edge_list 枝のリスト
    def __init__(self, node_num, edge_list) :
        self.__node_num = node_num
        self.__edge_list = edge_list

    ### @brief ノード数を返す．
    @property
    def node_num(self) :
        return self.__node_num

    ### @brief 枝のリストを返す．
    @property
    def edge_list(self) :
        return self.__edge_list


### @brief 優先度付きキューを表すクラス
class Queue :

    ### @brief 初期化
    ### @param[in] max_size 最大サイズ
    def __init__(self, max_size) :
        self.__heap = [ None for i in range(max_size) ]
        self.__num = 0

    ### @brief 要素数を返す．
    def num(self) :
        return self.__num

    ### @brief ノードを追加する．
    def push(self, node) :
        pos = self.__num
        self.__num += 1
        self.__locate(node, pos)
        self.__move_up(pos)

    ### @brief 先頭のノードを取り出す．
    def pop_top(self) :
        assert self.__num > 0
        node = self.__heap[0]
        self.__num -= 1
        node0 = self.__heap[self.__num]
        self.__locate(node0, 0)
        self.__move_down(0)
        return node

    ### @brief ノードを適切な位置まで上げる．
    def __move_up(self, pos) :
        while pos > 0 :
            p_pos = (pos - 1) // 2
            node = self.__heap[pos]
            p_node = self.__heap[p_pos]
            if node.flow > p_node.flow :
                self.__locate(node, p_pos)
                self.__locate(p_node, pos)
                pos = p_pos
            else :
                break

    ### @brief ノードを適切な位置まで下げる．
    def __move_down(self, pos) :
        while True :
            l_pos = pos * 2 + 1
            r_pos = pos * 2 + 2
            if l_pos >= self.__num :
                # 子供を持たない場合
                break
            node = self.__heap[pos]
            l_node = self.__heap[l_pos]
            if r_pos >= self.__num :
                # 左の子供のみ持つ場合
                if l_node.flow > node.flow :
                    self.__locate(node, l_pos)
                    self.__locate(l_node, pos)
                break
            else :
                if r_node.flow > node.flow :
                    self.__locate(node, r_pos)
                    self.__locate(r_node, pos)
                    pos = r_pos
                else :
                    break

    ### @brief ノードをヒープに積む．
    def __locate(self, node, pos) :
        self.__heap[pos] = node
        node.pos = pos


### @brief 増加路を見つける．
### @param[in] graph 対象のグラフ
### @param[in] start 始点のノード番号
### @param[in] end 終点のノード番号
def find_path(graph, start, end) :
    queue = Queue(graph.node_num)
    s_node = graph.node(start)
    s_node.flow = flow_max
    s_node.prev = None
    queue.push(s_node)

    while queue.num() > 0 :
        node = queue.pop_top()
        p_edge = node.prev
        if p_edge is None or p_edge.to_id == node.node_id :
            # outedge を探す．
            for edge in node.outedge_list :
                to_node = graph.node(edge.to_id)
                flow = node.flow
                if edge.cap


### @brief 最大フローを求める．
### @param[in] graph 対象のフローグラフ
### @param[in] start 始点のノード番号
### @param[in] end 終点のノード番号
### @return 全体のフロー値と個々の枝のフローのリストを返す．
def max_flow(graph, start, end) :
    # 個々のノードのフロー値
    node_flow = [ 0 for i in range(graph.node_num) ]

    # 個々の枝のフロー値
    edge_flow = [ 0 for edge in graph.edge_list ]

    # 増加路が見つける．
    while find_path(graph, start, end, node_flow, edge_flow) :
        backtrace(graph, node_flow, edge_flow)
