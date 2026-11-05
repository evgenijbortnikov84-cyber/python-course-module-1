"""Проверки программы через реальный запуск и ввод команд."""

import os
from pathlib import Path
import subprocess
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PROGRAM = REPO_ROOT / "module_3" / "lesson_3" / "shopping_list.py"


class ShoppingListTests(unittest.TestCase):
    def run_program(self, *lines):
        result = subprocess.run(
            [sys.executable, str(PROGRAM)],
            input="\n".join(lines) + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_add_sum_sort_and_delete(self):
        output = self.run_program(
            "добавить", "шампунь 1", "белый хлеб 2", "шампунь 1", "",
            "показать", "удалить", "шампунь", "показать", "выход",
        )
        self.assertIn("белый хлеб 2.0\nшампунь 2.0\n", output)
        self.assertEqual(output.count("шампунь 2.0\n"), 1)
        self.assertEqual(output.count("белый хлеб 2.0\n"), 2)

    def test_fractional_quantities_and_multiple_batches(self):
        output = self.run_program(
            "добавить", "яблоки 0.5", "",
            "добавить", "яблоки 1.25", "", "показать", "выход",
        )
        self.assertIn("яблоки 1.75\n", output)

    def test_empty_list_and_missing_position(self):
        output = self.run_program(
            "показать", "удалить", "молоко", "добавить", "",
            "показать", "выход",
        )
        self.assertEqual(output.count("Список пуст."), 2)

    def test_command_case_spaces_and_unknown_command(self):
        output = self.run_program("неизвестно", "  ПОКАЗАТЬ  ", "  ВЫХОД  ")
        self.assertEqual(
            output.count("Команды: добавить, удалить, показать, выход"), 2
        )
        self.assertIn("Список пуст.", output)

    def test_list_is_not_saved_between_runs(self):
        first_output = self.run_program(
            "добавить", "молоко 1", "", "показать", "выход"
        )
        self.assertIn("молоко 1.0\n", first_output)
        second_output = self.run_program("показать", "выход")
        self.assertIn("Список пуст.", second_output)
        self.assertNotIn("молоко", second_output)


if __name__ == "__main__":
    unittest.main()
