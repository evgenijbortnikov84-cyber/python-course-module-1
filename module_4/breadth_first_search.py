from collections import deque


def breadth_first_search(graph, start):
    """Обойти достижимые вершины по слоям. Граф задан списками соседей."""
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


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["A", "D"], "D": []}
    print(breadth_first_search(graph, "A"))  # ['A', 'B', 'C', 'D']
