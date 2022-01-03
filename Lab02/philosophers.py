import sys
from threading import Thread, Lock
import time


class Philosopher(Thread):
    """Implements a philosopher"""

    def __init__(self, philosopher_id, left_fork, right_fork):
        Thread.__init__(self)
        self.philosopher_id = philosopher_id
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while True:
            with self.left_fork:
                time.sleep(0.1)
                result = self.right_fork.acquire(False)

                if result:
                    break

            self.left_fork, self.right_fork = self.right_fork, self.left_fork

        print(f"Philosopher {self.philosopher_id} is eating")

        self.right_fork.release()


def main():
    if len(sys.argv) < 2:
        print(f"Insufficient number of arguments! Usage: {sys.argv[0]} num_philosophers")
        sys.exit()

    num_philosophers = int(sys.argv[1])

    forks = [Lock() for _ in range(num_philosophers)]
    philosophers = [Philosopher(i, forks[i - 1], forks[i]) for i in range(num_philosophers)]

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()


if __name__ == "__main__":
    main()
