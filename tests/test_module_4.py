import subprocess
import sys
import unittest
from pathlib import Path

from module_4.binary_search import binary_search
from module_4.insertion_sort import insertion_sort
from module_4.breadth_first_search import (
    breadth_first_search,
    breadth_first_search_details,
    shortest_path,
)


class BinarySearchTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(binary_search([], 1), -1)

    def test_single_found(self):
        self.assertEqual(binary_search([7], 7), 0)

    def test_single_missing(self):
        self.assertEqual(binary_search([7], 8), -1)

    def test_edges(self):
        for target, index in [(2, 0), (11, 3)]:
            with self.subTest(target=target):
                self.assertEqual(binary_search([2, 4, 7, 11], target), index)

    def test_missing(self):
        for target in [0, 5, 20]:
            with self.subTest(target=target):
                self.assertEqual(binary_search([2, 4, 7, 11], target), -1)

    def test_duplicates(self):
        values = [1, 2, 2, 2, 3]
        index = binary_search(values, 2)
        self.assertIn(index, [1, 2, 3])
        self.assertEqual(values[index], 2)

    def test_million_elements(self):
        values = range(1_000_000)
        self.assertEqual(binary_search(values, 999_999), 999_999)
        self.assertEqual(binary_search(values, 1_000_000), -1)


class Item:
    def __init__(self, value, label):
        self.value = value
        self.label = label

    def __gt__(self, other):
        return self.value > other.value


class InsertionSortTests(unittest.TestCase):
    def check_sort(self, values):
        original = values
        expected = sorted(values)
        result = insertion_sort(values)
        self.assertIsNone(result)
        self.assertIs(values, original)
        self.assertEqual(original, expected)

    def test_empty(self):
        self.check_sort([])

    def test_single(self):
        self.check_sort([5])

    def test_sorted(self):
        self.check_sort([1, 2, 3, 4])

    def test_reverse(self):
        self.check_sort([4, 3, 2, 1])

    def test_negative_and_duplicates(self):
        self.check_sort([5, -2, 5, 0, -2])

    def test_stability(self):
        values = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
        insertion_sort(values)
        self.assertEqual([item.label for item in values], ["b", "d", "a", "c"])


class BreadthFirstSearchTests(unittest.TestCase):
    def setUp(self):
        self.graph = {"A": ["B", "C"], "B": ["D"], "C": ["A", "D"], "D": []}

    def test_example_order(self):
        self.assertEqual(breadth_first_search(self.graph, "A"), ["A", "B", "C", "D"])

    def test_distances(self):
        _, distances, predecessors = breadth_first_search_details(self.graph, "A")
        self.assertEqual(distances, {"A": 0, "B": 1, "C": 1, "D": 2})
        self.assertEqual(predecessors, {"B": "A", "C": "A", "D": "B"})

    def test_shortest_path(self):
        self.assertEqual(shortest_path(self.graph, "A", "D"), ["A", "B", "D"])

    def test_single_vertex(self):
        self.assertEqual(breadth_first_search({"A": []}, "A"), ["A"])

    def test_start_is_target(self):
        self.assertEqual(shortest_path(self.graph, "A", "A"), ["A"])

    def test_self_loop(self):
        self.assertEqual(breadth_first_search({"A": ["A"]}, "A"), ["A"])

    def test_cycle_and_repeated_edges(self):
        self.assertEqual(breadth_first_search({"A": ["B", "B"], "B": ["A"]}, "A"), ["A", "B"])

    def test_disconnected_target(self):
        self.assertIsNone(shortest_path({"A": [], "B": []}, "A", "B"))

    def test_unknown_target(self):
        self.assertIsNone(shortest_path(self.graph, "A", "missing"))

    def test_neighbor_only_vertex(self):
        self.assertEqual(shortest_path({"A": ["B"]}, "A", "B"), ["A", "B"])
        self.assertEqual(breadth_first_search({"A": ["B"]}, "B"), ["B"])

    def test_unknown_start(self):
        for graph in [{}, self.graph]:
            with self.subTest(graph=graph):
                with self.assertRaises(ValueError):
                    breadth_first_search(graph, "missing")

    def test_none_vertex(self):
        self.assertEqual(shortest_path({None: ["B"]}, None, "B"), [None, "B"])

    def test_graph_not_modified(self):
        original = {vertex: neighbors.copy() for vertex, neighbors in self.graph.items()}
        breadth_first_search_details(self.graph, "A")
        self.assertEqual(self.graph, original)


class ProgramExamplesTests(unittest.TestCase):
    def test_scripts(self):
        root = Path(__file__).resolve().parents[1]
        expected = {
            "binary_search.py": "3",
            "insertion_sort.py": "[-2, 1, 5, 5]",
            "breadth_first_search.py": (
                "['A', 'B', 'C', 'D']\n"
                "{'A': 0, 'B': 1, 'C': 1, 'D': 2}\n"
                "['A', 'B', 'D']"
            ),
        }
        for filename, output in expected.items():
            with self.subTest(filename=filename):
                result = subprocess.run(
                    [sys.executable, "-B", str(root / "module_4" / filename)],
                    cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=5,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(result.stdout.strip(), output)


if __name__ == "__main__":
    unittest.main()
