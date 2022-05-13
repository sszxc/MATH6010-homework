# 爬山法求解STS(v)
# by Qu Chendi
import numpy as np
import random
import matplotlib.pyplot as plt
import time

v = 145
X = np.array(range(1, v + 1))
B = []
block_num = 0  # 三元组个数
live_num = np.zeros(v)  # 每个数出现的次数
x_matrix = np.eye(v)  # 0-1矩阵，若点i,j在B的一个三元组中出现过，(i,j)=(j,i)=1
# bn_list = []
# bn_list.append(block_num)
time_start = time.time()
while block_num < (v - 1) * v / 6:
    # SWITCH
    live_id = np.where(live_num < (v - 1) / 2)[0].tolist()
    live_point = X[live_id]  # 更新live_point list
    point = random.choice(live_point)  # 随机取一个
    live_pair = X[np.where(x_matrix[point - 1, :] == 0)[0].tolist()]  # 找出没有相遇过的点
    pair = random.sample(list(live_pair), 2)  # 随机取两个组成live_pair

    if x_matrix[pair[0] - 1, pair[1] - 1] == 0:  # 另外两个数未相遇过，直接添加
        B.append([point, pair[0], pair[1]])

        block_num += 1
        live_num[point - 1] += 1
        live_num[pair[0] - 1] += 1
        live_num[pair[1] - 1] += 1

        x_matrix[point - 1, pair[0] - 1] = 1
        x_matrix[pair[0] - 1, point - 1] = 1
        x_matrix[point - 1, pair[1] - 1] = 1
        x_matrix[pair[1] - 1, point - 1] = 1
        x_matrix[pair[0] - 1, pair[1] - 1] = 1
        x_matrix[pair[1] - 1, pair[0] - 1] = 1
    else:  # 其余两个数之前出现过，加入这一组，去掉之前的
        B.append([point, pair[0], pair[1]])
        for p in B:
            if (pair[0] in p) and (pair[1] in p):
                B.remove(p)
                p.remove(pair[0])
                p.remove(pair[1])
                i = int(p[0])

                live_num[point - 1] += 1
                live_num[i - 1] -= 1

                x_matrix[point - 1, pair[0] - 1] = 1
                x_matrix[pair[0] - 1, point - 1] = 1
                x_matrix[point - 1, pair[1] - 1] = 1
                x_matrix[pair[1] - 1, point - 1] = 1

                x_matrix[i - 1, pair[0] - 1] = 0
                x_matrix[pair[0] - 1, i - 1] = 0
                x_matrix[i - 1, pair[1] - 1] = 0
                x_matrix[pair[1] - 1, i - 1] = 0
                break
    # bn_list.append(block_num)
time_end = time.time()
print('time cost', time_end - time_start, 's')

print(B)
print(block_num)
# i = len(bn_list)
# plt.plot(range(0, i), bn_list)
# plt.xlabel("steps")
# plt.ylabel("Block_num")
# plt.title("v = 43")
# plt.show()
