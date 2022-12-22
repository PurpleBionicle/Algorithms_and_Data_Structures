import fileinput


class Node:
    """
     сложность обращения к следующей вершине O(1) - class Node
    """

    def __init__(self, word: str, end_of_word: bool):
        self.word = word
        self.kids = {}
        self.end_of_word = end_of_word


class Bor:

    def __init__(self):
        self.root: Node = Node('', False)

    def __max_prefix(self, word1: str, word2: str) -> int:
        min_len: int = min(len(word1), len(word2))
        for i in range(min_len):
            if word1[i] != word2[i]:
                return i
        return min_len

    def __split(self, current_node: Node, word: str, index: int) -> None:
        split: int = self.__max_prefix(word[index:], current_node.word)
        equal_part = current_node.word[:split]
        new_node = Node(current_node.word[split:], current_node.end_of_word)
        new_node.kids = current_node.kids
        current_node.kids = {current_node.word[split]: new_node}
        word_split = word[index + split:]
        if word_split:
            current_node.kids[word_split[0]] = Node(word_split, True)
            current_node.end_of_word = False
        current_node.word = equal_part

    def correction(self, word) -> list[str]:
        compare = None
        word = word.lower()
        if not self.find(word):
            compare = []
            for k, v in self.root.kids.items():
                self.__tree_bypass(word, False, '', 0, v, compare)
        return compare

    """ сложность добавления O(n): находим место в дереве за одно последовательное считывание слова"""

    def add(self, word) -> None:
        if not word:
            return
        word = word.lower()
        index = 0
        current_node: Node = self.root
        compare: bool = False
        while index < len(word) and word[index] in current_node.kids:
            compare = False
            current_node: Node = current_node.kids[word[index]]
            if current_node.word == word[index: index + len(current_node.word)]:
                compare = True
                index += len(current_node.word)
                continue
            break
        if index == len(word):
            current_node.end_of_word = True
            return
        if word[index] not in current_node.kids and (compare or current_node == self.root):
            current_node.kids[word[index]] = Node(word[index:], True)
            return

        self.__split(current_node, word, index)

    """ сложность поиска O(n): за одно последовательное считывание слова постепенно двигаемся по дереву 
    и находим наше слово"""

    def find(self, word) -> bool:
        word = word.lower()
        if not self.root.kids:
            return False
        index: int = 0
        current_node: Node = self.root

        while index < len(word) and word[index] in current_node.kids:
            current_node: Node = current_node.kids[word[index]]
            len_temp = len(current_node.word)
            if current_node.word == word[index: index + len_temp]:
                index += len_temp
                continue
            break

        return index == len(word) and current_node.end_of_word

    def __check_error(self, node: Node, word: str, index: int, offset: int, code: str, error: bool, answer: list,
                      check_word: str) -> None:
        replace_error: bool = node.word[offset + 1:] == check_word[offset + 1:]  # был изменен 1 символ
        buf: str = node.word[offset + 1:]  # чтобы срез не брать два раза
        delete_error: bool = buf == check_word[offset: offset + len(buf)]  # был удален 1 символ
        buf = node.word[offset:]
        insert_error: bool = buf == word[
                                    index + offset + 1: index + offset + 1 + len(
                                        buf)]  # был вставлен 1 символ
        transpose_error: bool = False
        # транспозиция 2-ух символов
        if len(word) > index + offset + 1 and offset == len(node.word) - 1 and word[index + offset + 1] == node.word[
            offset]:
            if check_word[offset] in node.kids:
                self.__tree_bypass(
                    word[index + offset + 1] + check_word[offset] + word[index + offset + 2:], error, code + node.word,
                    1, node.kids[check_word[offset]], answer)
        elif offset < len(check_word) - 1 and check_word[offset + 1] + check_word[offset] + check_word[
                                                                                            offset + 2:] == node.word[
                                                                                                            offset:]:
            transpose_error = True

        if delete_error:
            if index + len(node.word) - 1 == len(word) and node.end_of_word:
                answer.append(code + node.word)
            for k, vert in node.kids.items():
                self.__tree_bypass(word, error, code + node.word, index + len(node.word) - 1, vert, answer)

        if insert_error:
            if index + len(node.word) + 1 == len(word) and node.end_of_word:
                answer.append(code + node.word)
            for k, vert in node.kids.items():
                self.__tree_bypass(word, error, code + node.word, index + len(node.word) + 1, vert, answer)

        if transpose_error or replace_error:
            if index + len(node.word) == len(word) and node.end_of_word:
                answer.append(code + node.word)
            for k, vert in node.kids.items():
                self.__tree_bypass(word, error, code + node.word, index + len(node.word), vert, answer)

    """
    сложность поиска подходящих исправлений по сжатому префиксному дереву O(n^2 * k), n - длина слова, k - мощность
    """

    def __tree_bypass(self, word: str, error: bool, code: str, index: int, node: Node, answer: list):
        check_word: str = word[index: index + len(node.word)]
        if node.word == check_word:
            if node.end_of_word and (
                    len(word) == index + len(node.word) or (len(word) - 1 == index + len(node.word) and not error)):
                answer.append(code + node.word)

            # переход к детям
            for symbol, vertex in node.kids.items():
                self.__tree_bypass(word, error, code + node.word, index + len(node.word), vertex, answer)
            return
        if error:
            return

        error = True

        offset: int = self.__max_prefix(node.word, check_word)

        self.__check_error(node=node, word=word, index=index, offset=offset, code=code, error=error, answer=answer,
                           check_word=check_word)


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

    for line in fileinput.input():
        line = line.replace('\n', '')
        if line == '':
            continue

        if words < count:
            bor.add(line)
            words += 1
        else:

            answer: list = bor.correction(line)
            if answer is None:
                print(f'{line} - ok')
                continue
            if not answer:
                print(f'{line} -?')
                continue
            if len(answer) == 1:
                print(f'{line} -> {answer[0]}')
                continue

            answer = sorted(answer)
            print(f'{line} -> ', end='')
            print(', '.join(answer))


if __name__ == '__main__':
    main()
