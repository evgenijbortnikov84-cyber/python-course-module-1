import json
import os
import stat
from pathlib import Path
from tempfile import NamedTemporaryFile


class Model:
    # Подкласс явно перечисляет поля и допустимые типы.
    fields = {}

    @classmethod
    def validate(cls, values):
        if not isinstance(values, dict) or set(values) != set(cls.fields):
            raise ValueError("Набор полей не соответствует модели")
        for name, expected_type in cls.fields.items():
            if not isinstance(values[name], expected_type):
                raise ValueError(f"Неверный тип поля {name}")

    def save(self, filename):
        """Атомарно заменяет JSON-файл; ничего не возвращает."""
        # Произвольные свойства не перебираются. Поля задаёт автор модели.
        values = {name: getattr(self, name) for name in self.fields}
        self.validate(values)
        content = json.dumps(values, ensure_ascii=False, indent=2)
        path = Path(filename)
        mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
        pending = None
        try:
            with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                    prefix=".model-", suffix=".tmp", delete=False) as temporary:
                pending = Path(temporary.name)
                temporary.write(content)
            # На POSIX сохраняем прежние права. Новый файл остаётся 0600.
            # На Windows доступ определяется ACL каталога, а не POSIX mode.
            if mode is not None and os.name == "posix":
                pending.chmod(mode)
            pending.replace(path)
        finally:
            if pending is not None:
                pending.unlink(missing_ok=True)

    @classmethod
    def load(cls, filename):
        """Загружает модель с конструктором без аргументов.

        Ошибки структуры/JSON: ValueError; ошибки доступа: OSError.
        """
        try:
            values = json.loads(Path(filename).read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("Файл содержит некорректный JSON") from error
        cls.validate(values)
        model = cls()
        for name, value in values.items():
            setattr(model, name, value)
        return model


class Article(Model):
    fields = {"title": str, "text": str, "author": str}
    title = "Заголовок"
    text = "Текст статьи"
    author = "Автор"


if __name__ == "__main__":
    article = Article()
    article.save("article.json")
    restored = Article.load("article.json")
    print(restored.title, restored.text, restored.author, sep="\n")
