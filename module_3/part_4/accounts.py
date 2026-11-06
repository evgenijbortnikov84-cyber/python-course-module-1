import hashlib
import hmac
import json
import secrets
from getpass import getpass
from pathlib import Path
from tempfile import NamedTemporaryFile

ITERATIONS = 600_000
MIN_PASSWORD_LENGTH = 8
DUMMY_SALT = "00" * 16
DUMMY_HASH = "00" * 32


def account_path(login, directory=None):
    directory = Path(directory) if directory is not None else Path.home() / ".python_course_accounts"
    identifier = hashlib.sha256(login.encode("utf-8")).hexdigest()
    return directory / identifier / "account.json"


def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                               bytes.fromhex(salt), ITERATIONS).hex()


def validate_credentials(login, passwd):
    if not isinstance(login, str) or not login.strip() or len(login) > 64:
        raise ValueError("Логин должен содержать от 1 до 64 символов и не быть пустым")
    if login != login.strip():
        raise ValueError("Уберите пробелы по краям логина")
    if not isinstance(passwd, str) or len(passwd) < MIN_PASSWORD_LENGTH or not passwd.strip():
        raise ValueError("Пароль должен содержать не менее 8 символов и не состоять из пробелов")


def register(login, passwd, directory=None):
    """True при регистрации, False при занятом логине; ошибки ввода: ValueError."""
    validate_credentials(login, passwd)
    path = account_path(login, directory)
    if path.exists():
        return False
    salt = secrets.token_hex(16)
    record = {"login": login, "salt": salt, "hash": password_hash(passwd, salt)}
    content = json.dumps(record, ensure_ascii=False).encode("utf-8")
    path.parent.parent.mkdir(parents=True, exist_ok=True)
    pending = None
    try:
        with NamedTemporaryFile(dir=path.parent.parent, prefix=".pending-",
                                delete=False) as temporary:
            pending = Path(temporary.name)
            temporary.write(content)
        # Создание каталога резервирует логин; чужую запись не перезаписываем.
        try:
            path.parent.mkdir()
        except FileExistsError:
            return False
        try:
            pending.replace(path)
        except OSError:
            path.parent.rmdir()
            raise
    finally:
        if pending is not None:
            pending.unlink(missing_ok=True)
    return True


def valid_record(record, login):
    if not isinstance(record, dict) or record.get("login") != login:
        return False
    for key, size in (("salt", 32), ("hash", 64)):
        value = record.get(key)
        if (not isinstance(value, str) or len(value) != size
                or any(char not in "0123456789abcdef" for char in value)):
            return False
    return True


def login_function(login, passwd, directory=None):
    """Ошибка входа возвращает False, включая повреждённую запись."""
    record = None
    if isinstance(login, str) and isinstance(passwd, str):
        try:
            candidate = json.loads(account_path(login, directory).read_text(encoding="utf-8"))
            if valid_record(candidate, login):
                record = candidate
        except (OSError, ValueError, UnicodeError):
            pass
    # Для отсутствующего/битого аккаунта выполняется та же дорогая операция.
    # Это убирает мгновенный отказ, но не гарантирует тождественное время I/O.
    salt = record["salt"] if record is not None else DUMMY_SALT
    expected = record["hash"] if record is not None else DUMMY_HASH
    actual = password_hash(passwd if isinstance(passwd, str) else "", salt)
    matches = hmac.compare_digest(actual, expected)
    return record is not None and matches


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
