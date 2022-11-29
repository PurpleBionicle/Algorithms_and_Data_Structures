import fileinput


class Node:
    def __init__(self, chars='', brother=None, child=None, end_of_word=False):
        self.chars: str = chars
        self.brother: Node = brother
        self.child: Node = child
        self.end_of_word = end_of_word

    def check_for_empty(self):
        return len(self.chars) == 0


class Bor:
    def __init__(self):
        self.root = None

    def __max_prefix(self, node: Node, word: str) -> int:
        for i in range(len(word)):
            if i == len(node.chars) or word[i] != node.chars[i]:
                return i
        return len(word)

    def __split(self, node: Node, index: int) -> None:
        new_node = Node(chars=node.chars[index:], end_of_word=True)
        new_node.child = node.child
        node.child = new_node
        node.chars = node.chars[:index]

    def search(self, tree=Node(), word: str = '') -> None | Node:
        def __check_error(tree:Node=Node(),word:str=''):
            def compare_word(word1:str,word2:str):
                count_error:int = 0
                i,j= 0,0
                while i<len(word1) or j<len(word2):
                    if word1[i]==word2[j]:
                        i+=1
                        j+=1
                    else:
                        count_error+=1
                        if word1[i+1]==word[j]:
                            i+=2
                            j+=1
                        elif word[i]==word[j+1]:
                            j+=2
                            i+=1
                        else:
                            return -1
                        #Не пропущен 

            # лишний символ
            same_part = self.__max_prefix(tree,word)
            if same_part

            # отсутствует символ
            if i + 1 < len(node.key) and node.key[i + 1] == word[word_index]:
                err = ErrorType.LOOSE
                self._recursive_check(accumulate, node, word, err, key_index + i + 1, word_index)
            elif i + 1 == len(node.key) and word[word_index] in node.kids:
                err = ErrorType.LOOSE
                self._recursive_check(accumulate + node.key, node.kids[word[word_index]], word, err, 0, word_index)

            # символы поменяны местами
            if word_index + 1 < len(word) and i == len(node.key) - 1 and (
                    word[word_index + 1] == node.key[i] and word[word_index] in node.kids):
                err = ErrorType.SWAP_BOARD
                self._recursive_check(accumulate + node.key, node.kids[word[word_index]], word, err, 1, word_index + 2)
            elif word_index + 1 < len(word) and i + 1 < len(node.key) and node.key[i] == word[word_index + 1] and \
                    node.key[i + 1] == \
                    word[word_index]:
                err = ErrorType.SWAP_BOARD
                self._recursive_check(accumulate, node, word, err, key_index + i + 2,
                                      word_index + 2)

            # Если не сработало ни одна из предыдущих условий, значит символ был заменён
            err = ErrorType.REPLACE
            self._recursive_check(accumulate, node, word, err, key_index + i + 1, word_index + 1)
            return

        if tree is None:
            return None

        if tree.check_for_empty():
            if self.root is None:
                return None
            tree = self.root

        same_part: int = self.__max_prefix(tree, word)
        if same_part == 0:
            # если нет префикса, то идем к другому брату - в другую ветвь
            return self.search(tree.brother, word)
        if same_part == word and same_part == tree.chars and tree.end_of_word:
            # дошли
            return tree
        if same_part == len(tree.chars):
            # если слово больше ноды, то спускаемся глубже
            return self.search(tree.child, word[same_part:])
        return None

    def add(self, tree=None, word: str = ''):
        if self.root is None:
            tree = Node(chars=word, end_of_word=True)
            self.root = tree
            return tree

        if tree is None:
            tree = Node(chars=word, end_of_word=True)
            return tree
        # if tree.check_for_empty():
        #     tree = Node(chars=word)
        #     if self.root is None:
        #         self.root = tree
        #     return tree

        same_part: int = self.__max_prefix(tree, word)
        if same_part == 0:
            tree.brother = self.add(tree.brother, word)
        elif same_part < len(word):
            if same_part < len(tree.chars):
                self.__split(tree, same_part)
            tree.child = self.add(tree.child, word[same_part:])
        return tree


def get_error_type(word: str, answer: str):
    pass


def main():
    # вставка лишнего символа, удаление символа, замена символа или транспозиция соседних символов.
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
            words += 1
        else:
            # raise error/1 type_error node / 1 node
            answer_node = bor.search(Node(), line)
            if answer_node is None:
                print(f'{line} -?')
            else:
                print(f'{line} - ok')


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
