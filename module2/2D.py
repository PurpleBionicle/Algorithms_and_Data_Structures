import re
import fileinput


class Node:
    def __init__(self, chars=None, brother=None, child=None):
        self.chars: str = chars
        self.brother: Node = brother
        self.child: Node = child

    def check_for_empty(self):
        return len(self.chars) == 0 or self is None


class Bor:
    def __init__(self):
        self.root = Node()

    def __max_prefix(self, node: Node, word: str) -> int:
        for i in range(len(word)):
            if i == len(node.chars) or word[i] != node.chars[i]:
                return i
        return len(word)

    def __split(self, node: Node, index: int) -> None:
        new_node = Node(chars=node.chars[index:])
        new_node.brother = node.brother
        node.brother = new_node
        node.chars = node.chars[index:]

    def search(self, tree: Node, word: str):
        if tree.check_for_empty():
            return 0
        same_part: int = self.__max_prefix(tree, word)
        if same_part == 0:
            # если нет префикса, то идем к другому брату - в другую ветвь
            return self.search(tree.brother, word)
        if same_part == len(word):
            # дошли
            return tree
        if same_part == len(tree.chars):
            # если слово больше ноды, то спускаемся глубже
            return self.search(tree.child, word)
        return 0

    def add(self, tree: Node, word: str):
        if tree.check_for_empty():
            return Node(chars=word)

        same_part: int = self.__max_prefix(tree, word)
        if same_part == 0:
            tree.brother = self.add(tree.brother, word)
        elif same_part < len(word):
            if same_part < len(tree.chars):
                self.__split(tree, same_part)
            tree.child = self.add(tree.child, word[same_part:])
        return tree

    # node
    #             int prefix(char* x, int n, char* key, int m) // длина наибольшего общего префикса строк x и key
    # 	for( int k=0; k<n; k++ )
    # 		if( k==m || x[k]!=key[k] )
    # 			return k;
    # 	return n;


# -1 = ошибка , 0 = 1 ошибка , 1 = совпадение
def main():
    bor = Bor()
    count = None
    words: int = 0
    while count is None:
        input_: str = input()
        if input_.isdigit():
            count = int(input_)
        elif input_ == '':
            continue
        else:
            print('error')

    node = None
    answer_node = None
    for line in fileinput.input():
        line = line.replace('\n', '')
        if line == '':
            continue

        if words < count:
            node = bor.add(node, line)
        else:
            answer_node = bor.search(answer_node, line)

        words += 1


if __name__ == '__main__':
    main()

# def __split(self, word: str, same: int) -> Node:
# different = self.root.chars[same:]
# self.root.chars = self.root.chars[:same]
# if self.root.child is not None:
#     # Если есть ребенок, то создадим нового и перезапишем связи
#     last_children: Node = self.root.child
#     self.root.child = Node(chars=word[same:], child=last_children)
# else:
#     self.root.child = Node(chars=different)
#
# last_brother = self.root.brother
# self.root.brother = Node(chars=word[same:],brother=last_brother)
# return self.root.brother
# new_node = Node()

# def add(self, word: str):
#     if self.root.chars is None:
#         self.root.chars = word
#     else:
#         len_same_part: int = 0
#         offset: int = 0
#         current_node: Node = self.root
#         while len(word) != 0:
#             if current_node is not None:
#                 if word[offset] != current_node.chars[offset] or offset > len(current_node.chars):
#                     offset = 0
#                     if len_same_part == 0:
#                         if current_node.brother is None:
#                             current_node.brother = word
#                             break
#                         else:
#                             # если есть брат идем к нему и сравниваем дальше
#                             current_node = current_node.brother
#                     else:
#                         # если есть общая часть длины всей ноды, то отрезаем ее и ищем по срезу в детях
#                         if len_same_part == len(current_node.chars):
#                             word = word[len_same_part:]
#                             len_same_part = 0
#                             current_node = current_node.child
#                         else:
#                             # должны по общей части разбить ноду
#                             current_node = current_node.__split(word, len_same_part)
#                             word = word[len_same_part:]
#
#                 else:
#                     offset += 1
#                     len_same_part = offset
#                     continue
#             else:
#                 current_node.chars = word
#                 word.clear()
#
# def search(self, word: str):
#     if self.root.chars is None:
#         return 1 if len(word)<=1 else 0
#     else:
#         len_same_part: int = 0
#         offset: int = 0
#         current_node: Node = self.root
#         while len(word) != 0:
#             if current_node is not None:
#                 if word[offset] != current_node.chars[offset] or offset > len(current_node.chars):
#                     offset = 0
#                     if len_same_part == 0:
#                         if current_node.brother is None:
#                             current_node.brother = word
#                             break
#                         else:
#                             # если есть брат идем к нему и сравниваем дальше
#                             current_node = current_node.brother
#                     else:
#                         # если есть общая часть длины всей ноды, то отрезаем ее и ищем по срезу в детях
#                         if len_same_part == len(current_node.chars):
#                             word = word[len_same_part:]
#                             len_same_part = 0
#                             current_node = current_node.child
#                         else:
#                             # должны по общей части разбить ноду
#                             current_node = current_node.__split(word, len_same_part)
#                             word = word[len_same_part:]
#
#                 else:
#                     offset += 1
#                     len_same_part = offset
#                     continue
#             else:
#                 current_node.chars = word
#                 word.clear()
