import fileinput
import math
from array import array
import re


class Bitarray():
    def __init__(self, size: int = 0):
        self.array = array('B', [0] * ((size + 7) // 8))
        self.size: int = size

    def add(self, index: int) -> None:
        # узнаем индекс в байте и переводим в dec и делаем ИЛИ
        self.array[index // 8] |= int(math.pow(2, 8 - 1 - (index % 8)))

    def check_bit(self, index: int) -> bool:  # TODO check
        # вернем индекс в булевом представлении
        return bool(self.array[index // 8] & int(math.pow(2, 8 - 1 - (index % 8))))

    def __str__(self):
        str_array: str = ''
        for byte in self.array:
            str_array += f'{byte:08b}'
        str_array = str_array[:self.size]
        return str_array


class Bloom_filter():
    def __generate_primes(self, count: int):
        primes: list[int] = [2]
        number: int = 3
        while len(primes) != count:
            prime_flag: bool = True
            for prime in primes:
                if number % prime == 0:
                    prime_flag = False
                    break
            if prime_flag:
                primes.append(number)
            number += 1

        return primes

    def __init__(self, n: int, P: float):
        if n <= 0 or P <= 0.0 or P > 1.0:
            raise Exception('error')

        self.count: int = n
        self.M_31: int = 2147483647
        self.size: int = round((-1 * n * math.log2(P)) / math.log(2))
        self.hashes_count: int = round(-1 * math.log2(P))
        if self.size <= 0 or self.hashes_count <= 0:
            raise Exception('error')
        # else:
        # print(f'{self.size} {self.hashes_count}')
        self.array: Bitarray = Bitarray(self.size)
        self.primes: list[int] = self.__generate_primes(self.hashes_count)

    def __str__(self):
        return str(self.array)

    def hash(self, i: int, key: int) -> int:
        return (((i + 1) * key + self.primes[i]) % self.M_31) % self.size

    def add(self, key: int):
        for index in range(self.hashes_count):
            current_hash: int = self.hash(index, key)
            self.array.add(current_hash)

    def search(self, key: int) -> bool:
        for i in range(self.hashes_count):
            index: int = self.hash(i, key)
            bit: bool = self.array.check_bit(index)
            if not bit:
                return False
        return True


def main():
    bloom = None
    for line in fileinput.input():
        line = line.replace('\n', '')

        if len(line) == 0:
            continue

        # add K, search K или print,
        if re.search('set \d+ \d+', line):
            if bloom is None:
                params: list[str] = line.split(' ')
                try:
                    bloom = Bloom_filter(int(params[1]), float(params[2]))
                    print(f'{bloom.size} {bloom.hashes_count}')
                except Exception as error:
                    print(error)
            else:
                print('error')

        elif re.search('add \d+', line):
            if bloom is not None:
                bloom.add(int(line.split(' ')[1]))
            else:
                print('error')

        elif re.search('search \d+', line):
            if bloom is not None:
                result: int = bloom.search(int(line.split(' ')[1]))
                print('1' if result else '0')
            else:
                print('error')

        elif line == 'print':
            if bloom is not None:
                print(bloom)
            else:
                print('error')
        else:
            print('error')


if __name__ == '__main__':
    main()
