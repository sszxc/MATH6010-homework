# Author: Xuechao Zhang
# Date: March 20th, 2022
# Description: Greedy Algorithm for Min Dominating Set

from matplotlib import colors
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import math

def random_graph_with_min_degree(n, delta, p):
    """
    生成一个n个节点的连通图, 所有边连接概率为p, 但保证节点最小度delta
    modified from https://stackoverflow.com/questions/61958360/how-to-create-random-graph-where-each-node-has-at-least-1-edge-using-networkx
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
    # min degree verification
    min_degree = n
    min_degree_node = None
    for i in list(G.nodes):
        if G.degree(i)<min_degree:
            min_degree = G.degree(i)
            min_degree_node = i
    print("vertice", min_degree_node, "has min degree", min_degree, ".")
    return G

def find_min_dominating_set(graph):
    remaining_set = list(graph.nodes)
    dominating_set = []
    while len(remaining_set):
        max_degree = 0
        max_degree_node = None
        for i in remaining_set:
            if graph.degree(i) > max_degree:  # 找最大度
                max_degree = graph.degree(i)
                max_degree_node = i
        # 更新剩余集合
        dominating_set.append(max_degree_node)
        remaining_set.remove(max_degree_node)
        remaining_set =[node for node in remaining_set if node not in list(graph.adj[max_degree_node])]
    print("Dominating set found!")
    return dominating_set

if __name__ == '__main__':
    print("------------------------------------------------")
    # 生成随机图
    n = random.randint(5,20)  # 定义顶点数量
    delta = 2  # 最小度
    probability = 0.1  # 图中边连接概率
    G = random_graph_with_min_degree(n, delta, probability)

    # 寻找最小支配集
    min_dom_set = find_min_dominating_set(G)
    # 自带函数验证是否支配
    print("Dominating verification:", nx.algorithms.is_dominating_set(G, min_dom_set))
    
    # 与理论最大值比较
    print("Result has", len(min_dom_set), "vertices.", end=" ")
    print("Theoretically it has at most", n*(1+math.log(delta+1))/(delta+1), "vertices.")

    # 染色
    colors = ["gold" if node in min_dom_set else "lightblue" for node in list(G.nodes)]

    # 画图
    nx.draw(G, 
            node_color=colors,
            node_size=1000,
            with_labels=True,
            font_weight='bold')
    patch1 = mpatches.Patch(color='gold', label='Dominating Set')
    patch2 = mpatches.Patch(color='lightblue', label='Other Vertices')
    plt.legend(handles=[patch1, patch2])
    plt.show()