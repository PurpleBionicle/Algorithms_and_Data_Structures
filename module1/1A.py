import sys


def find_values(str):
    array = []
    current_value = ''
    for i in range(len(str)):
        if str[i].isdigit():
            current_value += str[i]

        elif str[i] == '-':
            if len(current_value) != 0:
                array.append(int(current_value))
                current_value = ''
            if i != len(str) - 1 and str[i + 1].isdigit():
                current_value = str[i]
        else:
            if len(current_value) != 0:
                array.append(int(current_value))
                current_value = ''

    if len(current_value) != 0:
        array.append(int(current_value))

    return array if 0 != len(array) else [0]


if __name__ == '__main__':
    answer = 0
    lines = sys.stdin.readlines()

    for line in range(len(lines)):
        current_array = find_values(lines[line])
        answer += sum(current_array)

    print(answer)