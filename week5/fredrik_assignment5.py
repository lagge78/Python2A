import ssl
import time
import threading
from urllib.request import urlopen, Request
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# Header with user agent is needed to allow access for scraping
HEADER = {"User-Agent": "Mozilla/5.0"}
URLS = [
    "https://consid.se/",
    "https://stackoverflow.com/",
    "https://9gag.com/",
    "https://www.yahoo.com",
    "https://www.reddit.com",
    "https://www.youtube.com",
    "https://9gag.com/",
    "https://consid.se/",
    "https://www.reddit.com",
    "https://www.youtube.com",
    "https://stackoverflow.com",
    "https://www.aftonbladet.se/",
    "https://www.yahoo.com",
    "https://consid.se/",
    "https://www.youtube.com",
    "https://9gag.com/",
    "https://stackoverflow.com/",
    "https://www.yahoo.com",
    "https://www.reddit.com/",
    "https://consid.se/",
    "https://9gag.com/",
    "https://stackoverflow.com/",
    "https://www.aftonbladet.se/",
    "https://www.yahoo.com",
    "https://www.reddit.com",
    "https://www.youtube.com",
    "https://9gag.com/",
    "https://consid.se/",
    "https://stackoverflow.com/",
    "https://www.aftonbladet.se/"
]


def timer(func):
    def timer_wrapper(*args):
        start = time.time()
        func(*args)
        end = time.time()
        exec_time = end - start
        print(f"Execution time: {(exec_time):.7f} seconds ({func.__name__})")
        return exec_time

    return timer_wrapper


def request_and_open(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    request = Request(url, headers=HEADER)
    url_info_byte = urlopen(request, timeout=20, context=ctx).read()
    url_info_string = url_info_byte.decode("utf-8")

    return url_info_string


@timer
def request_single():
    for url in URLS:
        request_and_open(url)


@timer
def request_pool(num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(request_and_open, URLS)


@timer
def request_queue(num_threads):
    def worker(queue):
        while True:
            url = queue.get()
            if url is None:
                break
            request_and_open(url)
            queue.task_done()

    queue = Queue()
    threads = []

    for url in URLS:
        queue.put(url)

    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)

    queue.join()

    for _ in range(num_threads):
        queue.put(None)

    for thread in threads:
        thread.join()


def main():
    num_threads = [2, 4, 8, 16, 32, 64]
    num_iterations = 8
    mean_times_pool = []
    mean_times_queue = []

    print(f"Number of threads: 1. Executing...")
    total_time_single = sum(request_single() for _ in range(num_iterations))
    mean_time_single = total_time_single / num_iterations

    for i in num_threads:
        print(f"Number of threads: {i}. Executing...")
        total_time_pool = sum(request_pool(i) for _ in range(num_iterations))
        total_time_queue = sum(request_queue(i) for _ in range(num_iterations))
        mean_times_pool.append(total_time_pool / num_iterations)
        mean_times_queue.append(total_time_queue / num_iterations)

    print(f"The mean time using single thread: {mean_time_single}")
    print(f"The mean times using thread pool executor are: {mean_times_pool}")
    print(f"The mean times using queue.Queue workers are: {mean_times_queue}")


if __name__ == "__main__":
    main()
