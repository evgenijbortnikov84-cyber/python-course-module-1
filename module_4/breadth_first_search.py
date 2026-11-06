from collections import deque


def breadth_first_search_details(graph, start):
    """Вернуть (порядок, расстояния, предшественники) для невзвешенного графа.

    Граф задан словарём со списками соседей. Вершины должны быть хешируемыми.
    Вершина существует, если встречается среди ключей или соседей.
    Неизвестная начальная вершина вызывает ValueError.
    Время O(V + E), дополнительная память O(V).
    """
    vertices = set(graph)
    for neighbors in graph.values():
        vertices.update(neighbors)
    if start not in vertices:
        raise ValueError("Начальная вершина отсутствует в графе")

    queue = deque([start])
    distances = {start: 0}
    predecessors = {}
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.get(vertex, ()):
            if neighbor not in distances:
                # Отмечаем при добавлении, чтобы не ставить вершину повторно.
                distances[neighbor] = distances[vertex] + 1
                predecessors[neighbor] = vertex
                queue.append(neighbor)
    return order, distances, predecessors


def breadth_first_search(graph, start):
    """Вернуть порядок обхода достижимых вершин. Неизвестный start: ValueError."""
    order, _, _ = breadth_first_search_details(graph, start)
    return order


def shortest_path(graph, start, target):
    """Вернуть кратчайший путь по числу рёбер или None для недостижимой цели."""
    _, distances, predecessors = breadth_first_search_details(graph, start)
    if target not in distances:
        return None
    path = [target]
    while path[-1] != start:
        path.append(predecessors[path[-1]])
    path.reverse()
    return path


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["A", "D"], "D": []}
    order, distances, _ = breadth_first_search_details(graph, "A")
    print(order)
    print(distances)
    print(shortest_path(graph, "A", "D"))
