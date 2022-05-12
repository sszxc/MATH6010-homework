# Author: Xuechao Zhang
# Date: May 9th, 2022
# Description: a hill-climbing algorithm for constructing random STS(v)

import itertools
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from hypergraph_visualization import *

class STS():
    def __init__(self, node_num, monitor=False):
        """
        node_num: 节点数量
        monitor: 是否开启实时渲染
        """
        self.monitor = monitor
        if node_num % 6 == 1 or node_num % 6 == 3:
            self.construct(node_num)
        else:
            raise ValueError("Wrong node number! v must satisfy v%6==1 or v%6==3.")

    def graph_add_hyper_neighbors(self):
        """
        为超图中每个节点创建邻居集合 (点-边-点)
        集合中会包含节点自身, 计算度时注意 -1
        注意需要在添加完所有顶点后执行
        """
        nx.set_node_attributes(self.G, None, "neighbors")  #TODO: list 和 set 都需要单独赋值, dict 不用
        for node in [node for node in list(self.G.nodes)
                            if node[:4] == 'node']:  # 遍历所有节点
            self.G.nodes[node]['neighbors'] = {node}  # 赋初始集合

    def update_nodes_neighbor(self):
        """
        遍历超边, 计算超图顶点的度
        n.b. 两条不同的超边连接A、B时, 节点度计算一次
        """
        for node in [node for node in list(self.G.nodes)
                            if node[:4] == 'node']:  # 遍历所有节点
            self.G.nodes[node]['neighbors'] = {node}  # 清空邻居 (针对switch操作)
        for hyper_edge in list(self.G.nodes):
            if hyper_edge[:4] == 'edge':  # 遍历超边
                connected_nodes = list(self.G.adj[hyper_edge])  # 超边连接的所有点
                for i,j in list(itertools.permutations(connected_nodes, 2)):
                    self.G.nodes[i]['neighbors'].add(j)

    def construct(self, node_num):
        '''
        爬山法构造 STS(v)
        '''
        self.G = nx.Graph()
        hyper_node = []  # 超图中的点
        hyper_edge = []  # 超图中的边
        for i in range(node_num):  # 创建所有节点
            self.G.add_node('node'+str(i))
            hyper_node.append('node'+str(i))
        self.graph_add_hyper_neighbors()
        target_edge_num = node_num*(node_num-1)/6  # 最优条件

        def find_live_points(graph):
            """
            寻找度小于 (node_num-1)/2 的点
            """
            live_points = []
            for node in hyper_node:
                if len(graph.adj[node]) < (node_num-1)/2:
                # if len(graph.nodes[node]['neighbors'])-1 < node_num-1:  # 两种写法等价
                    live_points.append(node)
            return live_points

        def find_live_pairs(graph, live_points):
            """
            寻找live_points中未相互连接的点对
            """
            live_pairs = []
            for p, q in list(itertools.combinations(live_points, 2)):
                if q not in graph.nodes[p]['neighbors']:
                    live_pairs.append((p, q))
            all_points = list(set([node for pair in live_pairs for node in pair]))  # 一种丧失了可读性的漂亮代码 和下一行等价                            
            # all_points = list(set([point[0] for point in live_pairs]
            #                     + [point[1] for point in live_pairs]))
            return live_pairs, all_points

        def find_live_block(live_pairs, all_points):
            """
            寻找live_pairs中可行的block
            """
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
        
        def switch_block(graph, live_pairs, all_points):
            """
            无法新增的情况下进行随机替换
            """
            first_edge = random.choice(live_pairs)
            if random.randint(0,1) == 0:  # 保证随机性, 注意下文ab并不等价
                a, b = first_edge
            else:
                b, a = first_edge
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
                            # print(l[0], b, c, "→", a, b, c)
                            return
            print("FUCKED UP")  # 一般是出问题了



        # 开始构造        
        tqdm_bar = tqdm(total=target_edge_num)  # 进度条控制
        if self.monitor:
            self.hyper_node_layout = nx.circular_layout(self.G)  # 超图节点环形分布
            fig = plt.figure()  # 生成画布
            plt.ion()  # 打开交互模式
        while len(hyper_edge) < target_edge_num:
            self.update_nodes_neighbor()
            live_points = find_live_points(self.G)                        # 寻找未连接满的顶点
            live_pairs, all_points = find_live_pairs(self.G, live_points)   # 寻找可行的连接对
            live_blocks = find_live_block(live_pairs, all_points)   # 寻找可行的超边
            if live_blocks:                             # 有可行的超边
                new_edge_name = 'edge'+str(len(hyper_edge))
                self.G.add_node(new_edge_name)           # 新增超边
                hyper_edge.append(new_edge_name)
                for i in live_blocks:
                    self.G.add_edge(new_edge_name, i)    # 连接所有顶点
                tqdm_bar.update(1)  # 进度条控制
            else:                                       # 没有可行的超边
                switch_block(self.G, live_pairs, all_points)
            if self.monitor:
                fig.clf()
                self.update_gif(hyper_node, self.hyper_node_layout)
                plt.pause(0.01)
        # 完成构造
        tqdm_bar.close()  # 进度条控制
        if self.monitor:
            plt.ioff()  # 关闭交互模式
            plt.show()

    def update_gif(self, node, node_pos):
        """
        更新构建过程截图 节点为固定位置
        """
        draw_hypergraph(self.G, fixed_node=(node, node_pos))

    def draw(self):
        """
        绘制图形 节点随机分布
        """
        fig, ax = plt.subplots()
        draw_hypergraph(self.G)
        plt.show()

if __name__ == '__main__':
    random.seed(777)
    v = 31
    graph = STS(v, monitor=False)
    graph.draw()