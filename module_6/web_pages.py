import time
from concurrent.futures import ThreadPoolExecutor

import requests


LINKS = [
    "https://www.python.org/",
    "https://www.python.org/about/",
    "https://www.python.org/downloads/",
    "https://www.python.org/doc/",
    "https://www.python.org/community/",
]


def get_html(link):
    """Получить текст страницы или сообщить об ошибке HTTP/соединения."""
    with requests.get(link, timeout=20) as response:
        response.raise_for_status()
        return response.text


def main():
    start = time.perf_counter()
    sequential_pages = [get_html(link) for link in LINKS]
    sequential = time.perf_counter() - start

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as pool:
        parallel_pages = list(pool.map(get_html, LINKS))
    parallel = time.perf_counter() - start

    for link, first, second in zip(LINKS, sequential_pages, parallel_pages):
        print(f"{link} - символов последовательно/параллельно: "
              f"{len(first)}/{len(second)}")
    print(f"Последовательно: {sequential:.3f} с")
    print(f"Параллельно: {parallel:.3f} с")


if __name__ == "__main__":
    main()
