import fileinput


class Knapsack:
    def __check_params(self, accuracy, capacity) -> bool:
        return not (accuracy < 0 or accuracy > 1 or type(accuracy) is not float) and not (
                capacity < 0 or type(capacity) is not int)

    def __check_items(self, weight: int, value: int) -> bool:
        return weight >= 0 and value >= 0

    def __init__(self):
        self.accuracy: float = 0.0
        self.capacity: int = 0
        self.items: list[[int, int]] = []
        self.table: list = []

    def set_params(self, accuracy: float, capacity: int) -> None:
        if self.__check_params(accuracy, capacity):
            self.accuracy = accuracy
            self.capacity = capacity
        else:
            raise Exception('error')

    def add_item(self, weight: int, value: int):
        if self.__check_items(weight, value):
            self.items.append((value, weight))

    def __find_answer_items(self, new_values: list, target_price: int) -> None:
        self.final_weight = self.table[len(self.items)][target_price]
        self.answer = []
        self.original_price = 0
        for i in range(len(self.items), 0, -1):
            if self.table[i - 1].get(target_price) is None or \
                    self.table[i - 1][target_price] > self.table[i][target_price]:
                self.answer.append(i)
                self.original_price += self.items[i - 1][0]
                target_price -= new_values[i - 1][0]

    def download(self) -> None:
        if len(self.items) == 0:
            raise Exception('error')
        else:
            new_values: list[[int, int]] = []
            if self.accuracy != 0:
                max_value: int = max(item[0] for item in self.items)
                self.approximation: float = len(self.items) / (self.accuracy * max_value)
                for item in self.items:
                    new_values.append((int(item[0] * self.approximation), item[1]))
            else:
                new_values = self.items

            count = 0  # Номер строки в таблице
            self.table.append({0: 0})  # инициализирующее число
            target_price = 0

            for item in new_values:
                count += 1
                self.table.append(self.table[count - 1].copy())
                #  пока в новой строке все старое, но пройдя ее будем менять клеточки
                for previous_item in self.table[count - 1].items():
                    if self.table[count].get(previous_item[0] + item[0]) is None:
                        if previous_item[1] + item[1] <= self.capacity:
                            self.table[count][previous_item[0] + item[0]] = previous_item[1] + item[1]
                            if target_price < previous_item[0] + item[0]:
                                target_price = previous_item[0] + item[0]
                    else:
                        if self.table[count - 1][previous_item[0] + item[0]] > previous_item[1] + item[1]:
                            self.table[count][previous_item[0] + item[0]] = previous_item[1] + item[1]

        self.__find_answer_items(new_values, target_price)

    def __str__(self):
        self.answer = reversed(self.answer)
        return f'{self.final_weight} {self.original_price}\n' + '\n'.join(str(x) for x in self.answer)


def input_(knapsack: Knapsack, accuracy, capacity, line: str):
    line = line.replace('\n', '')
    if line == '':
        return

    split: list[str] = line.split(' ')

    if accuracy is None:
        if len(split) == 1:
            accuracy = float(line)
            return accuracy, capacity
        else:
            print('error')

    elif capacity is None:
        if len(split) == 1:
            capacity = int(line)
            return accuracy, capacity
        else:
            raise Exception('error')

    else:
        knapsack.set_params(accuracy, capacity)
        if len(split) == 2:
            try:
                knapsack.add_item(int(split[0]), int(split[1]))
                return accuracy, capacity
            except Exception as error:
                raise Exception(error)
        else:
            raise Exception('error')


def main():
    knapsack = Knapsack()
    accuracy = None
    capacity = None
    for line in fileinput.input():
        if line == 'exit\n':
            break
        try:
            accuracy, capacity = input_(knapsack, accuracy, capacity, line)
        except Exception as e:
            print(e)
    knapsack.download()
    print(knapsack)


if __name__ == '__main__':
    main()
