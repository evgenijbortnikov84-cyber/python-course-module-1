from collections import deque


def _contains_vertex(graph, vertex):
    # Ключ проверяется сразу. Просмотр соседей нужен только для вершины без ключа.
    return vertex in graph or any(vertex in neighbors for neighbors in graph.values())


def _check_start(graph, start):
    if not _contains_vertex(graph, start):
        raise ValueError("Начальная вершина отсутствует в графе")


def breadth_first_search(graph, start):
    """Вернуть только порядок обхода, без расстояний и предшественников.

    Граф: словарь со списками соседей; вершины хешируемые.
    Вершины могут встречаться только среди соседей. Неизвестный start: ValueError.
    """
    _check_start(graph, start)
    queue = deque([start])
    visited = {start}
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.get(vertex, ()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def breadth_first_search_details(graph, start):
    """Вернуть (порядок, расстояния, предшественники) невзвешенного графа.

    Неизвестный start: ValueError. Время O(V + E), память O(V).
    Если start является ключом, недостижимая часть графа не просматривается.
    """
    _check_start(graph, start)
    queue = deque([start])
    distances = {start: 0}
    predecessors = {}
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.get(vertex, ()):
            if neighbor not in distances:
                distances[neighbor] = distances[vertex] + 1
                predecessors[neighbor] = vertex
                queue.append(neighbor)
    return order, distances, predecessors


def shortest_path(graph, start, target):
    """Кратчайший путь; None, если существующая цель недостижима.

    Отсутствие start или target вызывает ValueError. При нескольких кратчайших
    путях выбирается первый найденный по порядку соседей в списках.
    Поиск останавливается при обнаружении target, не после полного обхода.
    """
    _check_start(graph, start)
    if start == target:
        return [start]
    queue = deque([start])
    # Словарь одновременно отмечает обнаруженные вершины и хранит родителей.
    predecessors = {start: start}
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.get(vertex, ()):
            if neighbor in predecessors:
                continue
            predecessors[neighbor] = vertex
            if neighbor == target:
                path = [target]
                while path[-1] != start:
                    path.append(predecessors[path[-1]])
                path.reverse()
                return path
            queue.append(neighbor)
    # Проверку откладываем: найденная цель уже заведомо существует.
    if not _contains_vertex(graph, target):
        raise ValueError("Целевая вершина отсутствует в графе")
    return None


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["A", "D"], "D": []}
    order, distances, _ = breadth_first_search_details(graph, "A")
    print(order)
    print(distances)
    print(shortest_path(graph, "A", "D"))
