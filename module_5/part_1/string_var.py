class StringVar:
    def __init__(self, value=""):
        self.set(value)

    def set(self, value):
        if not isinstance(value, str):
            raise TypeError("Ожидается строка")
        self._value = value

    def get(self):
        return self._value


if __name__ == "__main__":
    text = StringVar("Привет")
    print(text.get())
    text.set("Python")
    print(text.get())
