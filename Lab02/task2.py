"""
    Basic thread handling exercise:

    Use the Thread class to create and run more than 10 threads which print their name and a random
    number they receive as argument. The number of threads must be received from the command line.

    e.g. Hello, I'm Thread-96 and I received the number 42

"""
import sys
import random
import threading
import time

RANDOM_MIN = 0
RANDOM_MAX = 1000


def print_thread(number):
    print(f"[Thread {threading.currentThread().getName()}] Received number {number}")


def main():
    if len(sys.argv) < 2:
        print(f"Insufficient number of arguments! Usage: {sys.argv[0]} num_threads")
        sys.exit()

    random.seed(time.time())

    num_threads = int(sys.argv[1])
    threads = [threading.Thread(target=print_thread, args=(random.randint(RANDOM_MIN, RANDOM_MAX),))
               for _ in range(num_threads)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
