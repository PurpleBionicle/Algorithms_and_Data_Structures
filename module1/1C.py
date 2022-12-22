import fileinput


def searching(graph: dict, searching_element: str, way: list[str], start_libraries: list[str], visited: dict) -> None:
    if graph.get(searching_element):
        for step in graph.get(searching_element):
            if step not in visited:
                way.append(step)
                visited[step] = 1
                searching(graph, step, way, start_libraries, visited)

    if len(way) > 1 and way[len(way) - 1] in start_libraries:
        for g in reversed(way):
            if g != way[0]:
                print(g, end=' ')
            else:
                print(g)
    if len(way) != 0:
        visited.pop(way.pop(), None)


if __name__ == '__main__':
    graph: dict = {}
    vuln_libs: list = []
    dependence: list = []
    while len(vuln_libs) == 0:
        vuln_libs = list(set(input().strip().split(' ')))
    while len(dependence) == 0:
        dependence = list(set(input().strip().split(' ')))

    for line in fileinput.input():
        libraries: list = line.strip().split(' ')
        if len(libraries) != 0:
            main_lib: str = libraries.pop(0)
            for lib in libraries:
                if lib in graph:
                    again: bool = False
                    for vertex in graph[lib]:
                        if vertex == main_lib:
                            again = True
                    if not again:
                        graph[lib].append(main_lib)
                else:
                    # добавим ребра в наш граф
                    graph[lib] = [main_lib]

    common = [value for value in vuln_libs if value in dependence]
    while len(common) != 0:
        print(common.pop())
    for vuln_lib in vuln_libs:
        way = [vuln_lib]
        visited = {vuln_lib: 1}
        searching(graph, vuln_lib, way, dependence, visited)
