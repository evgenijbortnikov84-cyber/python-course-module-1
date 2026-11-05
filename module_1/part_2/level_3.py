"""Часть 2, уровень 3: ввод пароля до выполнения всех условий."""

password = input("Введите пароль: ")

# Сравнения с lower() и upper() проверяют наличие букв обоих регистров.
while len(password) <= 8 or password == password.lower() or password == password.upper():
    print("Пароль должен быть длиннее 8 символов и содержать строчные и заглавные буквы.")
    password = input("Введите пароль: ")

print("Пароль принят.")
