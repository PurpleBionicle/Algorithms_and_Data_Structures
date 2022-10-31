import fileinput
import re


class Heap():
    def __init__(self):
        # key - index
        self.hash_table = dict()
        # tree[index] - [key - value]
        self.tree: list = []

    def __parent(self, index: int) -> int:
        return (index - 1) >> 1

    def __left_child(self, index: int) -> int:
        return (index << 1) + 1

    def __right_child(self, index: int) -> int:
        return (index << 1) + 2

    def __find_key(self, index: int) -> int:
        for node in self.tree:
            if self.hash_table[node[0]] == index:
                return node[0]

    def __heapify_up(self, index: int) -> None:
        # Поднимаем
        if index == 0:
            return

        parent: int = self.__parent(index)
        while index != 0 or index < self.__parent(index):
            # поменяли в хэше индексы для ключей
            self.hash_table[self.__find_key(index)], \
            self.hash_table[self.__find_key(parent)] = parent, index
            # по индексам поменяем значения и ключи
            self.tree[index], self.tree[parent] = [self.__find_key(parent), self.tree[parent][1]], \
                                                  [self.__find_key(index), self.tree[index][1]]

            index = parent
            parent = self.__parent(parent)

    # TODO
    def __heapify_down(self, index: int) -> None:
        left: int = self.__left_child(index)
        right: int = self.__right_child(index)
        # куда спускаем ????

    def add(self, key: int, value: str) -> None:
        pass

    def delete(self, key: int) -> None:
        pass

    def set(self, key: int, value: str) -> None:
        pass

    def __search(self, key: int) -> list:
        pass

    def search(self, key: int) -> None:
        result: list = self.__search(key)
        print('1 {0} {1}'.format(list[0],list[1]) if result[0] != -1 else '0')

    def min(self)->None:
        pass

    def max(self)->None:
        pass

    def print(self)->None:
        pass

    def extract(self)->None:
        pass

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
