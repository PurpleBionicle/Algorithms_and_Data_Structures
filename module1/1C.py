import fileinput


class Graph():

    def __make_graph(self, line: str) -> None:
        libs = line.split(' ')
        # начинаем с 2
        for lib in libs[1:]:
            if lib in self.graph:
                # если нет либы в ее зависимости то строим
                if libs[0] not in self.graph[lib]:
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

    def __init__(self):
        self.graph: dict = {}
        self.vuln_libs: set = set(input().split(' '))  # напишите пожалуйста в комменте -
        # так нормально,что инициализиция + приведение
        self.dependence: set = set(input().split(' '))
        for line in fileinput.input():
            line = line.replace('\n', '')
            self.__make_graph(line)

        self.__add_dependence()

    def search_vulnerability(self) -> None:
        for vuln_lib in self.vuln_libs:
            path: list = []
            visited: dict = {}
            self.__dfs(vuln_lib, path, visited)

    def __dfs(self, vuln_lib: str, path: list, used: dict) -> None:
        if vuln_lib in self.graph:
            for parent in self.graph[vuln_lib]:
                used[vuln_lib] = True
                if vuln_lib == parent and vuln_lib in self.dependence:
                    path.append(vuln_lib)
                    buf = path
                    buf.reverse()
                    used.clear()
                    print(" ".join(buf))
                    return
                else:
                    if parent not in used:
                        used_copy = used.copy()
                        buf = path
                        self.__dfs(parent, buf + [vuln_lib], used_copy)


if __name__ == "__main__":
    graph = Graph()
    graph.search_vulnerability()