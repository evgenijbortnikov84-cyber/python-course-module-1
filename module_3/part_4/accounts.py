import hashlib
import hmac
import json
import secrets
from getpass import getpass
from pathlib import Path
from tempfile import NamedTemporaryFile


def account_path(login):
    directory = Path.home() / ".python_course_accounts"
    identifier = hashlib.sha256(login.encode()).hexdigest()
    return directory / identifier / "account.json"


def password_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600_000).hex()


def register(login, passwd):
    path = account_path(login)
    if path.exists():
        return False
    salt = secrets.token_hex(16)
    record = {"login": login, "salt": salt, "hash": password_hash(passwd, salt)}
    path.parent.parent.mkdir(exist_ok=True)
    with NamedTemporaryFile(dir=path.parent.parent, delete=False) as temporary:
        pending = Path(temporary.name)
        temporary.write(json.dumps(record).encode())
    try:
        # Публикуем готовую запись, только если логин всё ещё свободен.
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
        pending.unlink(missing_ok=True)
    return True


def login_function(login, passwd):
    try:
        record = json.loads(account_path(login).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False
    return hmac.compare_digest(password_hash(passwd, record["salt"]), record["hash"])


if __name__ == "__main__":
    action = input("Регистрация или вход? ").strip().lower()
    if action in ("регистрация", "вход"):
        login = input("Логин: ")
        password = getpass("Пароль: ")
        if action == "регистрация":
            print("Пользователь создан" if register(login, password) else "Логин занят")
        else:
            print("Вход выполнен" if login_function(login, password) else "Ошибка входа")
    else:
        print("Неизвестная команда")
