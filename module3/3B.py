import fileinput
import math
from array import array
import re


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
        else:
            print(f'{self.size} {self.hashes_count}')

        self.array = array('B', [0] * ((self.size + 7) // 8))
        self.primes: list[int] = self.__generate_primes(self.hashes_count)

    def __str__(self):
        if self.array is None:
            raise Exception('error')

        result: str = ''
        for bit in self.array:
            bin: str = f'{bit:08b}'
            result += bin
        return result if len(result) % self.size != 0 else result[:-(len(result) % self.size)]

    def add(self, k: int):
        for i in range(self.hashes_count):
            #         по всем хэшам идем
            hash: int = (((i + 1) * k + self.primes[i]) % self.M_31) % self.size
            # узнаем индекс в байте и переводим в dec и делаем или
            self.array[hash // 8] = self.array[hash // 8] | int(math.pow(2, 8 - 1 - (hash % 8)))

    def search(self, k: int) -> int:
        for i in range(self.hashes_count):
            hash = ((((i + 1) * k + self.primes[i]) % self.M_31) % self.size)
            bin_array: str = f'{self.array[hash // 8]:08b}'
            if bin_array[hash % 8] == '0':
                return 0
        return 1


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
                print(result)
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
