import fileinput
import re

class Item:
    def __init__(self, weight: int, cost: int):
        self.weight: int = weight
        self.cost: int = cost
        self.unit_cost: float = cost / weight
        self.index = 0

    def __iter__(self, other):
        return self.unit_cost > other.unit_cost


class Knapsack:
    def __init__(self, capacity: float, accuracy: float):
        self.capacity = capacity
        self.accuracy = accuracy
        self.all_item: list[Item] = []
        self.size: float = 0
        self.indexes: list[int] = []
        self.cost: float = 0

    def add_item(self, item: Item) -> None:
        item.index = len(self.all_item) + 1
        self.all_item.append(item)
        self.size += item.weight
        self.cost += item.cost

    def __right_accuracy(self, a: float, b: float) -> bool:
        return a < b and a / b <= self.accuracy

    def __find_fullness(self) -> list[Item]:
        fullness: list[Item] = self.all_item.sort(key=lambda elem: elem.unit_cost)
        if self.size <= self.capacity:
            return fullness
        else:
            for item in fullness:
                if self.__right_accuracy(self.size - item.cost, self.capacity):
                    fullness.remove(item)
                    break
                else:
                    continue
            return fullness

    def fullness(self) -> str:
        items: list[Item] = self.__find_fullness()
        answer: str = f'{self.size} {self.cost}\n'
        for item in items:
            answer += f'{item.index}\n'
        return answer


def digit_input() -> float | int:
    element = None
    while element is None:
        input_ = input()
        element = float(input_) if input_ != '' and input_.isdigit() else None
    return element


if __name__ == '__main__':

    capacity = digit_input()
    accuracy = digit_input()

    knapsack = Knapsack(capacity, accuracy)
    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == '':
            continue
        elif re.search('\d+ \d+',line):
            weight, cost = line.split(' ')
            knapsack.add_item(Item(weight, cost))
        else:
            print('error')
    print(knapsack.fullness())
