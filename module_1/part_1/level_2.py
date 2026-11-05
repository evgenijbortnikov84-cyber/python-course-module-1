"""Часть 1, уровень 2: отметка на МКАД длиной 109 км."""

speed = int(input())
time = int(input())

# Остаток от деления учитывает любое количество полных кругов.
position = (speed * time) % 109
print(position)
