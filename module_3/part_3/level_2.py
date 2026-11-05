import re
import sys


def short_words(text):
    words = re.findall(r"[^\W\d_]+", text)
    return [word for word in words if len(word) < 5]


if __name__ == "__main__":
    print("Введите текст. Для завершения в Windows нажмите Ctrl+Z и Enter.")
    print(short_words(sys.stdin.read()))
