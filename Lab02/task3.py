"""
Coffee Factory: A multiple producer - multiple consumer approach

Generate a base class Coffee which knows only the coffee name
Create the Espresso, Americano and Cappuccino classes which inherit the base class knowing that
each coffee type has a predetermined size.
Each of these classes have a get message method

Create 3 additional classes as following:
    * Distributor - A shared space where the producers puts coffees and the consumers takes them
    * CoffeeFactory - An infinite loop, which always sends coffees to the distributor
    * User - Another infinite loop, which always takes coffees from the distributor

The scope of this exercise is to correctly use threads, classes and synchronization objects.
The size of the coffee (ex. small, medium, large) is chosen randomly everytime.
The coffee type is chosen randomly everytime.

Example of output:

Consumer 65 consumed espresso
Factory 7 produced a nice small espresso
Consumer 87 consumed cappuccino
Factory 9 produced an italian medium cappuccino
Consumer 90 consumed americano
Consumer 84 consumed espresso
Factory 8 produced a strong medium americano
Consumer 135 consumed cappuccino
Consumer 94 consumed americano
"""

import random
import sys
from threading import BoundedSemaphore, Semaphore, Thread
import time


class Coffee:
    """ Base class """

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_name(self):
        """ Returns the coffee name """
        return self.name

    def get_size(self):
        """ Returns the coffee size """
        return self.size


class Espresso(Coffee):
    """ Espresso implementation """

    def __init__(self, size):
        Coffee.__init__(self, "espresso", size)

    def get_message(self):
        """ Output message """
        return "nice {} {}".format(self.get_size(), self.get_name())


class Americano(Coffee):
    """ Espresso implementation """

    def __init__(self, size):
        Coffee.__init__(self, "americano", size)

    def get_message(self):
        """ Output message """
        return "strong {} {}".format(self.get_size(), self.get_name())


class Cappuccino(Coffee):
    """ Cappuccino implementation """

    def __init__(self, size):
        Coffee.__init__(self, "cappuccino", size)

    def get_message(self):
        """ Output message """
        return "italian {} {}".format(self.get_size(), self.get_name())


class Distributor:
    """Distributor - the buffer"""

    def __init__(self, buffer_size):
        self.mutex_prod = BoundedSemaphore(1)
        self.mutex_cons = BoundedSemaphore(1)

        self.empty = Semaphore(value=buffer_size)
        self.full = Semaphore(value=0)

        self.buffer = []

    def put(self, elem):
        self.empty.acquire()

        with self.mutex_prod:
            self.buffer.append(elem)

        self.full.release()

    def get(self):
        self.full.acquire()

        with self.mutex_cons:
            elem = self.buffer.pop()

        self.empty.release()

        return elem


class CoffeeFactory(Thread):
    """CoffeeFactory - the producer"""

    def __init__(self, factory_id, buff, sizes, coffees):
        Thread.__init__(self)
        self.factory_id = factory_id
        self.buff = buff
        self.sizes = sizes
        self.coffees = coffees

    def run(self):
        while True:
            coffee_type = random.choice(self.coffees)
            coffee_size = random.choice(self.sizes)

            coffee = coffee_type(coffee_size)
            print(f"Factory {self.factory_id} produced {coffee.get_message()}")

            self.buff.put(coffee)


class User(Thread):
    """User - the consumer"""

    def __init__(self, consumer_id, buff):
        Thread.__init__(self)
        self.consumer_id = consumer_id
        self.buff = buff

    def run(self):
        while True:
            coffee = self.buff.get()
            print(f"Consumer {self.consumer_id} consumed {coffee.get_message()}")


def main():
    if len(sys.argv) < 4:
        print(f"Insufficient number of arguments! Usage: {sys.argv[0]} "
              f"num_producers num_consumers buffer_size")
        sys.exit()

    num_producers = int(sys.argv[1])
    num_consumers = int(sys.argv[2])
    buffer_size = int(sys.argv[3])

    random.seed(time.time())

    coffees = [Espresso, Americano, Cappuccino]
    sizes = ["small", "medium", "large"]

    buff = Distributor(buffer_size)

    users = [User(i, buff) for i in range(num_consumers)]
    producers = [CoffeeFactory(i, buff, sizes, coffees) for i in range(num_producers)]

    for producer in producers:
        producer.start()

    for user in users:
        user.start()


if __name__ == '__main__':
    main()
