"""Часть 2, уровень 2: ход ладьи между двумя различными клетками."""

column_1 = int(input())
row_1 = int(input())
column_2 = int(input())
row_2 = int(input())

if column_1 == column_2 or row_1 == row_2:
    print("YES")
else:
    print("NO")
