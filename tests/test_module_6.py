import io
import threading
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

import requests
from module_6 import threads, web_pages


class ThreadTests(unittest.TestCase):
    def test_waits_one_second_and_prints_name(self):
        output = io.StringIO()
        with patch.object(threads.time, "sleep") as sleep, redirect_stdout(output):
            threads.get_thread("Первый")
        sleep.assert_called_once_with(1)
        self.assertEqual(output.getvalue(), "Первый\n")

    def test_five_sequential_calls_and_five_distinct_threads(self):
        calls = []
        barrier = threading.Barrier(5)
        main_thread = threading.current_thread()

        def worker(name):
            current = threading.current_thread()
            if current is not main_thread:
                barrier.wait(timeout=5)
            calls.append((name, current))

        with patch.object(threads, "get_thread", side_effect=worker), redirect_stdout(io.StringIO()):
            threads.main()
        expected = {f"Поток {i}" for i in range(1, 6)}
        sequential = [(name, thread) for name, thread in calls if thread is main_thread]
        parallel = [(name, thread) for name, thread in calls if thread is not main_thread]
        self.assertEqual([name for name, _ in sequential], [f"Поток {i}" for i in range(1, 6)])
        self.assertEqual({name for name, _ in parallel}, expected)
        self.assertEqual(len(parallel), 5)
        self.assertEqual(len({thread for _, thread in parallel}), 5)
        self.assertTrue(all(not thread.is_alive() for _, thread in parallel))


class WebPageTests(unittest.TestCase):
    def test_returns_text_checks_status_and_closes_response(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.text = "<html>Привет</html>"
        with patch.object(web_pages.requests, "get", return_value=response) as get:
            self.assertEqual(web_pages.get_html("https://example.test/a"), response.text)
        get.assert_called_once_with("https://example.test/a", timeout=20)
        response.raise_for_status.assert_called_once_with()
        response.__exit__.assert_called_once()

    def test_http_error_is_not_silenced(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.raise_for_status.side_effect = requests.HTTPError("404")
        with patch.object(web_pages.requests, "get", return_value=response):
            with self.assertRaises(requests.HTTPError):
                web_pages.get_html("https://example.test/missing")
        response.__exit__.assert_called_once()

    def test_connection_timeout_is_not_silenced(self):
        with patch.object(web_pages.requests, "get", side_effect=requests.Timeout("timeout")):
            with self.assertRaises(requests.Timeout):
                web_pages.get_html("https://example.test/slow")

    def test_five_urls_sequentially_and_in_five_workers(self):
        calls = []
        barrier = threading.Barrier(5)
        main_thread = threading.current_thread()

        def download(link):
            current = threading.current_thread()
            if current is not main_thread:
                barrier.wait(timeout=5)
            calls.append((link, current))
            return "<html>" + link + "</html>"

        output = io.StringIO()
        with patch.object(web_pages, "get_html", side_effect=download), redirect_stdout(output):
            web_pages.main()
        self.assertEqual(len(set(web_pages.LINKS)), 5)
        self.assertEqual([url for url, thread in calls if thread is main_thread], web_pages.LINKS)
        parallel = [(url, thread) for url, thread in calls if thread is not main_thread]
        self.assertCountEqual([url for url, _ in parallel], web_pages.LINKS)
        self.assertEqual(len({thread for _, thread in parallel}), 5)
        self.assertTrue(all(not thread.is_alive() for _, thread in parallel))
        for link in web_pages.LINKS:
            self.assertIn(link, output.getvalue())
        self.assertIn("Последовательно:", output.getvalue())
        self.assertIn("Параллельно:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
