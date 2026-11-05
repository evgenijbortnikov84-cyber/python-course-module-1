# Основы Python · Модули 1 и 3

[Скриншоты кода и результатов запуска](screenshots/)

## Модуль 1

Шесть самостоятельных программ для Python 3. Дополнительные библиотеки не требуются.

| Часть | Уровень | Решение |
| --- | --- | --- |
| 1 | 1 | [Вычисление выражения](module_1/part_1/level_1.py) |
| 1 | 2 | [Движение по МКАД](module_1/part_1/level_2.py) |
| 1 | 3 | [Максимум двух чисел](module_1/part_1/level_3.py) |
| 2 | 1 | [Совпадающие числа](module_1/part_2/level_1.py) |
| 2 | 2 | [Ход ладьи](module_1/part_2/level_2.py) |
| 2 | 3 | [Проверка пароля](module_1/part_2/level_3.py) |

## Запуск

Из корня репозитория выполните команду для нужного файла. Например, для задачи про МКАД:

```powershell
python module_1/part_1/level_2.py
```

Введите скорость и время на отдельных строках. При вводе 30 км/ч и 5 часов программа выведет 41 — отметку на дороге длиной 109 км.

## Модуль 3

| Задание | Решение | Скриншот |
| --- | --- | --- |
| 1.1 Вклад | [Код](module_3/part_1/level_1.py) | [Открыть](screenshots/m3_1_1.png) |
| 1.2 Цикл while | [Код](module_3/part_1/level_2.py) | [Открыть](screenshots/m3_1_2.png) |
| 1.3 Сумма цифр | [Код](module_3/part_1/level_3.py) | [Открыть](screenshots/m3_1_3.png) |
| 2.1 Повторяющиеся элементы | [Код](module_3/part_2/level_1.py) | [Открыть](screenshots/m3_2_1.png) |
| 2.2 Максимум матрицы | [Код](module_3/part_2/level_2.py) | [Открыть](screenshots/m3_2_2.png) |
| 2.3 Ключи и значения | [Код](module_3/part_2/level_3.py) | [Открыть](screenshots/m3_2_3.png) |
| 3.1 Площадь треугольника | [Код](module_3/part_3/level_1.py) | [Открыть](screenshots/m3_3_1.png) |
| 3.2 Короткие слова | [Код](module_3/part_3/level_2.py) | [Открыть](screenshots/m3_3_2.png) |
| 3.3 Максимальное число | [Код](module_3/part_3/level_3.py) | [Открыть](screenshots/m3_3_3.png) |
| 4.1 Регистрация | [Код](module_3/part_4/accounts.py) | [Открыть](screenshots/m3_4_1.png) |
| 4.2 Проверка повторного логина | [Код](module_3/part_4/accounts.py) | [Открыть](screenshots/m3_4_2.png) |
| 4.3 Вход | [Код](module_3/part_4/accounts.py) | [Открыть](screenshots/m3_4_3.png) |
| Список покупок | [Код](module_3/lesson_3/shopping_list.py) | [Открыть](screenshots/shopping_list.png) |

Из корня репозитория запустите `python -m unittest discover -s tests -v`, чтобы проверить список покупок.
