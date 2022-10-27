import fileinput
import re
class Node:
    def __init__(self):
        self.value:str
        self.key:int
        self.parent:Node
        self.left:Node
        self.right:Node

class SplayTree():
    def __init__(self):
        pass

    def set(self, key:int, value:str)->None:
        print(2)

    def add(self, key:int, value:str)->None:
        print(1)


    def delete(self, key:int)->None:
        print(3)


    def search(self, key:int)->None:
        print(4)


    def min(self)->None:
        print(5)


    def max(self)->None:
        print(6)

    def print(self)->None:
        print(7)

if __name__ == '__main__':

    tree = SplayTree()

    for line in fileinput.input():
        line = line.replace('\n', '')

        if line == '':
            continue

        elif re.search('add .* .*',line):
            params:list = line.split(' ')
            tree.add(params[1],params[2])

        elif re.search('set .* .*',line):
            params:list = line.split(' ')
            tree.set(params[1],params[2])

        elif re.search('delete .*',line):
            params:list = line.split(' ')
            tree.delete(params[1])

        elif re.search('search .*',line):
            params:list = line.split(' ')
            tree.search(params[1])

        elif line=='min':
            tree.min()

        elif line=='max':
            tree.max()

        elif line=='print':
            tree.print()

        else:
            print('error')
