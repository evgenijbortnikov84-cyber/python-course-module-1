import hashlib
import hmac
import json
import secrets
import unicodedata
from getpass import getpass
from pathlib import Path
from tempfile import NamedTemporaryFile

ITERATIONS = 600_000
LEGACY_ITERATIONS = 600_000  # Старый формат всегда использовал именно это число.
FORMAT_VERSION = 2
MAX_PASSWORD_LENGTH = 128


def normalize_login(login):
    if not isinstance(login, str):
        raise ValueError("Логин должен быть строкой")
    login = unicodedata.normalize("NFC", login)
    if not login.strip() or len(login) > 64 or login != login.strip():
        raise ValueError("Логин: от 1 до 64 символов, без пробелов по краям")
    return login


def account_path(login, directory=None):
    directory = Path(directory) if directory is not None else Path.home() / ".python_course_accounts"
    identifier = hashlib.sha256(normalize_login(login).encode("utf-8")).hexdigest()
    return directory / identifier / "account.json"


def find_account_path(login, directory=None):
    """Учитывает старые записи с ненормализованным именем, не переписывая их."""
    path = account_path(login, directory)
    matches = {path} if path.exists() else set()
    for old_path in path.parent.parent.glob("*/account.json"):
        try:
            record = json.loads(old_path.read_text(encoding="utf-8"))
            if isinstance(record, dict) and normalize_login(record.get("login")) == normalize_login(login):
                matches.add(old_path)
        except (OSError, ValueError):
            continue
    if len(matches) > 1:
        raise ValueError("Несколько старых аккаунтов имеют одинаковый нормализованный логин")
    return next(iter(matches)) if matches else path


def password_hash(password, salt, iterations):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                               bytes.fromhex(salt), iterations).hex()


def register(login, passwd, directory=None):
    """Локальный учебный пример: True при успехе, False при занятом логине."""
    login = normalize_login(login)
    if not isinstance(passwd, str) or not 8 <= len(passwd) <= MAX_PASSWORD_LENGTH or not passwd.strip():
        raise ValueError("Пароль: от 8 до 128 символов, не только пробелы")
    path = find_account_path(login, directory)
    if path.exists():
        return False
    salt = secrets.token_hex(16)
    record = {"version": FORMAT_VERSION, "iterations": ITERATIONS, "login": login,
              "salt": salt, "hash": password_hash(passwd, salt, ITERATIONS)}
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = None
    try:
        with NamedTemporaryFile(dir=path.parent, prefix=".pending-", delete=False) as temporary:
            pending = Path(temporary.name)
            temporary.write(json.dumps(record, ensure_ascii=False).encode("utf-8"))
        # Учебная программа рассчитана на один запущенный экземпляр.
        # Пустой каталог после сбоя можно использовать повторно.
        if path.exists():
            return False
        pending.replace(path)
    finally:
        if pending is not None:
            pending.unlink(missing_ok=True)
    return True


def record_iterations(record):
    if "version" not in record and "iterations" not in record:
        return LEGACY_ITERATIONS
    if type(record.get("version")) is not int or record["version"] != FORMAT_VERSION:
        raise ValueError("Неизвестная версия записи")
    value = record.get("iterations")
    if type(value) is not int or not 1 <= value <= 2_000_000:
        raise ValueError("Некорректное число итераций")
    return value


def login_function(login, passwd, directory=None):
    """Не обещает скрыть существование логина или выровнять время ответа."""
    if not isinstance(passwd, str) or len(passwd) > MAX_PASSWORD_LENGTH:
        return False
    try:
        login = normalize_login(login)
        record = json.loads(find_account_path(login, directory).read_text(encoding="utf-8"))
        if not isinstance(record, dict) or normalize_login(record.get("login")) != login:
            return False
        for key, size in (("salt", 32), ("hash", 64)):
            value = record.get(key)
            if (not isinstance(value, str) or len(value) != size
                    or any(char not in "0123456789abcdef" for char in value)):
                return False
        actual = password_hash(passwd, record["salt"], record_iterations(record))
        return hmac.compare_digest(actual, record["hash"])
    except (OSError, ValueError):
        return False


def main():
    try:
        action = input("Регистрация или вход? ").strip().lower()
        if action not in ("регистрация", "вход"):
            print("Неизвестная команда")
            return
        login = input("Логин: ")
        password = getpass("Пароль: ")
        if action == "регистрация":
            print("Пользователь создан" if register(login, password) else "Логин занят")
        else:
            print("Вход выполнен" if login_function(login, password) else "Ошибка входа")
    except (ValueError, EOFError) as error:
        print(f"Ошибка: {error}")
    except OSError:
        print("Ошибка: не удалось прочитать или сохранить данные аккаунта")


if __name__ == "__main__":
    main()
