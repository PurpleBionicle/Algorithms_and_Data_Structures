import fileinput


class Deque():
    def __init__(self):
        self.size: int = 0
        self.capacity: int = 0
        self.first: int = 0  # тем самым мы сможет добиться того, что у нас будет цикличная структура
        # то есть нам не придется передвигать элементы и также начало будет с этого индекса, а не с нуля

    def set_size(self, input_size: str) -> None:
        if input_size.isdigit():
            self.capacity = int(input_size)
            # выделение памяти один раз, но
            # придется постоянно проверять элементы на ==None (
            self.array = [None] * int(input_size)

        else:
            print('error')

    def pushf(self, value: str) -> None:
        if self.size == self.capacity:
            print('overflow')
        else:
            self.size += 1
            self.first -= 1
            self.array[(self.first) % self.capacity] = value

    def pushb(self, value: str) -> None:
        if self.size == self.capacity:
            print('overflow')
        else:
            self.array[(self.first + self.size) % self.capacity] = value
            self.size += 1

    def popf(self) -> str:
        #     можно конечно через [x if x] - но так доп память
        if self.size == 0:
            return ('underflow')

        else:
            result: str
            result, self.array[self.first % self.capacity] = self.array[self.first % self.capacity], None
            self.first += 1
            self.size -= 1
            return result

    def popb(self) -> str:
        if self.size == 0:
            return ('underflow')
        else:
            result: str
            result, self.array[(self.first + self.size - 1) % self.capacity] = \
                self.array[(self.first + self.size - 1) % self.capacity], None

            self.size -= 1
            return result

    def print(self) -> None:
        #     можно конечно через [x if x] - но так доп память
        if self.size == 0:
            print('empty')
            return
        for i in range(self.size):
            if i != self.size - 1:
                print(self.array[(self.first + i) % self.capacity], end=' ')
            else:
                print(self.array[(self.first + i) % self.capacity])


if __name__ == '__main__':

    deque = Deque()
    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == '':
            continue

        elif deque.capacity == 0:
            # наверно лучше потратиться на память тут, чем два раза сплитовать
            params: list = line.split(' ')
            if params[0] == 'set_size' and len(params) == 2:
                deque.set_size(params[1])
            else:
                print('error')

        # без сайза
        elif deque.capacity != 0:
            params = line.split(' ')
            if len(params) > 2:
                print('error')
            elif len(params) == 2:
                if params[0] == 'pushf':
                    deque.pushf(params[1])
                elif params[0] == 'pushb':
                    deque.pushb(params[1])
                else:
                    print('error')
            elif line == 'popf':
                print(deque.popf())
            elif line == 'popb':
                print(deque.popb())

            elif line == 'print':
                deque.print()
            else:
                print('error')
        else:
            print('error')