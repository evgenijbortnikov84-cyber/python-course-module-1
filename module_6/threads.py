import time
from threading import Thread


def get_thread(thread_name):
    time.sleep(1)
    print(thread_name)


def main():
    names = [f"Поток {number}" for number in range(1, 6)]
    start = time.perf_counter()
    for name in names:
        get_thread(name)
    sequential = time.perf_counter() - start

    start = time.perf_counter()
    threads = [Thread(target=get_thread, args=(name,)) for name in names]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    parallel = time.perf_counter() - start

    print(f"Последовательно: {sequential:.3f} с")
    print(f"Параллельно: {parallel:.3f} с")


if __name__ == "__main__":
    main()
