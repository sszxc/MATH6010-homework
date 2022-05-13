# Author: Xuechao Zhang
# Date: May 13th, 2022
# Description: a solution of knapsack problem based on SimulatedAnnealing algorithm

import random
import math
from matplotlib import pyplot as plt

def knapsack_problem():
    """
    问题条件
    """
    capacity = 750
    weight_profit = [(70,135),(73,139),(77,149),(80,150),(82,156),(87,163),(90,173),(94,184),\
        (98,192),(106,201),(110,210),(113,214),(115,221),(118,229),(120,240)]
    return capacity, weight_profit

def print_table(weight_profit):
    """
    打印表格
    """
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = ["Index", "Weights", "Profits"]	# 设置标题名称
    for i in range(len(weight_profit)):
        x.add_row([i, *weight_profit[i]])
    print(x)

class SimulatedAnnealing:
    def __init__(self, capacity, weight_profit, temperature = 1000, cooling_rate = 0.996, max_iterations = 1000):
        self.capacity = capacity
        self.weight_profit = weight_profit
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
    
    def init_solution(self):
        """
        随机生成可行解
        """
        solution = []
        choices = list(range(len(self.weight_profit)))
        while len(choices) > 0:
            sample = random.choice(choices)
            if self.is_valid(solution + [sample]):
                solution.append(sample)
                choices.remove(sample)
            else:
                return solution

    def is_valid(self, solution):
        """
        判断解是否有效
        """
        return sum([self.weight_profit[index][0] for index in solution]) <= self.capacity

    def evaluate_solution(self, solution):
        """
        评估解的价值
        """
        return sum([self.weight_profit[index][1] for index in solution])

    def random_neighbor(self, solution):
        """
        随机增删生成一个邻居解
        """
        while True:
            neighbor = solution.copy()
            choices = list(range(len(self.weight_profit)))
            sample = random.choice(choices)
            if sample in solution:
                neighbor.remove(sample)
            else:
                neighbor.append(sample)
            if self.is_valid(neighbor):
                return neighbor

    def solve(self):
        # 初始解
        best_solution = self.init_solution()
        best_solution_value = self.evaluate_solution(best_solution)
        best_ever = best_solution_value  # 记录历史最优解(不一定是输出的解)
        self.history = [best_solution_value]
        
        # 开始迭代
        iterations = 0
        while iterations < self.max_iterations:
            iterations += 1
            self.temperature = self.temperature * self.cooling_rate

            # 随机生成邻居解 并以概率性接收
            neighbor = self.random_neighbor(best_solution)
            neighbor_value = self.evaluate_solution(neighbor)
            if neighbor_value > best_solution_value or \
                random.random() < math.exp((neighbor_value - best_solution_value) / self.temperature):
                best_solution = neighbor.copy()
                best_solution_value = neighbor_value
            if best_solution_value > best_ever:
                best_ever = best_solution_value
            self.history.append(best_solution_value)
            if iterations % 100 == 0:
                print("Iterations:", iterations, 
                    "Temperature:", round(self.temperature, 2), 
                    "Best solution value:", best_solution_value,
                    "(Best ever:", best_ever, ")")
        return best_solution, best_solution_value, best_ever

    def draw_history(self):
        """
        绘制历史数据
        """
        plt.title(r'$\bf{Knapsack\ Problem}$'+'\nSimulated Annealing Algorithm')
        plt.xlabel('Iteration')
        plt.ylabel('Value')
        plt.plot(self.history)
        

if __name__ == '__main__':
    random.seed(777)
    print_table(knapsack_problem()[1])
    SA = SimulatedAnnealing(*knapsack_problem())
    _, _, best = SA.solve()
    SA.draw_history()
    plt.plot(SA.history.index(best), best, 'ro')  # 找出历史最优解
    plt.show()