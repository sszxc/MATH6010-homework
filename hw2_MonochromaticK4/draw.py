# Author: Ckzzz1
# Date: April 11th, 2022
# Description: Draw results of the monochromatic Kn experiment

from monochromatic_k4 import *
import time
import os
import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    os.chdir(sys.path[0])
    probability = 1  # 图中边连接概率
    n = 50  # 固定顶点数
    test_result = []
    theory_result = []
    for i in range(4, n):  # 改变最小度数
        MK4 = MonochromaticK4(i, 1)
        MK4.coloring()
        expect_value = math.comb(i, 4) * (2 ** -5)
        sum = MK4.compute_k4()
        test_result.append(sum)
        theory_result.append(expect_value)
    x = [i for i in range(4, n)]  # 横坐标
    l1 = plt.plot(x, test_result, 'r', label='Conditional Probability Algorithm')
    l3 = plt.plot(x, theory_result, 'b', label='Theoretical Bound')
    plt.xlabel('Size of Nodes')
    plt.ylabel('Size of The Monochromatic K4')
    plt.title(f'n = {n}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'n={n}_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()
