import fileinput
import re
import math


class Fillness:
    def __init__(self, binary_vector: int, cost: int):
        self.binary_vector: int = binary_vector
        self.cost: int = cost


class Knapsack:
    def __init__(self, capacity: int, accuracy: float, weights: list[int], values: list[int]):
        self.capacity = capacity
        self.accuracy = accuracy  # e
        self.values: list[int] = values
        self.weights: list[int] = weights
        self.size: float = 0
        self.__fullness: int = 0  # строка в бинарном представлении
        # k = (max(self.values) * (1 - self.accuracy)) / len(self.values)
        k = 1 - self.accuracy
        self.capacity = int(self.capacity * k)
        for i in range(len(self.weights)):
            self.weights[i] = round(float(self.weights[i]) * k) + 1

    def download(self):
        n = len(self.values)
        memory = [[Fillness(0, 0) for _ in range(self.capacity + 1)] for __ in range(n + 1)]
        for i in range(n + 1):
            for w in range(self.capacity + 1):
                if i == 0 or w == 0:
                    memory[i][w].cost = 0
                elif self.weights[i - 1] <= w:
                    if self.values[i - 1] + memory[i - 1][w - self.weights[i - 1]].cost > memory[i - 1][w].cost:
                        memory[i][w].cost = self.values[i - 1] + memory[i - 1][w - self.weights[i - 1]].cost
                        # K[i][w].binary_vector |= 1 << i - 1
                        memory[i][w].binary_vector = memory[i - 1][w - self.weights[i - 1]].binary_vector | (1 << i - 1)
                    else:
                        memory[i][w].cost = memory[i - 1][w].cost
                        memory[i][w].binary_vector = memory[i - 1][w].binary_vector

                else:
                    memory[i][w] = memory[i - 1][w]
                    memory[i][w].binary_vector = memory[i - 1][w].binary_vector

        # надо откатиться до последней ячейки с такой же стоимостью
        for i in range(self.capacity):
            if memory[n][self.capacity - i] == memory[n][self.capacity]:
                continue
            else:
                self.__fullness = memory[n][self.capacity - i + 1].binary_vector
                self.cost = memory[n][self.capacity - i + 1].cost
                self.size = self.capacity - i + 1
                break

        return memory[n][self.capacity]

    def __str__(self):
        answer: str = f'{self.size} {self.cost}\n'
        i: int = 0
        while i < self.capacity:
            if self.__fullness & 1:
                answer += f'{i + 1}\n'
            i += 1
            self.__fullness >>= 1  # //2
        return answer


if __name__ == '__main__':
    accuracy = float(input())
    capacity = int(input())
    weights: list[int] = []
    values: list[int] = []

    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == '':
            continue
        elif re.search('\d+ \d+', line):
            weight, cost = line.split(' ')
            weights.append(int(weight))
            values.append(int(cost))
        else:
            print('error')
    knapsack = Knapsack(capacity, accuracy, weights, values)
    knapsack.download()
    print(knapsack)
