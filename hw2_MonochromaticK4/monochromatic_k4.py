# Author: Xuechao Zhang
# Date: April 8th, 2022
# Description: Greedy Algorithm for Monochromatic K4

from matplotlib import colors
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import itertools

class MonochromaticK4():
    def __init__(self, nodes, probability):
        '''
        定义图, 初始化数据结构
        '''
        self.graph = self.random_graph_with_min_degree(nodes, probability)  # 随机连通图
        
        # --- K4 字典 ---
        # {K4id: [[K4顶点], 异色状态]}
        # 异色状态: 0: 未支配, 1: 支配
        # |状态|  0 |  1 |  2 |  3 |  4 |  5 |  6 |  -1 |
        # |已染|  0 |  1 |  2 |  3 |  4 |  5 |  6 |异色边|
        # |I_k|2^-5|2^-5|2^-4|2^-3|2^-2|2^-1|2^-0|  0  |
        self.K4_dict = self.find_K4()
        
        # --- 边 属性 ---
        # 边: {related_K4: [相关K4id], color: [颜色]}
        nx.set_edge_attributes(self.graph, None, "related_K4")  # 为边添加“相关的K4”属性  #TODO: 在这里赋空列表会造成浅拷贝
        nx.set_edge_attributes(self.graph, "None", "color")  # 为边添加“颜色”属性
        for e1, e2 in self.graph.edges:
            self.graph[e1][e2]['related_K4'] = []  # 赋初始空列表
        self.find_related_K4()

    def random_graph_with_min_degree(self, n, p, delta = 1):
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
        return G

    def find_K4(self):
        '''
        寻找4顶点完全子图
        '''        
        cliques = list(nx.find_cliques(self.graph))
        K4 = [c for c in cliques if len(c) == 4]
        K4_dict = {}
        for i in range(len(K4)):
            K4_dict[i] = [K4[i], 0]
        return K4_dict

    def find_related_K4(self):
        '''
        寻找每条边相关的K4
        '''
        for i in range(len(self.K4_dict)):
            nodes = self.K4_dict[i][0]
            for e1, e2 in itertools.combinations(nodes, 2):
                target = self.graph[e1][e2]  #TODO: target不能指向字典的key
                target['related_K4'].append(i)

    def coloring(self):            
        '''
        一种启发式染色算法
        '''
        def random_color():
            return random.choice(['balck', 'white'])

        def update_W(self, e1, e2, color):
            '''
            计算染色 (e1, e2) 为 color 在全局的收益
            '''
            reward = 0
            for k in self.graph[e1][e2]['related_K4']:
                # 计算染色 (e1, e2) 为 color 在 k 中的收益
                colors = [self.graph[e1][e2]['color']
                    for e1, e2 in itertools.combinations(self.K4_dict[k][0], 2)]
                reward -= update_Ik(colors)  # 染色前
                colors.append(color)  # 被染色的边原来肯定是 None, 这里直接 append 就行
                reward += update_Ik(colors)  # 染色后
                #TODO: Ik写进K4属性
            return reward

        def update_Ik(colors):
            '''
            根据六条边的颜色计算 Ik
            '''            
            count = 0
            target_color = 'None'
            for color in colors:
                if color != 'None':
                    if target_color == 'None':  # 第一个有色边
                        target_color = color
                        count += 1
                    elif color == target_color:  # 同色边
                        count += 1
                    else:  # 异色边
                        return 0
            if count == 0: 
                count = 1  # 已染0条边与1条边的Ik相同
            return 2**-count

        self.color_sequence = list(self.graph.edges)  # (伪随机的)染色顺序

        for e1, e2 in self.color_sequence:  # 比较黑白收益 执行染色
            reward_w = update_W(self, e1, e2, "white")
            reward_b = update_W(self, e1, e2, "black")
            self.graph[e1][e2]['color'] = "white" if reward_w < reward_b else "black"

    def draw_graph(self, label = False, legend = True):
        '''
        画图, 同时给边染上不同颜色
        '''
        fig, ax = plt.subplots()
        colors = ["grey" if self.graph[e1][e2]['color'] == "white" else "black"
                    for e1, e2 in self.graph.edges]
        nx.draw(self.graph,
                edge_color=colors,
                width = 3,
                node_color="lightblue",
                node_size=1000,
                with_labels=True,
                font_weight='bold')
        
        # if label == True:  # 标注框
        #     textstr = '\n'.join((
        #         r'n: %d'%self.n,
        #         r'$\delta$: %d'%self.delta,
        #         r'p: %.2f'%self.p,
        #         r'practical result: %d'%len(self.min_dom_set),
        #         r'theoretical result: %d'%self.theoretical_min_dom_set_size))
        #     props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        #     ax.text(0.0, 0.2, textstr, transform=ax.transAxes, fontsize=10,
        #         verticalalignment='top', bbox=props)    
        
        # if legend == True:  # 图例
        #     patch1 = mpatches.Patch(color='gold', label='Dominating Set')
        #     patch2 = mpatches.Patch(color='lightblue', label='Other Vertices')
        #     plt.legend(handles=[patch1, patch2])
        return plt
    
if __name__ == '__main__':
    print("------------------------------------------------")

    random.seed(777)
    # MK4 = MonochromaticK4(8, 0.7)
    MK4 = MonochromaticK4(200, 1)

    MK4.coloring()

    MK4.draw_graph(label = False, legend = False)  #TODO: 设计一下可视化方式, 包括但不限于调整配色、单独展示K4、染色顺序等
    plt.show()