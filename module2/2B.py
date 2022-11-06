import fileinput
import re


class Node:
    def __init__(self, key: int, value: str):
        self.parent: Node = None
        self.left: Node = None
        self.right: Node = None
        self.key: int = key
        self.value: str = value


class SplayTree:
    def __init__(self):
        self.root = None

    def __str__(self):
        result: str = ''

        def __print_(current_result: str, count: int) -> str:
            for _ in range(count):
                current_result += ' _'
            return current_result

        if self.root is None:
            result = '_\n'
            return result

        class Node_on_level:
            def __init__(self, node: Node = None):
                self.count_underscore = 0 if node is not None else 1
                self.node: Node = node

        current_level: list = []
        new_level: list = []
        flag_stop: bool = False
        current_level.append(Node_on_level(self.root))

        while not flag_stop:
            flag_stop = True
            count_of_node_per_next_level: int = 0

            for i in range(len(current_level)):
                if i != 0:
                    result += ' '

                if current_level[i].node is not None:
                    result += f'[{current_level[i].node.key} {current_level[i].node.value}'
                    if current_level[i].node.parent is not None:
                        result += f' {current_level[i].node.parent.key}'
                    result += ']'

                    if current_level[i].node.left is not None:
                        new_level.append(Node_on_level(current_level[i].node.left))
                        count_of_node_per_next_level += 1
                    elif len(new_level) == 0 or new_level[-1] is not None:
                        new_level.append(Node_on_level(None))
                    else:
                        new_level[i].count_underscore += 1

                    if current_level[i].node.right is not None:
                        new_level.append(Node_on_level(current_level[i].node.right))
                        count_of_node_per_next_level += 1
                    elif len(new_level) == 0 or new_level[-1] is not None:
                        new_level.append(Node_on_level(None))
                    else:
                        new_level[i].count_underscore += 1

                else:
                    result += '_'
                    result = __print_(result, current_level[i].count_underscore - 1)
                    if len(new_level) == 0 or new_level[-1].node is not None:
                        new_level.append(Node_on_level(None))
                        new_level[-1].count_underscore = current_level[i].count_underscore << 1
                    else:
                        new_level[-1].count_underscore += current_level[i].count_underscore << 1

            result += '\n'
            current_level, new_level = new_level, []
            if len(current_level) != 0 and count_of_node_per_next_level > 0:
                flag_stop = False

        return result

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
                    (grandparent.right == parent and parent.right == node):
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

    def search(self, key: int) -> Node:
        result: Node = self.__search(key)
        if result is not None:
            self.root = self.__splay(result)
        return result

    def set(self, key: int, value: str) -> None:
        node: Node = self.__search(key)
        if node is not None:
            self.root = self.__splay(node)
            self.root.value = value
        else:
            raise Exception('error')

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
                    raise Exception('error')

            if key < previos_node.key:
                previos_node.left = Node(key, value)
                previos_node.left.parent = previos_node
                self.root = self.__splay(previos_node.left)
            else:
                previos_node.right = Node(key, value)
                previos_node.right.parent = previos_node
                self.root = self.__splay(previos_node.right)

    def min(self) -> Node:
        if self.root is None:
            raise Exception('error')

        current_node: Node = self.root
        while current_node.left is not None:
            current_node = current_node.left
        self.root = self.__splay(current_node)
        if current_node is not None:
            return current_node

    def max(self) -> Node:
        if self.root is None:
            raise Exception('error')

        current_node: Node = self.root
        while current_node.right is not None:
            current_node = current_node.right
        self.root = self.__splay(current_node)
        return current_node

    def __merge(self, node1: Node, node2: Node) -> Node:
        if node1 is None:
            return node2
        if node2 is None:
            return node1

        max_node: Node = node1
        while max_node.right is not None:
            max_node = max_node.right

        node1 = self.__splay(max_node)
        node1.right = node2
        if node2 is not None:
            node2.parent = node1
        return node1

    def delete(self, key: int) -> None:
        node: Node = self.__search(key)
        if node is not None:
            self.root = self.__splay(node)

            if node.left is not None:
                node.left.parent = None
            if node.right is not None:
                node.right.parent = None

            self.root = self.__merge(node.left, node.right)
            del node
        else:
            raise Exception('error')


if __name__ == '__main__':

    tree = SplayTree()

    for line in fileinput.input():
        line = line.replace('\n', '')

        if re.search('add \S+ \S*', line):
            params: list = line.split(' ')
            try:
                tree.add(int(params[1]), params[2])
            except Exception as error:
                print(error)

        elif re.search('set \S+ \S*', line):
            params: list = line.split(' ')
            try:
                tree.set(int(params[1]), params[2])
            except Exception as error:
                print(error)

        elif re.search('delete \S+', line):
            params: list = line.split(' ')
            try:
                tree.delete(int(params[1]))
            except Exception as error:
                print(error)

        elif re.search('search \S+', line):
            params: list = line.split(' ')
            node: Node = tree.search(int(params[1]))

            if node is not None:
                print(f'1 {node.value}')
            else:
                print(0)

        elif line == 'min':
            try:
                node:Node =tree.min()
                print(node.key, node.value)
            except Exception as error:
                print(error)

        elif line == 'max':
            try:
                node:Node =tree.max()
                print(node.key, node.value)
            except Exception as error:
                print(error)


        elif line == 'print':
            print(tree, end='')

        elif line == '':
            continue

        else:
            print('error')
