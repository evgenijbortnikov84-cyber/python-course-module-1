import io
import itertools
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from decimal import Decimal, InvalidOperation
from pathlib import Path
from unittest.mock import patch

from module_3.part_1.level_1 import years_to_target
from module_3.part_1.level_2 import repeat_message, MESSAGE
from module_3.part_1.level_3 import digit_sum
from module_3.part_2.level_1 import find_duplicates
from module_3.part_2.level_2 import matrix_max
from module_3.part_2.level_3 import group_names_by_id
from module_3.part_3.level_1 import area
from module_3.part_3.level_2 import short_words
from module_3.part_3.level_3 import largest_number, compare
from module_3.part_4 import accounts
from module_3.lesson_3.shopping_list import add_position, remove_position, show_shopping_list

ROOT = Path(__file__).resolve().parents[1]


class Part1Tests(unittest.TestCase):
    def test_year_limit(self):
        with self.assertRaises(RuntimeError):
            years_to_target(1_000_000, "1e30", "0.001")
        self.assertEqual(years_to_target(100, 121, 10, max_years=2), 2)
        with self.assertRaises(RuntimeError):
            years_to_target(100, 121, 10, max_years=1)
        self.assertEqual(years_to_target(100, 100, 0, max_years=0), 0)
        with self.assertRaises(ValueError):
            years_to_target(100, 121, 10, max_years=-1)


    def test_deposit_growth(self):
        self.assertEqual(years_to_target("100", "121", "10"), 2)
        self.assertEqual(years_to_target("100", "100", "0"), 0)
        self.assertEqual(years_to_target("120", "100", "-10"), 0)

    def test_deposit_unreachable(self):
        for values in ((100, 200, 0), (100, 200, -1), (0, 200, 10), (1, 2, "0.1")):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    years_to_target(*values)

    def test_deposit_floor_policy(self):
        self.assertEqual(years_to_target("100.01", "110.02", "10"), 2)

    def test_deposit_invalid(self):
        for value in ("NaN", "Infinity", "-1", "текст"):
            with self.subTest(value=value), self.assertRaises((ValueError, InvalidOperation)):
                years_to_target(value, 200, 10)

    def test_repeat(self):
        output = io.StringIO()
        with redirect_stdout(output):
            repeat_message(2)
        self.assertEqual(output.getvalue(), (MESSAGE + "\n") * 2)

    def test_repeat_invalid(self):
        for count in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                repeat_message(count)

    def test_digit_sum(self):
        for number, expected in ((0, 0), (123, 6), (-507, 12), (10**30 + 1, 2)):
            self.assertEqual(digit_sum(number), expected)
        with self.assertRaises(ValueError):
            digit_sum("123")


class Part2Tests(unittest.TestCase):
    def test_types_do_not_merge(self):
        self.assertEqual(find_duplicates([1, True, 1.0, "1"]), [])
        result = find_duplicates([1, True, 1.0, "1"] * 2)
        self.assertEqual([type(value) for value in result], [int, bool, float, str])

    def test_repeated_name_pairs_and_numeric_ids(self):
        self.assertEqual(group_names_by_id([("a", 1), ("a", 2), ("b", 1)]),
                         {1: ["a", "b"], 2: ["a"]})


    def test_duplicates(self):
        self.assertEqual(find_duplicates([1, 4, 1, 6, "hello", "a", 5, "hello"]), [1, "hello"])
        self.assertEqual(find_duplicates([2, 1, 1, 2, 2]), [2, 1])
        self.assertEqual(find_duplicates([]), [])
        self.assertEqual(find_duplicates([1, 2, 3]), [])

    def test_duplicates_single_pass_input(self):
        self.assertEqual(find_duplicates(iter([1, 1, 2, 2])), [1, 2])

    def test_unhashable_duplicate_input(self):
        with self.assertRaises(TypeError):
            find_duplicates([[1], [1]])

    def test_matrix(self):
        self.assertEqual(matrix_max([[-5, -2], [-3]]), -2)
        self.assertEqual(matrix_max([[7]]), 7)
        self.assertEqual(matrix_max([[9, 70], [100, 1]]), 100)

    def test_empty_matrix_or_row(self):
        for matrix in ([], [[]], [[1], []]):
            with self.assertRaises(ValueError):
                matrix_max(matrix)

    def test_matrix_nonfinite_or_wrong_type(self):
        for value in (float("nan"), float("inf"), "5", True):
            with self.assertRaises(ValueError):
                matrix_max([[value]])

    def test_group_ids(self):
        users = {"Анна": "id1", "Иван": "id1", "Ольга": "id2"}
        self.assertEqual(group_names_by_id(users), {"id1": ["Анна", "Иван"], "id2": ["Ольга"]})
        self.assertEqual(len(users), 3)
        self.assertEqual(group_names_by_id({}), {})


class Part3Tests(unittest.TestCase):
    def test_comparator_transitivity(self):
        values = ("0", "1", "12", "121", "1212", "3", "30", "9")
        for a, b, c in itertools.product(values, repeat=3):
            if compare(a, b) <= 0 and compare(b, c) <= 0:
                self.assertLessEqual(compare(a, c), 0, (a, b, c))


    def test_triangle(self):
        for sides in itertools.permutations((3, 4, 5)):
            self.assertEqual(area(*sides), 6.0)

    def test_invalid_triangle(self):
        for sides in ((1, 2, 3), (0, 2, 2), (-1, 2, 2), (1, 1, float("nan")),
                      (1, 1, float("inf"))):
            with self.assertRaises(ValueError):
                area(*sides)

    def test_short_words(self):
        self.assertEqual(short_words("Кот, слон и мышь!"), ["Кот", "слон", "и", "мышь"])
        self.assertEqual(short_words("из-за don't can't rock'n'roll"), [])
        self.assertEqual(short_words("из-за don't", 6), ["из-за", "don't"])
        self.assertEqual(short_words("a-b l’été 123 _"), ["a-b"])
        self.assertEqual(short_words(""), [])

    def test_short_words_custom_limit(self):
        self.assertEqual(short_words("я ты дом", 3), ["я", "ты"])
        with self.assertRaises(ValueError):
            short_words("текст", 0)

    def test_largest_number(self):
        self.assertEqual(largest_number([3, 30, 34, 5, 9]), 9534330)
        self.assertEqual(largest_number([0, 0]), 0)
        self.assertEqual(largest_number(iter([12, 121])), 12121)

    def test_largest_number_against_all_permutations(self):
        for values in ((12, 121, 9), (0, 1, 10), (3, 30, 34, 5, 9), (9, 91, 90)):
            expected = max(int("".join(map(str, order))) for order in itertools.permutations(values))
            self.assertEqual(largest_number(values), expected)

    def test_largest_invalid(self):
        for values in ([], [-12, 5], [1.5], ["2"], [True]):
            with self.assertRaises(ValueError):
                largest_number(values)


class ShoppingFunctionsTests(unittest.TestCase):
    def test_add_remove(self):
        shopping = {}
        add_position(shopping, " белый хлеб ", 1.0)
        add_position(shopping, "белый хлеб", 1)
        self.assertEqual(shopping, {"белый хлеб": 2})
        self.assertIs(type(shopping["белый хлеб"]), int)
        remove_position(shopping, "нет такого")
        remove_position(shopping, "белый хлеб")
        self.assertEqual(shopping, {})

    def test_fractions_become_int_when_sum_integral(self):
        shopping = {}
        add_position(shopping, "яблоки", 0.5)
        add_position(shopping, "яблоки", 1.5)
        self.assertIs(type(shopping["яблоки"]), int)
        self.assertEqual(shopping["яблоки"], 2)

    def test_invalid_quantity_preserves_list(self):
        shopping = {"хлеб": 1}
        for value in (-1, 0, float("nan"), float("inf"), "2", True):
            with self.assertRaises(ValueError):
                add_position(shopping, "хлеб", value)
            self.assertEqual(shopping, {"хлеб": 1})
        with self.assertRaises(ValueError):
            add_position(shopping, " ", 1)

    def test_overflow_preserves_list(self):
        shopping = {"песок": 1e308}
        with self.assertRaises(ValueError):
            add_position(shopping, "песок", 1e308)
        self.assertEqual(shopping, {"песок": 1e308})

    def test_sorted_output(self):
        output = io.StringIO()
        with redirect_stdout(output):
            show_shopping_list({"яблоки": 1.75, "хлеб": 2})
        self.assertEqual(output.getvalue(), "хлеб 2\nяблоки 1.75\n")


class ProgramTests(unittest.TestCase):
    def run_script(self, script, data):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "module_3" / script)], input=data,
            capture_output=True, text=True, encoding="utf-8", timeout=5,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_expected_outputs(self):
        cases = (
            ("part_1/level_1.py", "100\n121\n10\n", "2\n"),
            ("part_1/level_2.py", "2\n", (MESSAGE + "\n") * 2),
            ("part_1/level_3.py", "-507\n", "12\n"),
            ("part_1/level_2.py", "0\n", ""),
            ("part_2/level_1.py", "", "[1, 'hello']\n"),
            ("part_2/level_2.py", "", "100\n"),
            ("part_2/level_3.py", "", "{1: ['Анна', 'Иван'], 2: ['Анна']}\n"),
            ("part_3/level_1.py", "3 4 5\n", "Три стороны через пробел: 6.0\n"),
            ("part_3/level_2.py", "Кот из-за don't\n\nи мышь\n",
             "Введите текст. Завершение: Windows - Ctrl+Z и Enter; Linux/macOS - Ctrl+D.\n['Кот', 'и', 'мышь']\n"),
            ("part_3/level_3.py", "3 30 34 5 9\n", "Неотрицательные целые через пробел: 9534330\n"),
        )
        for script, data, expected in cases:
            with self.subTest(script=script):
                self.assertEqual(self.run_script(script, data), expected)

    def test_invalid_inputs_without_traceback(self):
        cases = (
            ("part_1/level_1.py", "буква\n100\n10\n"),
            ("part_1/level_1.py", "NaN\n100\n10\n"),
            ("part_1/level_2.py", "нет\n"), ("part_1/level_2.py", "-1\n"),
            ("part_1/level_3.py", "нет\n"),
            ("part_3/level_1.py", "1 2\n"), ("part_3/level_1.py", "1 2 3\n"),
            ("part_3/level_3.py", "-12 5\n"), ("part_3/level_3.py", "\n"),
        )
        for script, data in cases:
            with self.subTest(script=script, data=data):
                self.assertIn("Ошибка:", self.run_script(script, data))

    def test_shopping_recovers_after_invalid_input(self):
        output = self.run_script("lesson_3/shopping_list.py",
            "добавить\nхлеб\nхлеб много\nхлеб -1\nхлеб 0\nхлеб nan\nхлеб 2\n\nпоказать\nвыход\n")
        self.assertEqual(output.count("Ошибка:"), 5)
        self.assertIn("хлеб 2\n", output)
        self.assertNotIn("хлеб 2.0", output)


class AccountsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.password = "пароль123"

    def register(self, login="Анна"):
        return accounts.register(login, self.password, self.directory)

    def test_registration_and_login_real_hash(self):
        self.assertTrue(self.register())
        path = accounts.account_path("Анна", self.directory)
        record = json.loads(path.read_text(encoding="utf-8"))
        self.assertNotIn(self.password, path.read_text(encoding="utf-8"))
        self.assertEqual(len(record["salt"]), 32)
        self.assertTrue(accounts.login_function("Анна", self.password, self.directory))
        self.assertFalse(accounts.login_function("Анна", "не тот пароль", self.directory))
        before = path.read_bytes()
        self.assertFalse(self.register())
        self.assertEqual(path.read_bytes(), before)

    def test_random_salts(self):
        with patch.object(accounts, "password_hash", return_value="a" * 64):
            self.register("Анна")
            self.register("Иван")
        records = [json.loads(accounts.account_path(name, self.directory).read_text(encoding="utf-8"))
                   for name in ("Анна", "Иван")]
        self.assertNotEqual(records[0]["salt"], records[1]["salt"])

    def test_invalid_credentials(self):
        for login, password in (("", self.password), (" ", self.password), (" Анна", self.password),
                                ("x" * 65, self.password), ("Анна", ""), ("Анна", "123"),
                                ("Анна", " " * 8), ("Анна", "x" * 129)):
            with self.assertRaises(ValueError):
                accounts.register(login, password, self.directory)
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_missing_and_corrupt_records(self):
        path = accounts.account_path("Анна", self.directory)
        path.parent.mkdir()
        contents = (None, "{", "[]", "{}", '{"login": "Анна", "salt": "bad"}')
        for content in contents:
            with self.subTest(content=content):
                if content is not None:
                    path.write_text(content, encoding="utf-8")
                self.assertFalse(accounts.login_function("Анна", self.password, self.directory))

    def test_corrupt_encoding(self):
        path = accounts.account_path("Анна", self.directory)
        path.parent.mkdir()
        path.write_bytes(b"\xff")
        with patch.object(accounts, "password_hash", return_value="ab" * 32):
            self.assertFalse(accounts.login_function("Анна", self.password, self.directory))

    def test_write_failure_cleans_pending(self):
        factory = accounts.NamedTemporaryFile
        class FailingFile:
            def __init__(self, **kwargs):
                self.file = factory(**kwargs)
                self.name = self.file.name
            def __enter__(self):
                return self
            def write(self, content):
                self.file.write(content[:3])
                raise OSError("Имитируем сбой записи")
            def __exit__(self, *args):
                self.file.close()
        with patch.object(accounts, "password_hash", return_value="ab" * 32):
            with patch.object(accounts, "NamedTemporaryFile", FailingFile):
                with self.assertRaises(OSError):
                    self.register()
        self.assertFalse(any(p.is_file() for p in self.directory.rglob("*")))

    def test_publish_failure_cleans_pending_and_allows_retry(self):
        with patch.object(accounts, "password_hash", return_value="ab" * 32):
            with patch.object(Path, "replace", side_effect=OSError("Имитируем сбой публикации")):
                with self.assertRaises(OSError):
                    self.register()
        self.assertFalse(any(p.is_file() for p in self.directory.rglob("*")))
        self.assertTrue(self.register())

    def test_empty_directory_reused(self):
        path = accounts.account_path("Анна", self.directory)
        path.parent.mkdir()
        with patch.object(accounts, "password_hash", return_value="ab" * 32):
            self.assertTrue(self.register())
        self.assertEqual(list(path.parent.iterdir()), [path])

    def test_path_stays_under_storage(self):
        path = accounts.account_path("../../outside", self.directory)
        self.assertEqual(path.parent.parent, self.directory)
        self.assertEqual(len(path.parent.name), 64)

    def test_version_and_saved_iterations(self):
        with patch.object(accounts, "ITERATIONS", 1000):
            self.register()
        path = accounts.account_path("Анна", self.directory)
        record = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual((record["version"], record["iterations"]), (2, 1000))
        with patch.object(accounts, "ITERATIONS", 2000):
            self.assertTrue(accounts.login_function("Анна", self.password, self.directory))

    def test_legacy_and_unicode(self):
        import hashlib
        # Старая запись: ненормализованный логин, нет версии и числа итераций.
        login = "е\u0308ж"
        old_path = self.directory / hashlib.sha256(login.encode()).hexdigest() / "account.json"
        old_path.parent.mkdir()
        salt = "ab" * 16
        record = {"login": login, "salt": salt,
                  "hash": accounts.password_hash(self.password, salt, 600_000)}
        old_path.write_text(json.dumps(record), encoding="utf-8")
        before = old_path.read_bytes()
        with patch.object(accounts, "ITERATIONS", 1000):
            self.assertTrue(accounts.login_function("ёж", self.password, self.directory))
            self.assertFalse(accounts.register("ёж", self.password, self.directory))
        self.assertEqual(old_path.read_bytes(), before)

    def test_normalized_registration(self):
        with patch.object(accounts, "ITERATIONS", 1000):
            self.assertTrue(accounts.register("е\u0308ж", self.password, self.directory))
            self.assertFalse(accounts.register("ёж", self.password, self.directory))
            self.assertTrue(accounts.login_function("ёж", self.password, self.directory))
        self.assertEqual(accounts.account_path("е\u0308ж", self.directory),
                         accounts.account_path("ёж", self.directory))
        # NFC не объединяет похожие буквы разных алфавитов.
        self.assertNotEqual(accounts.normalize_login("a"), accounts.normalize_login("а"))

    def test_password_upper_bound(self):
        with patch.object(accounts, "ITERATIONS", 1000):
            self.assertTrue(accounts.register("Анна", "x" * 128, self.directory))
            self.assertTrue(accounts.login_function("Анна", "x" * 128, self.directory))
        with patch.object(accounts, "password_hash") as hasher:
            self.assertFalse(accounts.login_function("Анна", "x" * 129, self.directory))
            hasher.assert_not_called()

    def test_reject_invalid_version_and_iterations(self):
        path = accounts.account_path("Анна", self.directory)
        path.parent.mkdir()
        base = {"login": "Анна", "salt": "ab" * 16, "hash": "cd" * 32}
        for extra in ({"version": 99, "iterations": 1000}, {"version": 2},
                      {"version": 2, "iterations": 0}, {"version": 2, "iterations": True},
                      {"version": 2, "iterations": 2_000_001}, {"iterations": 1000}):
            path.write_text(json.dumps(dict(base, **extra)), encoding="utf-8")
            self.assertFalse(accounts.login_function("Анна", self.password, self.directory))

    def test_default_directory(self):
        with patch.object(Path, "home", return_value=self.directory):
            self.assertEqual(accounts.account_path("Анна").parent.parent,
                             self.directory / ".python_course_accounts")

    def test_main_three_scenarios(self):
        # Проверяем разные ответы 4.1, 4.2, 4.3, используя временное хранилище.
        with patch.object(Path, "home", return_value=self.directory):
            with patch.object(accounts, "getpass", return_value=self.password):
                for action, expected in (("регистрация", "Пользователь создан\n"),
                                         ("регистрация", "Логин занят\n"),
                                         ("вход", "Вход выполнен\n")):
                    with self.subTest(action=action, expected=expected):
                        output = io.StringIO()
                        with patch("builtins.input", side_effect=[action, "Анна"]), redirect_stdout(output):
                            accounts.main()
                        self.assertEqual(output.getvalue(), expected)

    def test_main_input_and_storage_errors(self):
        for error, expected in ((ValueError("Неверный пароль"), "Ошибка: Неверный пароль\n"),
                                (OSError("Нет доступа"), "Ошибка: не удалось прочитать или сохранить данные аккаунта\n")):
            with patch("builtins.input", side_effect=["регистрация", "Анна"]):
                with patch.object(accounts, "getpass", return_value=self.password):
                    with patch.object(accounts, "register", side_effect=error):
                        output = io.StringIO()
                        with redirect_stdout(output):
                            accounts.main()
                        self.assertEqual(output.getvalue(), expected)


if __name__ == "__main__":
    unittest.main()
