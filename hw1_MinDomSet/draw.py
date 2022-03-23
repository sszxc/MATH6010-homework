# Author: Ckzzz1
# Date: March 23rd, 2022
# Description: Draw results of the dominating set experiment

from min_dom_set import *
import time
import os
import sys

if __name__ == '__main__':
    os.chdir(sys.path[0])

    probability = 0.1  # 图中边连接概率

    # 图像1
    n = 200  # 固定顶点数
    test_result = []
    test_result2 = []
    theory_result = []
    for delta in range(1, n + 1):  # 改变最小度数
        MDS = MinDominatingSet(n, delta, probability)
        MDS.find_min_dom_set(0)
        test_result.append(len(MDS.min_dom_set))
        MDS.find_min_dom_set(1)
        test_result2.append(len(MDS.min_dom_set))
        theory_result.append(MDS.theoretical_min_dom_set_size)
    x = [i for i in range(1, n + 1)]  # 横坐标
    l1 = plt.plot(x, test_result, 'r', label='Greedy Algorithm')
    l2 = plt.plot(x, test_result2, 'g', label='Better Greedy Algorithm')
    l3 = plt.plot(x, theory_result, 'b', label='Theoretical Size')
    plt.xlabel('Size of Delta')
    plt.ylabel('Size of The Dominating Set')
    plt.title(f'n = {n}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'n={n}_delta_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()

    # 图像2
    delta = 2  # 固定最小度数
    test_result = []
    test_result2 = []
    theory_result = []
    for n in range(delta + 1, delta * 100 + 1):  # 改变顶点数
        MDS = MinDominatingSet(n, delta, probability)
        MDS.find_min_dom_set(0)
        test_result.append(len(MDS.min_dom_set))
        MDS.find_min_dom_set(1)
        test_result2.append(len(MDS.min_dom_set))
        theory_result.append(MDS.theoretical_min_dom_set_size)
    x = [i for i in range(delta + 1, delta * 100 + 1)]  # 横坐标
    l1 = plt.plot(x, test_result, 'r', label='Greedy Algorithm')
    l2 = plt.plot(x, test_result2, 'g', label='Better Greedy Algorithm')
    l3 = plt.plot(x, theory_result, 'b', label='Theoretical Size')
    plt.xlabel('Size of Nodes')
    plt.ylabel('Size of The Dominating Set')
    plt.title(f'delta={delta}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'delta={delta}_n_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()
