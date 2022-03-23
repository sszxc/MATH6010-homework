# Author: Xuechao Zhang
# Date: March 20th, 2022
# Description: Test Min Dominating Set Theorem on Different Scales

from min_dom_set import *
import datetime
import os
import sys

if __name__ == '__main__':
    os.chdir(sys.path[0])

    for i in range(20):
        # 生成随机图
        n = random.randint(5,50)  # 定义顶点数量
        delta = random.randint(1,int(n/2))  # 最小度
        probability = 0.1  # 图中边连接概率
        MDS = MinDominatingSet(n, delta, probability)

        # 寻找最小支配集
        MDS.find_min_dom_set()
        
        # 与理论最大值比较
        print("The result has", len(MDS.min_dom_set), "vertices.", end=" ")
        print("Theoretically it has at most", MDS.theoretical_min_dom_set_size, "vertices.")

        # 画图
        plt = MDS.draw_graph()
        plt.savefig('result_'+str(n)+'_'+str(delta)+'_'+
                    str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)+
                    '.jpg')
        # plt.show()
        plt.clf()