import math
import fileinput
import re


class Fillness:
    def __init__(self, weight: int, binary_vector: int):
        self.binary_vector: int = binary_vector
        self.weight: int = weight


class Knapsack:
    def __check_types(self, capacity: int, accuracy: float, weights: list[int], values: list[int]) -> int:
        if accuracy < 0 or accuracy > 1 or type(accuracy) is not float:
            return 0
        if capacity < 0 or type(capacity) is not int:
            return 0
        for value in values:
            if value < 0 or type(value) is not int:
                return 0
        for weight in weights:
            if weight < 0 or type(weight) is not int:
                return 0
        if len(weights) < 0 or len(values) < 0:
            return 0
        return 1

    def __check_weights(self) -> None:
        for i in range(len(self.values)):
            if self.weights[i] > self.capacity:
                self.values.remove(self.values[i])
                self.weights.remove(self.weights[i])

    def __init__(self, capacity: int, accuracy: float, weights: list[int], values: list[int]):
        result: int = self.__check_types(capacity, accuracy, weights, values)
        if result:
            self.accuracy: float = accuracy
            self.capacity: int = int(capacity)
            self.weights: list[int] = weights
            self.original_values: list[int] = values
            self.size: int = 0
            self.approximation_ratio_ = len(self.original_values) / (self.accuracy * max(self.original_values))
            self.values: list[int] = [int(x * self.approximation_ratio_) for x in self.original_values]
        else:
            raise Exception('error')

        self.__check_weights()
        self.fillness = Fillness(0, 0)

    def download(self):
        all_costs: int = sum(self.values)
        table = [Fillness(self.capacity + 1, 0) for _ in range(all_costs + 1)]
        table[0] = Fillness(0, 0)
        i: int = 0
        while i < len(self.values):
            j: int = all_costs
            while j >= self.values[i]:

                if self.weights[i] + table[j - self.values[i]].weight < table[j].weight:
                    table[j].weight = table[j - self.values[i]].weight
                    table[j].binary_vector = table[j - self.values[i]].binary_vector
                    table[j].weight += self.weights[i]
                    table[j].binary_vector |= 1 << i
                j -= 1
            i += 1

        # выберем лучшую стоимость
        for i in range(len(table) - 1, 0, -1):
            if table[i].weight <= self.capacity:
                self.fillness = table[i]
                return i, table[i]

    def __str__(self):
        answer: str = f'{self.fillness.weight} '
        items: str = ''
        cost: int = 0
        i: int = 0
        while i < self.capacity:
            if self.fillness.binary_vector & 1:
                items += f'{i + 1}\n'
                cost += self.original_values[i]
            i += 1
            self.fillness.binary_vector >>= 1  # //2
        answer += f'{str(cost)}\n'
        return answer + items


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

    try:
        knapsack = Knapsack(capacity, accuracy, weights, values)
        knapsack.download()
        print(knapsack)
    except Exception as error:
        print(error)
