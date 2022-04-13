# Author: Ckzzz1
# Date: April 13rd, 2022
# Description: Draw results of the monochromatic Kn experiment

import monochromatic_k4
import monochromatic_k4_old
import time
import os
import sys
import matplotlib.pyplot as plt


if __name__ == '__main__':
    os.chdir(sys.path[0])
    n = 50  # 固定顶点数
    test_result = []
    test2_result = []
    for i in range(4, n):  # 测试旧方法所需时间
        t1 = time.time()
        MK4_old = monochromatic_k4_old.MonochromaticK4(i, 1)
        MK4_old.coloring()
        t2 = time.time()
        test_result.append(t2 - t1)
    for i in range(4, n):  # 测试优化后方法所需时间
        t1 = time.time()
        MK4 = monochromatic_k4.MonochromaticK4(i)
        MK4.coloring()
        t2 = time.time()
        test2_result.append(t2 - t1)
    x = [i for i in range(4, n)]  # 横坐标
    l1 = plt.plot(x, test_result, 'r', label='Before Refinement')
    l2 = plt.plot(x, test2_result, 'b', label='After Refinement')
    plt.xlabel('Size of Nodes')
    plt.ylabel('Seconds')
    plt.title(f'n = {n}')
    plt.legend(loc='best')
    localtime = time.localtime(time.time())
    plt.savefig(f'n={n}_{localtime.tm_mon}_{localtime.tm_mday}_{localtime.tm_hour}_{localtime.tm_min}.jpg')
    plt.close()
