import json
from pathlib import Path
from tempfile import NamedTemporaryFile


class Model:
    def save(self, filename):
        values = {}
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                if not callable(value):
                    values[name] = value
        # Сериализация завершается до изменения файла.
        content = json.dumps(values, ensure_ascii=False, indent=2)
        path = Path(filename)
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                delete=False) as temporary:
            pending = Path(temporary.name)
            temporary.write(content)
        try:
            pending.replace(path)
        finally:
            pending.unlink(missing_ok=True)
        return values


class Article(Model):
    title = "Заголовок"
    text = "Текст статьи"
    author = "Автор"


if __name__ == "__main__":
    article = Article()
    print(article.save("article.json"))
