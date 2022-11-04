import fileinput
import re
from typing import Any


class Heap():
    def __init__(self):
        # key - index
        self.hash_table = dict()
        # tree[index] - [key - value]
        self.tree: list = []

    def __parent(self, index: int) -> int:
        return (index - 1) >> 1

    def __left_child(self, index: int) -> int:
        #   0
        #  1   2
        # 3 4 5 6
        return (index << 1) + 1

    def __right_child(self, index: int) -> int:
        return (index << 1) + 2

    def __heapify_up(self, index: int) -> None:
        # Поднимаем
        if index == 0:
            return

        parent: int = self.__parent(index)
        while index != 0 or index < self.__parent(index):
            # поменяли в хэше индексы для ключей
            self.hash_table[self.tree[index][0]], \
            self.hash_table[self.tree[index][parent]] = parent, index
            # по индексам поменяем значения и ключи
            self.tree[index], self.tree[parent] = [self.tree[index][parent], self.tree[parent][1]], \
                                                  [self.tree[index][0], self.tree[index][1]]

            index = parent
            parent = self.__parent(parent)

    def __heapify_down(self, index: int) -> None:
        left: int = self.__left_child(index)
        right: int = self.__right_child(index)
        while left < len(self.tree):
            if right < len(self.tree):  # если есть оба ребенка
                # если дети больше = дошли до куда надо
                if self.tree[index][0] < self.tree[left][0] and \
                        self.tree[index][0] < self.tree[right][0]:
                    break

                elif self.tree[left][0] < self.tree[right][0]:  # если правый больше, то поменяем с левом
                    self.hash_table[self.tree[index][0]], self.hash_table[self.tree[left][0]] = \
                        left, index
                    self.tree[left], self.tree[index] = self.tree[index], self.tree[left]
                    index = left
                else:  # если левый больше, то поменяем с правом
                    self.hash_table[self.tree[index][0]], self.hash_table[self.tree[right][0]] = \
                        right, index
                    self.tree[right], self.tree[index] = self.tree[index], self.tree[right]
                    index = right
            else:  # если только левый есть
                if self.tree[index][0] < self.tree[left][0]:
                    break
                else:
                    self.hash_table[self.tree[index][0]], self.hash_table[self.tree[left][0]] = \
                        left, index
                    self.tree[left], self.tree[index] = self.tree[index], self.tree[left]
                    index = left

            left: int = self.__left_child(index)
            right: int = self.__right_child(index)

    def add(self, key: int, value: str) -> None:
        self.tree.append([key, value])
        self.hash_table[key] = value
        self.__heapify_up(len(self.tree) - 1)

    def delete(self, key: int) -> None:
        if len(self.tree) == 0 or self.__search(key) == -1:
            print('error')
            return
        # если есть
        # поменяли в хэше индексы для ключей
        index: int = self.hash_table[key]
        self.tree[index], self.tree[-1] = self.tree[-1], self.tree[index]

        self.tree.pop()
        if self.tree[index][1] < self.tree[self.__parent(index)][1]:
            self.__heapify_up(index)
        else:
            self.__heapify_down(index)

        del self.hash_table[key]

    def set(self, key: int, value: str) -> int:
        index: int = self.__search(key)[0]
        if index == -1:
            print('error')
            return -1
        self.hash_table[key] = index
        self.tree[index][1] = value
        return 1

    def __search(self, key: int) -> list[int] | tuple[int, Any]:
        index: int = self.hash_table[key]
        if index is None:
            print('error')
            return [-1]
        else:
            # индекс + значение
            return index, self.tree[index][1]

    def search(self, key: int) -> None:
        result: list = self.__search(key)
        print('1 {0} {1}'.format(list[0], list[1]) if result[0] != -1 else '0')

    def min(self) -> None:
        if len(self.tree) == 0:
            print('error')
        else:
            print(self.tree[0])

    def max(self) -> tuple[int, int, Any] | None:
        if len(self.tree) == 0:
            print('error')
            return
        current_max: list = []
        for i in range(len(self.tree), 0, -1):
            # смотрим только листья дерева
            if self.tree[self.__left_child(i)] is not None or \
                    self.tree[self.__right_child(i)] is not None:
                return current_max[1], i + len(self.tree), current_max[0]

            if self.tree[i] > current_max:
                current_max = self.tree

    def extract(self) -> list:
        if len(self.tree) == 0:
            print('error')
            return
        # если есть
        result: list = self.tree[0]
        # поменяли в хэше индексы для ключей
        self.hash_table[self.tree[-1][0]] = 0

        self.tree[0], self.tree[-1] = self.tree[-1], self.tree[0]
        self.tree.pop()
        self.__heapify_down(0)
        del self.hash_table[result[0]]
        return result

    # TODO
    def print(self) -> None:
        def __print_(count: int) -> None:
            for i in range(count):
                print(' _', end='')

        if len(self.tree) == 0:
            print('_')
            return

        print('[{0} {1}]'.format(self.tree[0][0], self.tree[0][1]), end='')

        index: int = 0
        level_size: int = 2
        while index < len(self.tree):
            print('')  # \n
            if index + level_size < len(self.tree):
                for level_position in range(level_size):
                    if level_position != 0:
                        print(' ', end='')
                        current_elem: list = self.tree[index + level_position]
                        parent: int = self.__parent(index + level_position)
                        print('[{0} {1} {2}]'.format(current_elem[0], current_elem[1], self.tree[parent][0]), end='')
            else:
                diff: int = len(self.tree) - index
                for level_position in range(diff):
                    if level_position != 0:
                        print(' ', end='')
                    current_elem: list = self.tree[index + level_position]
                    parent: int = self.__parent(index + level_position)
                    print('[{0} {1} {2}]'.format(current_elem[0], current_elem[1], self.tree[parent][0]), end='')

                __print_(level_size - diff)

            index += level_size
            level_size <<= 1


if __name__ == '__main__':

    heap = Heap()
    # add K V, set K V, delete K, search K, min, max, extract или print
    for line in fileinput.input():
        line = line.replace('\n', '')

        if re.search('add \S{1}\S* \S*', line):
            params: list = line.split(' ')
            heap.add(int(params[1]), params[2])

        elif re.search('set \S{1}\S* \S*', line):
            params: list = line.split(' ')
            heap.set(int(params[1]), params[2])

        elif re.search('delete \S{1}\S*', line):
            params: list = line.split(' ')
            heap.delete(int(params[1]))

        elif re.search('search \S{1}\S*', line):
            params: list = line.split(' ')
            heap.search(int(params[1]))

        elif line == 'min':
            heap.min()

        elif line == 'max':
            heap.max()

        elif line == 'print':
            heap.print()

        elif line == 'extract':
            heap.extract()

        elif line == '':
            continue

        else:
            print('error')
