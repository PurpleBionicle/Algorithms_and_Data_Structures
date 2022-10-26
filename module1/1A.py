import fileinput


class Sum():
    def find_values(self) -> int:
        result: int = 0
        for line in fileinput.input():
            current_value: str = ''

            for i in range(len(line) - 1):
                if line[i].isdigit():
                    current_value += line[i]
                    if not line[i + 1].isdigit():
                        result += int(current_value)
                        current_value = ''

                # можно через or добавить к предыдущему условию,но тогда получается 2 проверки line[i + 1].isdigit
                elif line[i] == '-' and line[i + 1].isdigit():
                    current_value += line[i]

        return result


if __name__ == '__main__':
    sum = Sum()
    print(sum.find_values())