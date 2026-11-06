import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from module_5.part_1.string_var import StringVar
from module_5.part_1.point import Point
from module_5.part_1.warrior import Warrior
from module_5.part_1.arena import ArenaWarrior, Arena, RandomSource, Hit, ATTACK, DEFEND
from module_5.part_2.model import Article, Model


class FixedSource:
    def __init__(self, actions=(ATTACK, ATTACK)):
        self.actions = iter(actions)

    def choose_action(self):
        return next(self.actions)

    def roll_damage(self, bounds):
        return bounds[1]


class BasicTests(unittest.TestCase):
    def test_string_set_get(self):
        value = StringVar()
        self.assertEqual(value.get(), "")
        value.set("Привет")
        self.assertEqual(value.get(), "Привет")

    def test_string_invalid_constructor(self):
        with self.assertRaises(TypeError):
            StringVar(5)

    def test_string_invalid_set_preserves_value(self):
        value = StringVar("текст")
        with self.assertRaises(TypeError):
            value.set(None)
        self.assertEqual(value.get(), "текст")

    def test_point_move_and_distance(self):
        value = Point(3, 4)
        self.assertEqual(value.distance_to(Point()), 5)
        value.move(1, -2)
        self.assertEqual(value, Point(4, 2))

    def test_point_equality(self):
        self.assertEqual(Point(1, 2), Point(1, 2))
        self.assertNotEqual(Point(1, 2), Point(2, 1))
        self.assertNotEqual(Point(1, 2), (1, 2))
        self.assertIs(Point().__eq__(None), NotImplemented)

    def test_simple_attack_without_output(self):
        first, second = Warrior("A"), Warrior("B")
        with patch("builtins.print") as output:
            self.assertEqual(first.attack(second), 20)
        output.assert_not_called()
        self.assertEqual((first.health, second.health), (100, 80))

    def test_health_validation(self):
        warrior = Warrior("A")
        for damage in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                warrior.take_damage(damage)
        self.assertEqual(warrior.take_damage(150), 100)
        self.assertEqual(warrior.health, 0)
        with self.assertRaises(AttributeError):
            warrior.health = -10

    def test_mercy(self):
        warrior = Warrior("A")
        warrior.take_damage(100)
        warrior.finish(spare=True)
        self.assertEqual(warrior.health, 1)
        warrior.finish(spare=False)
        self.assertEqual(warrior.health, 0)


class ArenaTests(unittest.TestCase):
    def pair(self):
        return ArenaWarrior("A"), ArenaWarrior("B")

    def test_inherits_common_warrior(self):
        self.assertIsInstance(ArenaWarrior("A"), Warrior)

    def test_protection_and_armor(self):
        warrior = ArenaWarrior("A")
        warrior.defend()
        self.assertEqual(warrior.take_damage(Hit(30, 20, 10)), 20)
        self.assertEqual((warrior.health, warrior.armor), (80, 90))
        warrior.start_round()
        self.assertFalse(warrior.defending)

    def test_no_armor(self):
        warrior = ArenaWarrior("A")
        warrior.defend()
        warrior.take_damage(Hit(30, 0, 100))
        self.assertEqual(warrior.armor, 0)
        self.assertEqual(warrior.take_damage(Hit(30, 0, 10)), 30)
        self.assertEqual(warrior.armor, 0)

    def test_no_defense_does_not_consume_armor(self):
        warrior = ArenaWarrior("A")
        self.assertEqual(warrior.take_damage(Hit(30, 0, 100)), 30)
        self.assertEqual(warrior.armor, 100)

    def test_exhaustion(self):
        warrior = ArenaWarrior("A")
        source = FixedSource()
        for _ in range(10):
            self.assertEqual(warrior.prepare_hit(source).normal, 30)
        hit = warrior.prepare_hit(source)
        self.assertEqual((hit.normal, hit.protected, warrior.endurance), (10, 10, 0))

    def test_simultaneous_tie(self):
        first, second = self.pair()
        first.take_damage(70)
        second.take_damage(70)
        arena = Arena((first, second), FixedSource())
        self.assertEqual(len(arena.round()), 2)
        self.assertEqual((first.health, second.health), (0, 0))
        self.assertIsNone(arena.result().winner)
        self.assertEqual(len(arena.result().losers), 2)
        with self.assertRaises(ValueError):
            arena.round()

    def test_threshold_and_winner(self):
        first, second = self.pair()
        second.take_damage(89)
        arena = Arena((first, second))
        self.assertIsNone(arena.result())
        second.take_damage(1)
        self.assertIs(arena.result().winner, first)

    def test_seed_reproducibility(self):
        games = [Arena(self.pair(), RandomSource(42)) for _ in range(2)]
        outcomes = [game.play() for game in games]
        self.assertEqual(outcomes[0].winner.name, outcomes[1].winner.name)
        self.assertEqual([w.health for w in games[0].warriors],
                         [w.health for w in games[1].warriors])

    def test_round_limit(self):
        arena = Arena(self.pair(), FixedSource((DEFEND, DEFEND)))
        with self.assertRaises(RuntimeError):
            arena.play(max_rounds=1)

    def test_invalid_participants(self):
        first, second = self.pair()
        for warriors in ((first,), (first, first), (first, second, ArenaWarrior("C"))):
            with self.assertRaises(ValueError):
                Arena(warriors)

    def test_invalid_hit_does_not_change_state(self):
        warrior = ArenaWarrior("A")
        warrior.defend()
        with self.assertRaises(ValueError):
            warrior.take_damage(Hit(-1, 2, 5))
        self.assertEqual((warrior.health, warrior.armor), (100, 100))

    def test_invalid_action(self):
        arena = Arena(self.pair(), FixedSource(("ошибка", ATTACK)))
        with self.assertRaises(ValueError):
            arena.round()
        self.assertEqual(arena.warriors[0].health, 100)


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "article.json"

    def test_round_trip_and_return(self):
        article = Article()
        article.title = "Новый заголовок"
        self.assertIsNone(article.save(self.path))
        restored = Article.load(self.path)
        self.assertIsInstance(restored, Article)
        self.assertEqual(restored.title, article.title)
        self.assertEqual(restored.author, article.author)

    def test_overwrite(self):
        Article().save(self.path)
        article = Article()
        article.text = "Коротко"
        article.save(self.path)
        self.assertEqual(Article.load(self.path).text, "Коротко")

    def test_unrelated_property_not_called(self):
        class Extended(Article):
            @property
            def dangerous(self):
                raise AssertionError("Свойство нельзя вызывать")
        Extended().save(self.path)
        self.assertEqual(set(json.loads(self.path.read_text(encoding="utf-8"))),
                         {"title", "text", "author"})

    def test_invalid_json_and_structure(self):
        for content in ('{', '[]', '{}', '{"title": 1, "text": "", "author": ""}'):
            self.path.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                Article.load(self.path)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            Article.load(self.path)

    def test_serialization_failure_preserves_original(self):
        class Invalid(Model):
            fields = {"value": object}
            value = object()
        self.path.write_text("original", encoding="utf-8")
        with self.assertRaises(TypeError):
            Invalid().save(self.path)
        self.assertEqual(self.path.read_text(), "original")
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_write_failure_cleans_temp(self):
        from module_5.part_2 import model
        real_factory = model.NamedTemporaryFile

        class FailingFile:
            def __init__(self, **kwargs):
                self.file = real_factory(**kwargs)
                self.name = self.file.name
            def __enter__(self):
                return self
            def write(self, content):
                self.file.write(content[:3])
                raise OSError("Имитируем ошибку записи")
            def __exit__(self, *args):
                self.file.close()

        self.path.write_text("original", encoding="utf-8")
        with patch.object(model, "NamedTemporaryFile", FailingFile):
            with self.assertRaises(OSError):
                Article().save(self.path)
        self.assertEqual(self.path.read_text(), "original")
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_replace_failure_cleans_temp(self):
        self.path.write_text("original", encoding="utf-8")
        with patch.object(Path, "replace", side_effect=OSError("Нет доступа")):
            with self.assertRaises(OSError):
                Article().save(self.path)
        self.assertEqual(self.path.read_text(), "original")
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    @unittest.skipUnless(os.name == "posix", "Права POSIX проверяются на POSIX")
    def test_posix_permissions(self):
        Article().save(self.path)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)
        self.path.chmod(0o640)
        Article().save(self.path)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o640)

    def test_entry_points(self):
        root = Path(__file__).resolve().parents[1]
        for relative in ("part_1/string_var.py", "part_1/point.py", "part_1/warrior.py",
                         "part_1/arena.py", "part_2/model.py"):
            with self.subTest(script=relative):
                result = subprocess.run(
                    [sys.executable, "-B", str(root / "module_5" / relative)],
                    input="нет\nнет\n", capture_output=True, text=True,
                    encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                    cwd=self.temp.name, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
