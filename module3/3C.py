# import fileinput
# import re
#
#
# class Item:
#     def __init__(self, weight: int, cost: int):
#         self.weight: int = weight
#         self.cost: int = cost
#
#
# class Knapsack:
#     def __init__(self, capacity: float, accuracy: float):
#         self.capacity = capacity
#         self.accuracy = accuracy
#         self.all_item: list[Item] = []
#         self.size: float = 0
#         self.indexes: list[int] = []
#         self.cost: float = 0
#         self.__fullness: int = 0  # строка в бинарном представлении
#
#     def _fill(self, items):
#         # number, capacity, weight_cost, scaling_factor = 4
#         # new_capacity = int(float(capacity) / scaling_factor)
#         # new_weight_cost = [(round(float(weight) / scaling_factor) + 1, cost) for weight, cost in weight_cost]
#         # return dynamic_programming(number, new_capacity, new_weight_cost)
#         # FPTAS
#         #TODO REVIEW
#         new_capasity: int = int(self.capacity * self.accuracy)
#         new_items = self.all_item
#         for item in new_items:
#
#
#     def fill(self, items: list[Item]) -> None:
#         class Weight_and_binar_of_fillness:
#             def __init__(self, weight: int = 0, binar: int = 0):
#                 self.weight: int = weight
#                 self.binar: int = binar
#
#         def __sum_costs(items: list[Item]) -> int:
#             sum: int = 0
#             for item in items:
#                 sum += item.cost
#             return sum
#
#         all_costs: int = __sum_costs(items)
#         vector_of_costs: list[Weight_and_binar_of_fillness] = []
#         vector_of_costs[0] = Weight_and_binar_of_fillness(0, 0)
#
#         i: int = 0
#         j: int = all_costs
#         while i < len(items):
#             while j >= items[i].cost:
#                 if items[i].weight + vector_of_costs[j - items[i].cost].weight < vector_of_costs[j].weight:
#                     vector_of_costs[j] = vector_of_costs[j - items[i].cost]
#                     vector_of_costs[j].weight += items[i].weight
#                     vector_of_costs[j].binar |= 1 << i
#                 j -= 1
#             i += 1
#
#         # выберем лучшую стоимость
#         for i in range(0, vector_of_costs, -1):
#             if vector_of_costs[i] <= self.capacity:
#                 return i, vector_of_costs[i]
#
#     def __str__(self):
#         answer: str = f'{self.size} {self.cost}\n'
#         i: int = 0
#         while i < self.capacity:
#             if self.__fullness & 1:
#                 answer += f'{i + 1}\n'
#             i += 1
#             self.__fullness >>= 1  # //2
#         return answer
#
#
# def digit_input() -> float | int:
#     element = None
#     while element is None:
#         input_ = input()
#         element = float(input_) if input_ != '' and input_.isdigit() else None
#     return element
#
#
# if __name__ == '__main__':
#
#     capacity = digit_input()
#     accuracy = digit_input()
#     knapsack = Knapsack(capacity, accuracy)
#     items: list[Item] = []
#
#     for line in fileinput.input():
#         line = line.replace('\n', '')
#
#         if line == '':
#             continue
#         elif re.search('\d+ \d+', line):
#             weight, cost = line.split(' ')
#             items.append(Item(weight, cost))
#         else:
#             print('error')
#     knapsack.fill(items)
#     print(knapsack)
import math


class Fillness:
    def __init__(self, binary_vector: int, cost: int):
        self.binary_vector: int = binary_vector
        self.cost: int = cost


def knapSack(W, wt, val, n):
    K = [[Fillness(0, 0) for x in range(W + 1)] for x in range(n + 1)]
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w].cost = 0
            elif wt[i - 1] <= w:
                # K[i][w].cost = max(val[i - 1] + K[i - 1][w - wt[i - 1]].cost, K[i - 1][w].cost)
                if val[i - 1] + K[i - 1][w - wt[i - 1]].cost > K[i - 1][w].cost:
                    K[i][w].cost = val[i - 1] + K[i - 1][w - wt[i - 1]].cost
                    # K[i][w].binary_vector |= 1 << i - 1
                    K[i][w].binary_vector = K[i - 1][w - wt[i - 1]].binary_vector | (1 << i - 1)
                else:
                    K[i][w].cost = K[i - 1][w].cost
                    K[i][w].binary_vector = K[i - 1][w].binary_vector

            else:
                K[i][w] = K[i - 1][w]
                K[i][w].binary_vector = K[i - 1][w].binary_vector
    return K[n][W]


if __name__ == '__main__':
    # 165
    # 1 2 3 4 6
    values = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
    # weights = [6, 4, 3, 2, 5]
    weights = [23, 31, 29, 44, 53, 28, 63, 85, 89, 92]
    # values = [5, 3, 1, 3, 6]
    e = 0.001
    k = (max(values) * (1 - e)) / len(values)
    W = int(165 * k)
    for i in range(len(weights)):
        weights[i] = round(float(weights[i]) * k) + 1
    # W = 15
    Fillness = knapSack(W, weights, values, len(values))
    print(Fillness.cost, Fillness.binary_vector)
