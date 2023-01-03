import fileinput


class Graph():

    def add_vertex(self, libs: list[str]) -> None:
        # построим граф
        # начинаем с 2
        for lib in libs[1:]:
            if lib in self.graph:
                again: bool = False
                for node in self.graph[lib]:
                    if node == libs[0]:
                        again = True
                # если нет либы в ее зависимости то строим
                if not again:
                    self.graph[lib].append(libs[0])
            else:
                self.graph[lib] = [libs[0]]

    def __add_dependence(self) -> None:
        for node in self.dependence:
            if node in self.graph:
                if node not in self.graph[node]:
                    self.graph[node].append(node)
            else:
                self.graph[node] = [node]

    def __init__(self, vuln_libs: list[str], dependence: list[str]):
        self.graph: dict = {}
        self.vuln_libs = vuln_libs
        self.dependence = dependence

        self.__add_dependence()

    def search_vulnerability(self) -> None:
        common = [lib for lib in vuln_libs if lib in dependence]
        while len(common) != 0:
            print(common.pop())

        for vuln_lib in self.vuln_libs:
            path: list[str] = [vuln_lib]
            visited: dict = {vuln_lib: True}
            # поиск вглубину
            self.__dfs(vuln_lib, path, visited)

    def __dfs(self, vuln_lib: str, path: list, used: dict) -> None:
        if self.graph.get(vuln_lib):
            for step in self.graph.get(vuln_lib):
                if step not in used:
                    path.append(step)
                    used[step] = True
                    self.__dfs(step, path, used)

        if len(path) > 1 and path[len(path) - 1] in self.dependence:
            for node in reversed(path):
                if node != path[0]:
                    print(node, end=' ')
                else:
                    print(node)
        if len(path) != 0:
            used.pop(path.pop(), None)


if __name__ == "__main__":
    vuln_libs: list[str] = []
    dependence: list[str] = []
    while len(vuln_libs) == 0:
        vuln_libs = list(set(input().strip().split(' ')))
    while len(dependence) == 0:
        dependence = list(set(input().strip().split(' ')))

    graph: Graph = Graph(vuln_libs, dependence)
    for line in fileinput.input():
        libs: list[str] = line.strip().split(' ')
        graph.add_vertex(libs)

    graph.search_vulnerability()
