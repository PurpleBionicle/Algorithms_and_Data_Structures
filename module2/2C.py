import fileinput
import re


class Node():
    def __init__(self, key: int, value: str):
        self.key: int = key
        self.value: str = value

    def __str__(self):
        return f'{self.key} {self.value}'


class Heap():
    def __init__(self):
        # key - index
        self.hash_table = dict()
        # tree[index] - [key ,value]
        self.tree: list = []

    def __str__(self):
        result: str = ''

        def __print_(count: int) -> str:
            answer: str = ''
            for i in range(count):
                answer += ' _'
            return answer

        if len(self.tree) == 0:
            return '_'

        result += f'[{self.tree[0].key} {self.tree[0].value}]'

        index_current_level: int = 1
        level_size: int = 2
        while index_current_level < len(self.tree):
            result += '\n'
            if index_current_level + level_size < len(self.tree):
                for level_position in range(level_size):
                    if level_position != 0:
                        result += ' '
                    current_elem: Node = self.tree[index_current_level + level_position]
                    parent: int = self.__parent(index_current_level + level_position)
                    result += f'[{current_elem.key} {current_elem.value} {self.tree[parent].key}]'
            else:
                # Для последнего уровня
                shift: int = len(self.tree) - index_current_level
                for level_position in range(shift):
                    if level_position != 0:
                        result += ' '
                    current_elem: Node = self.tree[index_current_level + level_position]
                    parent: int = self.__parent(index_current_level + level_position)
                    result += f'[{current_elem.key} {current_elem.value} {self.tree[parent].key}]'

                result += __print_(level_size - shift)

            index_current_level += level_size
            level_size <<= 1
        return result

    def __parent(self, index: int) -> int | None:
        return (index - 1) >> 1 if (index - 1) >> 1 >= 0 else None

    def __left_child(self, index: int) -> int | None:
        #   0
        #  1   2
        # 3 4 5 6
        return (index << 1) + 1 if (index << 1) + 1 < len(self.tree) else None

    def __right_child(self, index: int) -> int | None:
        return (index << 1) + 2 if (index << 1) + 2 < len(self.tree) else None

    def __heapify_up(self, index: int) -> None:
        # Поднимаем
        if index == 0:
            return

        parent = self.__parent(index)
        while index != 0 and parent is not None and self.tree[index].key < self.tree[parent].key:
            # поменяли в хэше индексы для ключей
            self.hash_table[self.tree[index].key], \
            self.hash_table[self.tree[parent].key] = parent, index
            # по индексам поменяем значения и ключи
            self.tree[index], self.tree[parent] = self.tree[parent], self.tree[index]

            index = parent
            parent = self.__parent(parent)

    def __heapify_down(self, index: int) -> None:
        left = self.__left_child(index)
        right = self.__right_child(index)
        while left is not None:
            if right is not None:  # если есть оба ребенка
                # если дети больше = дошли до куда надо
                if self.tree[index].key < self.tree[left].key and \
                        self.tree[index].key < self.tree[right].key:
                    break

                elif self.tree[left].key < self.tree[right].key:  # если правый больше, то поменяем с левом
                    self.hash_table[self.tree[index].key], self.hash_table[self.tree[left].key] = \
                        left, index
                    self.tree[left], self.tree[index] = self.tree[index], self.tree[left]
                    index = left
                else:  # если левый больше, то поменяем с правом
                    self.hash_table[self.tree[index].key], self.hash_table[self.tree[right].key] = \
                        right, index
                    self.tree[right], self.tree[index] = self.tree[index], self.tree[right]
                    index = right
            else:  # если только левый есть
                if self.tree[index].key < self.tree[left].key:
                    break
                else:
                    self.hash_table[self.tree[index].key], self.hash_table[self.tree[left].key] = \
                        left, index
                    self.tree[left], self.tree[index] = self.tree[index], self.tree[left]
                    index = left

            left = self.__left_child(index)
            right = self.__right_child(index)

    def add(self, key: int, value: str) -> None:
        if key in self.hash_table:
            raise Exception('error')  # Если уже есть
        self.tree.append(Node(key, value))
        self.hash_table[key] = len(self.tree) - 1
        self.__heapify_up(len(self.tree) - 1)

    def delete(self, key: int) -> None | int:
        if len(self.tree) == 0:
            raise Exception('error')
        # если есть
        # поменяли в хэше индексы для ключей
        try:
            index: int = self.hash_table[key]
        except Exception:
            raise Exception('error')

        self.tree[index], self.tree[-1] = self.tree[-1], self.tree[index]
        self.hash_table[self.tree[index].key] = index
        self.tree.pop()
        if len(self.tree) > 0 and len(self.tree) != index:
            parent = self.__parent(index)
            if parent is not None:
                if self.tree[index].key < self.tree[parent].key:
                    self.__heapify_up(index)
                else:
                    self.__heapify_down(index)
            else:
                self.__heapify_down(index)

        del self.hash_table[key]
        return 1

    def set(self, key: int, value: str) -> int | None:
        try:
            index, old_value = self.search(key)
        except Exception as error:
            raise Exception(error)
        self.hash_table[key] = index
        self.tree[index].value = value
        return 1

    def search(self, key: int) -> None | tuple[int, str]:
        try:
            index = self.hash_table[key]
            return index, self.tree[index].value
        except Exception:
            raise Exception('error')

    def min(self) -> tuple[Node, int] | None:
        if len(self.tree) == 0:
            raise Exception('error')
        else:
            return self.tree[0], 0

    def max(self) -> None | tuple[Node, int]:
        if len(self.tree) == 0:
            raise Exception('error')
        current_max: Node = self.tree[0]
        index: int = 0
        for i in range(len(self.tree), 0, -1):
            # смотрим только листья дерева
            if self.__left_child(i - 1) is not None or \
                    self.__right_child(i - 1) is not None:
                return current_max, index

            if self.tree[i - 1].key > current_max.key:
                current_max = self.tree[i - 1]
                index = i - 1
        return current_max, index

    def extract(self) -> None | Node:
        if len(self.tree) == 0:
            raise Exception('error')
        # если есть
        result: Node = self.tree[0]
        # поменяли в хэше индексы для ключей
        self.hash_table[self.tree[-1].key] = 0

        self.tree[0], self.tree[-1] = self.tree[-1], self.tree[0]
        self.tree.pop()
        self.__heapify_down(0)
        del self.hash_table[result.key]
        return result


if __name__ == '__main__':

    heap = Heap()
    for line in fileinput.input():
        line = line.replace('\n', '')

        if re.search('add \S+ \S*', line):
            params: list = line.split(' ')
            try:
                heap.add(int(params[1]), params[2])
            except Exception as error:
                print(error)

        elif re.search('set \S+ \S*', line):
            params: list = line.split(' ')
            try:
                heap.set(int(params[1]), params[2])
            except Exception as error:
                print(error)

        elif re.search('delete \S+', line):
            params: list = line.split(' ')
            try:
                heap.delete(int(params[1]))
            except Exception as error:
                print(error)

        elif re.search('search \S+', line):
            params: list = line.split(' ')
            try:
                result: tuple = heap.search(int(params[1]))
                print(f'1 {result[0]} {result[1]}')
            except Exception:
                print('0')

        elif line == 'min':
            try:
                result = heap.min()
                print(result[0].key, result[1], result[0].value)
            except Exception as error:
                print(error)

        elif line == 'max':
            try:
                result = heap.max()
                print(result[0].key, result[1], result[0].value)
            except Exception as error:
                print(error)

        elif line == 'print':
            print(heap)

        elif line == 'extract':
            try:
                node: Node = heap.extract()
                print(f'{node.key} {node.value}')
            except Exception as error:
                print(error)

        elif line == '':
            continue

        else:
            print('error')
