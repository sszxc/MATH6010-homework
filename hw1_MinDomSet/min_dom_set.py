# Author: Xuechao Zhang
# Date: March 20th, 2022
# Description: Greedy Algorithm for Min Dominating Set

from re import M
from matplotlib import colors
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import math

class MinDominatingSet():
    def __init__(self, n, delta, p=0.1):
        print("n:", n, "delta:", delta, "p:", p)
        self.n = n
        self.delta = delta
        self.p = p
        self.graph = self.random_graph_with_min_degree(self.n, self.delta, self.p)
        self.theoretical_min_dom_set_bound()

    def random_graph_with_min_degree(self, n, delta, p, verification = False):
        """
        生成一个n节点图, 所有边连接概率为p, 同时保证节点最小度delta
        """
        G = nx.Graph()
        G.add_nodes_from(range(n))
        if p >= 1 or delta>=n-1:
            return nx.complete_graph(n, create_using=G)

        for i in range(n):
            node_nodes = range(i + 1, n)
            random_edges = [j for j in node_nodes if random.random() < p]  # 按概率连接(所有边组合只会在此出现一次)
            G.add_edges_from([(i, j) for j in random_edges])
            
            if G.degree(i) < delta:  # 最小度约束
                remaining_nodes = [j for j in list(G.nodes) if j not in list(G.adj[i]) and i!=j]  # 在剩余所有可选点中选择
                necessary_edges = random.sample(remaining_nodes, delta-G.degree(i))
                G.add_edges_from([(i, j) for j in necessary_edges])
        print("Random graph generated!")

        if verification:
            # min degree verification
            min_degree = n
            min_degree_node = None
            for i in list(G.nodes):
                if G.degree(i)<min_degree:
                    min_degree = G.degree(i)
                    min_degree_node = i
            print("vertice", min_degree_node, "has min degree", min_degree, ".")
        return G

    def find_min_dom_set(self, method = 1, verification = True):
        '''
        贪心算法寻找最小支配集
        method: 0 每次找剩余最大度节点; 1 每次找最大收益节点
        '''
        if method == 0:
            remaining_set = list(self.graph.nodes)
            dominating_set = []
            while len(remaining_set):
                max_degree = 0
                max_degree_node = None
                for i in remaining_set:
                    if self.graph.degree(i) > max_degree:  # 找最大度
                        max_degree = self.graph.degree(i)
                        max_degree_node = i
                # 更新剩余集合
                dominating_set.append(max_degree_node)
                remaining_set.remove(max_degree_node)
                remaining_set =[node for node in remaining_set if node not in list(self.graph.adj[max_degree_node])]  # 删掉对应点的邻居
        elif method == 1:
            dominating_set = []                         # 支配集
            undominated_set = list(self.graph.nodes)    # 未被支配的点
            undominated_neighbors = {}                  # 为每个可选点维护未被支配的邻居dict，换句话说，选择某个点能带来的收益
            for i in range(self.n):
                undominated_neighbors[i] = list(self.graph.adj[i].keys())
                
            while len(undominated_set):
                max_gain = 0
                max_gain_node = None
                for i in undominated_neighbors:
                    if len(undominated_neighbors[i]) > max_gain:  # 找最大收益
                        max_gain = len(undominated_neighbors[i])
                        max_gain_node = i
                # 更新剩余集合
                dominating_set.append(max_gain_node)
                undominated_neighbors.pop(max_gain_node)
                if max_gain_node in undominated_set:
                    undominated_set.remove(max_gain_node)
                undominated_set =[node for node in undominated_set if node not in list(self.graph.adj[max_gain_node])]  # 删掉对应点的邻居
        print("Dominating set found!")
        self.min_dom_set = dominating_set

        if verification:
            # networkx函数验证是否支配
            print("Dominating verification:", nx.algorithms.is_dominating_set(self.graph, self.min_dom_set))
    
        return self.min_dom_set

    def theoretical_min_dom_set_bound(self):
        '''
        计算理论上的最小支配集上界
        '''
        self.theoretical_min_dom_set_size = math.floor(self.n*(1+math.log(self.delta+1))/(self.delta+1))
        return self.theoretical_min_dom_set_size

    def draw_graph(self):
        '''
        画图, 同时给支配集染上不同颜色
        '''
        fig, ax = plt.subplots()

        colors = ["gold" if node in self.min_dom_set else "lightblue" for node in list(self.graph.nodes)]
        nx.draw(self.graph,
                node_color=colors,
                node_size=1000,
                with_labels=True,
                font_weight='bold')
        
        # 标注框
        textstr = '\n'.join((
            r'n: %d'%self.n,
            r'$\delta$: %d'%self.delta,
            r'p: %.2f'%self.p,
            r'practical result: %d'%len(self.min_dom_set),
            r'theoretical result: %d'%self.theoretical_min_dom_set_size))
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        ax.text(0.0, 0.2, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)    
        
        # 图例
        patch1 = mpatches.Patch(color='gold', label='Dominating Set')
        patch2 = mpatches.Patch(color='lightblue', label='Other Vertices')
        plt.legend(handles=[patch1, patch2])
        return plt


if __name__ == '__main__':
    print("------------------------------------------------")
    
    # 生成随机图
    n = 5  # 定义顶点数量
    delta = 2  # 最小度
    probability = 0.1  # 图中边连接概率
    MDS = MinDominatingSet(n, delta, probability)

    # 寻找最小支配集
    MDS.find_min_dom_set()
    
    # 与理论最大值比较
    print("The result has", len(MDS.min_dom_set), "vertices.", end=" ")
    print("Theoretically it has at most", MDS.theoretical_min_dom_set_size, "vertices.")

    # 画图
    plt = MDS.draw_graph()
    plt.show()