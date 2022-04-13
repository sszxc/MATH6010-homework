# Author: Xuechao Zhang
# Date: April 8th, 2022
# Description: Greedy Algorithm for Monochromatic K4

import math
import random
import itertools
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
class MonochromaticK4():
    def __init__(self, nodes):
        '''
        定义完全图, 初始化数据结构
        '''
        self.graph = nx.complete_graph(nodes)

        # --- K4 字典 ---
        # {K4id: [[K4顶点], I_k, 已选颜色]}
        # 异色状态: 0: 未支配, 1: 支配
        # |已染|  0 |  1 |  2 |  3 |  4 |  5 |  6 |异色边|
        # |I_k|2^-5|2^-5|2^-4|2^-3|2^-2|2^-1|2^-0|  0  |
        self.K4_dict = self.find_K4()

        # --- 边 属性 ---
        # 边: {related_K4: [相关K4id], color: [颜色]}
        nx.set_edge_attributes(self.graph, None, "related_K4")  # 为边添加“相关的K4”属性
        nx.set_edge_attributes(self.graph, "None", "color")  # 为边添加“颜色”属性
        for e1, e2 in self.graph.edges:
            self.graph[e1][e2]['related_K4'] = []  # 赋初始空列表
        self.find_related_K4()

    def find_K4(self):
        '''
        寻找4顶点完全子图
        '''
        K4 = [c for c in itertools.combinations(list(self.graph.nodes), 4)]
        K4_dict = {}
        for i in range(len(K4)):
            K4_dict[i] = [K4[i], 2 ** -5, None]  # 初始染色0条 未定颜色
        return K4_dict

    def find_related_K4(self):
        '''
        寻找每条边相关的K4
        '''
        for i in range(len(self.K4_dict)):
            nodes = self.K4_dict[i][0]
            for e1, e2 in itertools.combinations(nodes, 2):
                target = self.graph[e1][e2]['related_K4']
                target.append(i)

    def coloring(self):
        '''
        一种染色算法
        '''
        def update_W(self, e1, e2, color):
            '''
            计算染色 (e1, e2) 为 color 在全局的收益
            '''
            reward = 0
            for k in self.graph[e1][e2]['related_K4']:
                # 计算染色 (e1, e2) 为 color 在 k 中的收益
                if self.K4_dict[k][2] == None:  # 未染色
                    reward += 0
                else:
                    if color == self.K4_dict[k][2]:  # 同色
                        reward += self.K4_dict[k][1]
                    else:  # 异色
                        reward += 0
            return reward

        def color_edge(e1, e2, color):
            '''
            染色 (e1, e2) 为 color, 同时更新相关K4的染色状态
            '''
            self.graph[e1][e2]['color'] = color
            for k in self.graph[e1][e2]['related_K4']:
                if self.K4_dict[k][2] == None:  # 未染色
                    self.K4_dict[k][2] = color
                else:
                    if color == self.K4_dict[k][2]:  # 同色
                        self.K4_dict[k][1] *= 2
                    else:  # 异色
                        self.K4_dict[k][1] = 0

        self.color_sequence = list(self.graph.edges)  # (伪随机的)染色顺序

        for e1, e2 in tqdm(self.color_sequence):  # 比较黑白收益 执行染色
            reward_w = update_W(self, e1, e2, "white")
            reward_b = update_W(self, e1, e2, "black")
            if reward_w < reward_b:
                color_edge(e1, e2, "white")
            else:
                color_edge(e1, e2, "black")

    def draw_graph(self, label=False, legend=True):
        '''
        画图, 同时给边染上不同颜色
        '''
        fig, ax = plt.subplots()
        colors = ["grey" if self.graph[e1][e2]['color'] == "white" else "black"
                  for e1, e2 in self.graph.edges]
        nx.draw(self.graph,
                edge_color=colors,
                width=3,
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

    def compute_k4(self):
        '''
        计算同色K4的数量
        '''
        sum = 0
        for i in range(len(self.K4_dict)):
            colors = [self.graph[n1][n2]['color'] for n1, n2 in itertools.combinations(self.K4_dict[i][0], 2)]
            result = colors.count(colors[0]) == len(colors)
            if result:
                sum += 1
        return sum


if __name__ == '__main__':
    print("------------------------------------------------")

    random.seed(777)
    node = 50  # 生成顶点数
    MK4 = MonochromaticK4(node)

    MK4.coloring()

    MK4.draw_graph(label=False, legend=False)  # TODO: 设计一下可视化方式, 包括但不限于调整配色、单独展示K4、染色顺序等
    plt.show()

    # 计算期望值并与实验结果比较
    expect_value = math.comb(node, 4) * (2 ** -5)
    sum = MK4.compute_k4()
    print('expect_value = ', expect_value, '\nsum = ', sum)
