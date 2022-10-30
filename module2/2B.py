import fileinput
import re


class Node:
    def __init__(self, key: int, value: str):
        self.parent: Node = None
        self.left: Node = None
        self.right: Node = None
        self.key: int = key
        self.value: str = value


class SplayTree():
    def __init__(self):
        self.root = None

    def __zig(self, node: Node) -> None:
        parent: Node = node.parent
        if parent.parent is not None:
            grandparent: Node = parent.parent
            # определяем какой ребенок
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node

        if parent.left == node:
            right_tree: Node = node.right
            parent.left = right_tree
            if right_tree is not None:
                right_tree.parent = parent
            node.right = parent
            node.parent = parent.parent
            parent.parent = node
        else:
            left_tree: Node = node.left
            parent.right = left_tree
            if left_tree is not None:
                left_tree.parent = parent
            node.left = parent
            node.parent = parent.parent
            parent.parent = node

    def __zig_zig(self, node: Node) -> None:
        self.__zig(node.parent)
        self.__zig(node)

    def __zig_zag(self, node: Node) -> None:
        self.__zig(node)
        self.__zig(node)

    def __splay(self, node: Node) -> Node:
        while node.parent is not None:
            parent: Node = node.parent
            grandparent: Node = parent.parent

            if grandparent is None:
                self.__zig(node)

            elif (grandparent.left == parent and parent.left == node) or \
                    (grandparent.parent == parent and parent.right == node):
                self.__zig_zig(node)
            else:
                self.__zig_zag(node)
        return node

    def __search(self, key: int) -> Node:
        current_node: Node = self.root
        previous_node: Node = None
        while current_node is not None and key != current_node.key:
            previous_node = current_node
            if key > current_node.key:
                current_node = current_node.right
            else:
                current_node = current_node.left

        if current_node is None and previous_node is not None:
            self.root = self.__splay(previous_node)
        return current_node

    def search(self, key: int) -> None:
        result: Node = self.__search(key)
        print('1 ' + str(result.value)) if result is not None else print('0')

    def set(self, key: int, value: str) -> None:
        node: Node = self.__search(key)
        if node is not Node:
            self.root = self.__splay(node)
            self.root.value = value

    def add(self, key: int, value: str) -> None:
        if self.root is None:
            self.root = Node(key, value)
        else:
            previos_node = None
            current_node: Node = self.root

            # Вставляем
            while current_node is not None:
                previos_node = current_node
                if key < current_node.key:
                    current_node = current_node.left
                elif key > current_node.key:
                    current_node = current_node.right
                else:  # Есть элемент уже с таким ключом в дереве
                    self.root = self.__splay(current_node)
                    print('error')
                    return

            if key < previos_node.key:
                previos_node.left = Node(key, value)
                previos_node.left.parent = previos_node
                self.root = self.__splay(previos_node.left)
            else:
                previos_node.right = Node(key, value)
                previos_node.right.parent = previos_node
                self.root = self.__splay(previos_node.right)

    def min(self) -> None:
        if self.root is None:
            print('error')
            return

        current_node: Node = self.root
        while current_node.left is not None:
            current_node = current_node.left
        self.root = self.__splay(current_node)
        print(str(current_node.key) + ' ' + str(current_node.value))

    def __max(self, node: Node) -> Node:
        if node is None:
            print('error')
            return

        current_node: Node = self.root
        while current_node.right is not None:
            current_node = current_node.right
        self.root = self.__splay(current_node)
        return current_node

    def max(self) -> None:
        result: Node = self.__max(self.root)
        print(str(result.key) + ' ' + str(result.value))

    def __merge(self, node1: Node, node2: Node) -> Node:
        if node1 is None:
            return node2
        if node2 is None:
            return node1

        current_node: Node = node1
        node1 = self.__splay(self.__max(current_node))
        node1.right = node2
        if node2 is not None:
            node2.parent = node1
        return node1

    def delete(self, key: int) -> None:
        node: Node = self.__search(key)
        if node is not None:
            self.root = self.__splay(node)

            if node.left is not None:
                node.left.parent = Node
            if node.right is not None:
                node.right.parent = Node

            self.root = self.__merge(node.left, node.parent)
            del node

    def print(self) -> None:
        def __print_(count: int) -> None:
            for i in range(count):
                print(' _ _')

        if self.root is None:
            print('_')
            return

        class Level():
            def __init__(self):
                self.count_underscore = 0
                self.array: list = []

        current_level = Level()
        new_level = Level()
        current_level.array.append(self.root)
        while len(new_level.array) > 0:
            for i in range(len(current_level.array)):
                node: Node = current_level.array[i]
                if i != 0:
                    print(' ', end='')

                if node is not None:
                    print('[ {0} {1}'.format(node.key, node.value), end='')
                    if current_level.array[i].parent is not None:
                        print('{0}'.format(current_level.array[i].parent), end='')
                    print(']', end='')

                    if node.left is not None:
                        new_level.array.append(node.left)
                    elif len(new_level.array) == 0 or new_level.array[-1] is not None:
                        new_level.array.append(None)
                    else:
                        new_level.count_underscore += 1

                    if node.right is not None:
                        new_level.array.append(node.right)
                    elif len(new_level.array) == 0 or new_level.array[-1] is not None:
                        new_level.array.append(None)
                    else:
                        new_level.count_underscore += 1

                else:
                    print('_', end='')
                    __print_(current_level.count_underscore - 1)
                    if len(new_level.array) == 0 or new_level.array[-1] is not None:
                        new_level.array.append(None)
                        new_level.count_underscore = current_level.count_underscore << 1
                    else:
                        new_level.count_underscore += current_level.count_underscore

            if len(new_level.array) > 1:
                print('')
            current_level, new_level = new_level, None


if __name__ == '__main__':

    tree = SplayTree()

    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == '':
            continue

        elif re.search('add .* .*', line):
            params: list = line.split(' ')
            tree.add(int(params[1]), params[2])

        elif re.search('set .* .*', line):
            params: list = line.split(' ')
            tree.set(int(params[1]), params[2])

        elif re.search('delete .*', line):
            params: list = line.split(' ')
            tree.delete(int(params[1]))

        elif re.search('search .*', line):
            params: list = line.split(' ')
            tree.search(int(params[1]))

        elif line == 'min':
            tree.min()

        elif line == 'max':
            tree.max()

        elif line == 'print':
            tree.print()

        else:
            print('error')
