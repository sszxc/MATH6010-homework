# Author: Ckzzz1
# Date: May 11th, 2022
# Description: Draw results of the Uniform Graph Partition experiment

import UniformGraphPartition
import time
import os
import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    os.chdir(sys.path[0])
    n = 100  # 固定顶点数
    step = []
    test_result = []
    crosssum = []
    for i in range(2, n + 1, 2):  # 测试算法所需时间
        step.append(i)
        t1 = time.time()
        graph = UniformGraphPartition.UGP(i)
        n1, n2, cost, x, cost_list = graph.steepest_ascent()
        t2 = time.time()
        test_result.append(t2 - t1)
        crosssum.append(cost)
    l1 = plt.plot(step, test_result, 'r', label='Time')
    plt.xlabel('Size of Nodes')
    plt.ylabel('Seconds')
    plt.title(f'n = {n}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'time_n={n}_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()
    l2 = plt.plot(step, crosssum, 'r', label='CrossSum')
    plt.xlabel('Size of Nodes')
    plt.title(f'n = {n}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'nodes_n={n}_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()
