# Author: Xuechao Zhang
# Date: May 9th, 2022
# Description: a hill-climbing algorithm for constructing random STS(v)

import itertools
import networkx as nx
import matplotlib.pyplot as plt
from hypergraph import *

class STS():
    def __init__(self, node_num, debug = False):
        if node_num % 6 == 1 or node_num % 6 == 3:
            if debug:
                self.construct4debug()
            else:
                self.construct(node_num)
        else:
            raise ValueError("Wrong node number! v must satisfy v%6==1 or v%6==3.")

    def construct4debug(self):
        '''
        构造一个一般的超图 用于debug
        '''
        node_num = 6
        edge_num = 5
        graph = nx.Graph()                  # 转换成 star expansion 形式
        for i in range(node_num):           # 添加顶点
            graph.add_node('node'+str(i))
        for i in range(edge_num):           # 添加超边
            graph.add_node('edge'+str(i))
            for j in random.sample(range(node_num), 
                        random.choice([3, 3, 4])):      # 随机构造超边, 随机连接顶点
                graph.add_edge('edge'+str(i), 'node'+str(j))
        
        self.graph_add_hyper_neighbors(graph)
        self.update_nodes_degree(graph)
        self.graph = graph

    def graph_add_hyper_neighbors(self, graph):
        """
        为超图中每个节点创建邻居集合 (点-边-点)
        集合中会包含节点自身, 计算度时注意 -1
        注意在添加完所有顶点后执行
        """
        nx.set_node_attributes(graph, None, "neighbors")  #TODO: list 和 set 都需要单独赋值, dict 不用
        for node in [node for node in list(graph.nodes)
                            if node[:4] == 'node']:  # 遍历所有节点
            graph.nodes[node]['neighbors'] = {node}  # 赋初始集合

    def update_nodes_degree(self, graph):
        """
        遍历超边, 计算超图顶点的度
        n.b. 两条不同的超边连接A、B时, 节点度计算一次
        """
        for hyper_edge in list(graph.nodes):
            if hyper_edge[:4] == 'edge':  # 遍历超边
                connected_nodes = list(graph.adj[hyper_edge])  # 超边连接的所有点
                for i,j in list(itertools.permutations(connected_nodes, 2)):
                    graph.nodes[i]['neighbors'].add(j)

    def construct(self, node_num):
        '''
        构造 STS(v)
        '''
        graph = nx.Graph()
        hyper_node = []  # 超图中的点
        hyper_edge = []  # 超图中的边
        for i in range(node_num):
            graph.add_node('node'+str(i))
            hyper_node.append('node'+str(i))
        self.graph_add_hyper_neighbors(graph)

        def find_live_points():
            live_points = []
            for node in hyper_node:
                if len(graph.adj[node]) < (node_num-1)/2:
                # if len(graph.nodes[node]['neighbors'])-1 < node_num-1:  # 两种写法等价
                    live_points.append(node)
            return live_points

        def find_live_pairs(live_points):
            live_pairs = []
            for p, q in list(itertools.combinations(live_points, 2)):
                if q not in graph.nodes[p]['neighbors']:
                    live_pairs.append((p, q))
            all_points = list(set([node for pair in live_pairs for node in pair]))  # 一种丧失了可读性的漂亮代码 和下一行等价                            
            # all_points = list(set([point[0] for point in live_pairs]
            #                     + [point[1] for point in live_pairs]))
            return live_pairs, all_points

        def find_live_block(live_pairs, all_points):
            # 当做图来处理, 寻找3-集团, 但效率非常低
            # G = nx.Graph()
            # G.add_edges_from(live_pairs)
            # live_blocks = [c for c in nx.enumerate_all_cliques(G) if len(c)==3]
            # return live_blocks
            
            live_pairs_copy = live_pairs.copy()
            while live_pairs_copy:
                first_edge = random.choice(live_pairs_copy)
                a, b = first_edge
                for c in all_points:
                    if ((a,c) in live_pairs_copy or (c,a) in live_pairs_copy) \
                        and ((b,c) in live_pairs_copy or (c,b) in live_pairs_copy):
                        return (a,b,c)
                live_pairs_copy.remove(first_edge)
            return 0
        
        def switch_block(live_pairs, all_points):
            print("switch_block")
            first_edge = random.choice(live_pairs)
            a, b = first_edge
            for c in all_points:
                if ((a,c) in live_pairs or (c,a) in live_pairs)\
                    and b!=c:                               # 随意选择可行的 (a,b) 和 (a,c)
                    for edge in hyper_edge:
                        if b in list(graph.adj[edge]) and c in list(graph.adj[edge]):
                            l = list(graph.adj[edge])
                            l.remove(b)
                            l.remove(c)                            
                            graph.remove_edge(edge, l[0])   # 删除原来的(x,b,c), 添加 (a,b,c)
                            graph.add_edge(edge, a)
                            print(l[0], b, c, "→", a, b, c)
                            return

        target_edge_num = node_num*(node_num-1)/6
        print("target_edge_num", target_edge_num)
        count=0
        # 开始构造
        while len(hyper_edge) < target_edge_num:  # 最优条件
            self.update_nodes_degree(graph)
            live_points = find_live_points()                        # 寻找未连接满的顶点
            live_pairs, all_points = find_live_pairs(live_points)   # 寻找可行的连接对
            live_blocks = find_live_block(live_pairs, all_points)   # 寻找可行的超边
            if live_blocks:                         # 有可行的超边
                new_edge_name = 'edge'+str(len(hyper_edge))
                graph.add_node(new_edge_name)
                hyper_edge.append(new_edge_name)
                for i in live_blocks:
                    graph.add_edge(new_edge_name, i)
                print(len(hyper_edge), "add edge")
            else:                                   # 没有可行的超边
                switch_block(live_pairs, all_points)
                print(len(hyper_edge), "trigger switch!")
            count+=1
            if count==2000:  # 防止死循环
                break
        print("after", count, "times, mission completed.")
        self.graph = graph

    def draw(self):        
        draw_hypergraph(self.graph)

if __name__ == '__main__':
    # random.seed(777)
    v = 9
    graph = STS(v, debug=False)
    # graph.draw()