import json
import os
import secrets
import stat
from dataclasses import dataclass, fields
from pathlib import Path


@dataclass
class Model:
    @classmethod
    def validate(cls, values):
        declared = fields(cls)
        if not isinstance(values, dict) or set(values) != {field.name for field in declared}:
            raise ValueError("Набор полей не соответствует модели")
        for field in declared:
            # Поддерживаются конкретные типы, без Union и строковых аннотаций.
            if type(values[field.name]) is not field.type:
                raise ValueError(f"Неверный тип поля {field.name}")

    def save(self, filename):
        """Заменяет JSON-файл после успешной записи; возвращает None."""
        values = {field.name: getattr(self, field.name) for field in fields(self)}
        self.validate(values)
        content = json.dumps(values, ensure_ascii=False, indent=2)
        path = Path(filename)
        mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
        temporary_path = path.with_name(".model-" + secrets.token_hex(16) + ".tmp")
        pending = None
        try:
            # Режим x не перезаписывает чужой файл при совпадении имени.
            # Новый файл получает обычные права open: 0666 с учётом umask на POSIX.
            with open(temporary_path, "x", encoding="utf-8") as temporary:
                pending = temporary_path
                temporary.write(content)
            if mode is not None and os.name == "posix":
                pending.chmod(mode)
            pending.replace(path)
        finally:
            if pending is not None:
                pending.unlink(missing_ok=True)

    @classmethod
    def load(cls, filename):
        """Ошибки JSON/полей: ValueError; ошибки файловой системы: OSError."""
        try:
            values = json.loads(Path(filename).read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError("Файл содержит некорректный JSON") from error
        cls.validate(values)
        return cls(**values)


@dataclass
class Article(Model):
    title: str = "Заголовок"
    text: str = "Текст статьи"
    author: str = "Автор"


if __name__ == "__main__":
    article = Article()
    article.save("article.json")
    restored = Article.load("article.json")
    print(restored.title, restored.text, restored.author, sep="\n")
