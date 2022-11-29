import fileinput


class Error_login:
    def __init__(self, count: int, interval: int, start_lock_time: int, max_lock_time: int, current_time: int):
        self.max_trying: int = count
        self.count_of_trying: int = 0
        self.interval: int = interval
        self.current_time: int = current_time
        self.lock_time: int = start_lock_time
        self.min_lock_time: int = start_lock_time
        self.max_lock_time: int = max_lock_time
        self.first_try_time: int = 0

    def check_of_trying(self, trying: list[int]):
        trying.append(self.current_time)
        trying.sort()
        current_lock_time: int = 0
        init_time: int = trying[0]
        for try_ in trying:
            if try_ == self.current_time:
                return current_lock_time if current_lock_time > try_ else -1
            else:
                if try_ < current_lock_time:
                    continue

                if try_ - init_time > 2 * self.max_lock_time:
                    init_time = try_
                    self.lock_time = self.min_lock_time
                    self.count_of_trying = 0
                self.count_of_trying = self.count_of_trying + 1 if try_ - self.first_try_time < self.interval else 1

                if self.count_of_trying == 1:
                    self.first_try_time = try_

                if self.count_of_trying == self.max_trying:
                    self.count_of_trying = 0
                    current_lock_time = try_ + self.lock_time
                    self.lock_time *= 2


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
        память используется только для хранения массива (O(n)) 
        и для хранения нескольких переменных класса - (O(1))
    """
