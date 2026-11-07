import re
import sys

MAX_WORD_LENGTH = 5  # Возвращаем слова строго короче пяти символов.
# [^\W\d_] означает символ слова, кроме цифр и подчёркивания.
# Внутренние дефисы и апострофы соединяют части одного слова.
WORD_PATTERN = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*")


def short_words(text, max_length=MAX_WORD_LENGTH):
    if type(max_length) is not int or max_length <= 0:
        raise ValueError("Порог длины должен быть положительным целым числом")
    return [word for word in WORD_PATTERN.findall(text) if len(word) < max_length]


if __name__ == "__main__":
    print("Введите текст. Завершение: Windows - Ctrl+Z и Enter; Linux/macOS - Ctrl+D.")
    print(short_words(sys.stdin.read()))
