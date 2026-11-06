import re

MAX_WORD_LENGTH = 5  # Возвращаем слова строго короче пяти символов.
# [^\W\d_] означает символ слова, кроме цифр и подчёркивания.
# Внутренние дефисы и апострофы соединяют части одного слова.
WORD_PATTERN = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*")


def short_words(text, max_length=MAX_WORD_LENGTH):
    if type(max_length) is not int or max_length <= 0:
        raise ValueError("Порог длины должен быть положительным целым числом")
    return [word for word in WORD_PATTERN.findall(text) if len(word) < max_length]


if __name__ == "__main__":
    try:
        print(short_words(input("Введите одну строку текста: ")))
    except EOFError:
        print("Ошибка: текст не введён")
