# Author: Xuechao Zhang
# Date: May 9th, 2022
# Description: 超图可视化, star expansion 形式

import networkx as nx
import matplotlib.pyplot as plt
import random

def draw_hypergraph(graph, fixed_node=None):
    """
    根据名称"node0""node1""edge0""edge1"区分节点类型, 实现超图可视化
    fixed_node = (node, pos): 固定部分节点位置 
    """    
    colors = ["mediumseagreen" if node[:4]=='node' else "grey"
                        for node in list(graph.nodes)]
    sizes = [1000 if node[:4]=='node' else 50
                        for node in list(graph.nodes)]
    label_dict = {node:node[4:] if node[:4]=='node' else ''
                        for node in list(graph.nodes)}
    if fixed_node:
        (node, pos) = fixed_node
        pos = nx.spring_layout(graph, pos=pos, fixed=node)
    else:
        pos = nx.spring_layout(graph)
    nx.draw(graph,
        pos,
        node_color=colors,
        node_size=sizes,
        labels=label_dict,
        font_weight='bold')
    
    return plt

if __name__ == '__main__':
    random.seed(777)
    
    star_expansion_graph = nx.Graph()               # 转换成 star expansion 形式
    node_num = 6
    edge_num = 5
    for i in range(node_num):
        star_expansion_graph.add_node('node'+str(i))
    for i in range(edge_num):                       # 添加超边
        star_expansion_graph.add_node('edge'+str(i))
        for j in random.sample(range(node_num), random.choice([3, 3, 4])): # 连接超边和顶点
            star_expansion_graph.add_edge('edge'+str(i), 'node'+str(j))
    
    fig, ax = plt.subplots()
    draw_hypergraph(star_expansion_graph)    
    plt.show()