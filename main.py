import random
import threading
import time
from Lib import queue

"""
  Check systems:
      - Check on level of hungriness
      - Waiter-like object.
"""


class Philosopher(threading.Thread):

    def __init__(self, idx):
        super(Philosopher, self).__init__()
        if idx is None:
            idx = random.randrange(1, 10)
        self.idx = idx

        self.eating: bool = False

        self.hungry_threshold = 10
        self.thinking_threshold = 5

        self.hungriness = 0
        self.thinking = False

    def __str__(self):
        hungry: bool = self.hungriness <= self.thinking_threshold
        if hungry and self in waiter.array:
            return f'Philosopher {self.idx} is currently hungry and in waiting list'
        elif hungry:
            return f'Added Philosopher {self.idx} is hungry.'
        else:
            return f'Added Philosopher {self.idx} is still thinking'

    def pick_chopstick(self):
        pass

    def try_to_eat(self):
        pass

    def is_eating(self):
        return self.eating

    def get_status(self):  # check_philosopher
        hungry: bool = self.hungriness >= self.thinking_threshold
        if not hungry:
            print(f'Philosopher {self.idx} is currently thinking')
        elif hungry and self not in waiter.array:
            waiter.add(self)
            print(f'Added Philosopher {self.idx} to the waiting queue')
        else:
            print(f'Philosopher {self.idx} is hungry and currently on waiting queue')

    def run(self):
        while True:
            self.get_status()
            if self.hungriness <= 10:
                self.hungriness += 1
            time.sleep(3)


class Chopstick:
    def __init__(self, idx=None):
        if idx is None:
            idx = random.randrange(1, 10)
        self.id = idx
        self.is_held: bool = False
        self.held_by: Philosopher = None

    def __str__(self):
        if self.is_held:
            return f'Chopstick #{self.id} status is hold.'
        return f'Chopstick #{self.id} status is free.'

    def is_free(self):
        return self.is_held

    def assign_philosopher(self, philosopher: Philosopher = None):
        self.is_held = True
        self.held_by = philosopher


class Waiter(threading.Thread):
    def __init__(self):
        super(Waiter, self).__init__()
        self.queue = queue.Queue()
        self.array = []

    def add(self, item: object):
        if item not in self.array:
            self.queue.put(item)
            self.array.append(item)

    def get_chopsticks(phil: Philosopher):

        return

    def serve(self):
        phil: Philosopher = self.queue.pop()

        left_chopstick = chopsticks[(phil.idx - 1) % 5]
        right_chopstick = chopsticks[phil.idx % 5]

        if left_chopstick.is_free() and right_chopstick.is_free():
            left_chopstick.assign_philosopher(phil)
            right_chopstick.assign_philosopher(phil)
        self.array.remove(phil)


class CustomThread(threading.Thread):
    def run(self):
        print(f'{self.getName()} started!')
        while True:
            time.sleep(random.randrange(1, 5))
            print("---------------------------------")


if __name__ == '__main__':
    global philosophers
    global chopsticks
    global waiter

    philosophers = (Philosopher(0), Philosopher(1), Philosopher(2), Philosopher(3), Philosopher(4))
    chopstick: Chopstick = (Chopstick(0), Chopstick(1), Chopstick(2), Chopstick(3), Chopstick(4))

    waiter = Waiter()
    waiter.start()

    print("Program started")

    for person in philosophers:
        print("Starting philosopher Threads")
        person.start()
