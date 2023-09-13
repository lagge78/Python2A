import sys
import time

FILENAME = "eng_vocab.txt"

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds ({func.__name__})")
        return result
    return wrapper

class ContextManager:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        try:
            self.file = open(self.filename, "r")
            return self.file
        except FileNotFoundError:
            print("File not found")
            exit()

    def __exit__(self, type, value, traceback):
        if self.file:
            self.file.close()

def my_generator(filename):
    with ContextManager(filename) as file:
        yield file

@timer_decorator
def read_generator(filename):
    total_bytes = 0
    for line in my_generator(filename):
        total_bytes += sys.getsizeof(line)
    print(f"{total_bytes} Bytes are used by the generator")


@timer_decorator
def read_list(filename):
    with ContextManager(filename) as file:
        text_list = file.read().splitlines()
        total_bytes = sys.getsizeof(text_list)
        print(f"{total_bytes} Bytes are used by the list")

def main():
    try:
        read_list(FILENAME)
        read_generator(FILENAME)


    except Exception:
        print("Something is wrong")

if __name__ == "__main__":
    main()
