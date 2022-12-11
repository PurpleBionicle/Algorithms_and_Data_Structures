import fileinput


class Error_login:
    def __init__(self, count: int, interval: int, start_lock_time: int, max_lock_time: int, current_time: int):
        self.max_trying: int = count
        self.count_of_trying: int = 0
        self.interval: int = interval
        self.current_time: int = current_time
        self.lock_time: int = start_lock_time if start_lock_time else None
        self.min_lock_time: int = start_lock_time
        self.max_lock_time: int = max_lock_time
        self.trys_per_interval: list = []

    def __clear(self) -> None:
        self.trys_per_interval.clear()
        self.count_of_trying = 0

    def check_of_trying(self, trying: list[int]) -> int:
        trying.sort()
        current_lock_time: int = 0

        if len(trying) == 0:
            return -1

        for try_ in trying:
            # if try_ < current_lock_time:  # игнор попыток во время бана
            #     continue

            if self.current_time - try_ > 2 * self.max_lock_time:  # 2Bmax condition
                continue

            if self.count_of_trying == 0:
                self.trys_per_interval.append(try_)
                self.count_of_trying += 1
                if self.max_trying == 1:
                    """Вырожденный случай так как
                     для расчета интервала нужно обращение к массиву , а в этом случае - list out of range"""
                    current_lock_time = self.trys_per_interval[0] + self.lock_time
                    self.lock_time *= 2
                    if self.lock_time > self.max_lock_time:
                        self.lock_time = self.max_lock_time
                    self.__clear()
                continue

            if try_ - self.trys_per_interval[0] > self.interval:
                self.trys_per_interval.pop(0)
                self.trys_per_interval.append(try_)
                continue

            else:
                self.trys_per_interval.append(try_)
                self.count_of_trying += 1

            if self.count_of_trying == self.max_trying:
                current_lock_time = self.trys_per_interval[-1] + self.lock_time
                self.lock_time *= 2
                if self.lock_time > self.max_lock_time:
                    self.lock_time = self.max_lock_time
                self.__clear()

        return current_lock_time if current_lock_time > self.current_time else -1


def main():
    info: list = input().split()
    error = Error_login(int(info[0]), int(info[1]), int(info[2]), int(info[3]), int(info[4]))
    trying: list[int] = []
    for line in fileinput.input():
        line = line.replace('\n', '')
        trying.append(int(line))
    result = error.check_of_trying(trying)
    print(result if result != -1 else 'ok')


if __name__ == '__main__':
    main()
    """
    Ассимптотическая сложность = О(nlogn):
        1. считать n записей и занести в массив - O(n)
        2. отсортировать - O(nlogn)
        3. пройтись по всем для проверки - О(n), так как цикл содержит только if-ы
    Память = O(n):
        память используется только для хранения массива и хранения попыток в интервала одного блока (O(n)) 
        и для хранения нескольких переменных класса - (O(1))
    """
