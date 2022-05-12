# Author: Ckzzz1
# Date: May 11th, 2022
# Description: Steepest Ascent for uniform graph partition

import numpy as np
import time
import matplotlib.pyplot as plt
import os
import sys


class UGP():
    def __init__(self, nodes=10):
        self.nodes = nodes
        self.edges = np.random.rand(nodes, nodes) * 100  # 初始化边的权值
        for i in range(nodes):
            self.edges[i][i] = 0  # 对角线置0
        for i in range(1, nodes):
            for j in range(0, i):
                self.edges[i][j] = self.edges[j][i]  # 对角矩阵

    def change(self, n1, n2):  # 遍历交换一次顶点
        max_gain = 0
        a, b = [0, 0]
        for i in range(n1.size):
            for j in range(n2.size):  # 只考虑局部变化，减少代码运行时间
                gain = -(sum(self.edges[m][n1[i]] for m in n1) - sum(self.edges[m][n1[i]] for m in n2) + sum(
                    self.edges[m][n2[j]] for m in n2) - sum(self.edges[m][n2[j]] for m in n1) + 2 * self.edges[n1[i]][
                             n2[j]])
                if gain > max_gain:
                    max_gain = gain
                    a, b = [i, j]
        return max_gain, a, b

    def steepest_ascent(self):  # 爬山法
        n = np.arange(self.nodes)
        np.random.shuffle(n)
        n1, n2 = np.split(n, 2)
        cost = sum(self.edges[m][n] for m in n1 for n in n2)
        i = 1
        cost_list = [cost]
        while True:
            max_gain, a, b = self.change(n1, n2)
            if max_gain == 0:  # 局部最优时停止
                break
            else:
                n1 = np.append(n1, n2[b])
                n2 = np.append(n2, n1[a])
                n1 = np.delete(n1, a)
                n2 = np.delete(n2, b)
                cost -= max_gain
                i += 1
                cost_list.append(cost)
        return n1, n2, cost, [m for m in range(i)], cost_list


if __name__ == '__main__':
    nodes = 100
    t1 = time.time()
    graph = UGP(nodes)
    n1, n2, cost, x, cost_list = graph.steepest_ascent()
    t2 = time.time()
    print(f'edges = {graph.edges} \n')
    print(f'n1 = {n1} \n')
    print(f'n2 = {n2} \n')
    print(f'cost = {cost} \n')
    print(f'time = {t2 - t1} seconds')
    os.chdir(sys.path[0])
    l1 = plt.plot(x, cost_list, 'r', label='CrossSum')
    plt.xlabel('Steps')
    plt.title(f'n = {nodes}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'n={nodes}_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()
