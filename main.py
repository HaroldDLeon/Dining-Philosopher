import random
import threading
import time


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
        self.left_chopstick: Chopstick = None
        self.right_chopstick: Chopstick = None

    def __str__(self):
        hungry: bool = self.hungriness <= self.thinking_threshold
        if hungry and self in waiter.array:
            return f'Philosopher {self.idx} is currently hungry and in waiting list. \n'
        elif hungry:
            return f'Added Philosopher {self.idx} is hungry. \n'
        else:
            return f'Added Philosopher {self.idx} is still thinking. \n'

    def pick_chopsticks(self, left_chopstick, right_chopstick):

        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

        self.left_chopstick.assign_philosopher(self)
        self.right_chopstick.assign_philosopher(self)

    def release_chopsticks(self):
        self.left_chopstick.release()
        self.right_chopstick.release()

        self.left_chopstick = None
        self.right_chopstick = None

        self.eating = False

    def is_eating(self):
        return self.eating

    def bye_hungry(self):
        self.eating = True
        self.hungriness = 0

    def get_status(self):
        hungry: bool = self.hungriness >= self.thinking_threshold
        if not hungry or self.eating:
            print(f'Philosopher {self.idx} is currently thinking. \n')
        elif hungry and self not in waiter.array:
            waiter.add(self)
            print(f'Added Philosopher {self.idx} to the waiting queue. \n')
        else:
            print(f'Philosopher {self.idx} is hungry and currently on waiting queue. \n')

    def run(self):
        while True:
            self.get_status()
            if self.eating:
                time.sleep(10)
                self.release_chopsticks()
            elif self.hungriness <= 10:
                self.hungriness += 1
            sleep_time = random.randrange(1, 5)
            time.sleep(sleep_time)


class Chopstick:
    def __init__(self, idx=None):
        if idx is None:
            idx = random.randrange(1, 10)
        self.id = idx
        self.is_held: bool = False
        self.held_by: Philosopher = None

    def __str__(self):
        if self.is_held:
            return f'Chopstick #{self.id} status is hold. \n'
        return f'Chopstick #{self.id} status is free. \n'

    def is_free(self):
        return not self.is_held

    def assign_philosopher(self, philosopher: Philosopher = None):
        self.is_held = True
        self.held_by = philosopher

    def release(self):
        self.is_held = False
        self.held_by = None


class Waiter(threading.Thread):
    def __init__(self):
        super(Waiter, self).__init__()
        self.array = []

    def add(self, item: object):
        if item not in self.array:
            self.array.append(item)

    def serve(self):
        if len(self.array) >= 1:
            phil: Philosopher = self.array[0]

            left_chopstick = chopsticks[(phil.idx - 1) % 5]
            right_chopstick = chopsticks[phil.idx % 5]

            print(f'Trying to serve philosopher {phil.idx}. \n')

            if left_chopstick.is_free() and right_chopstick.is_free():
                left_chopstick.is_held = True
                right_chopstick.is_held = True

                phil.pick_chopsticks(left_chopstick, right_chopstick)
                phil.bye_hungry()
                self.array.remove(phil)

                print(f'Waiter served Philosopher {phil.idx}. \n')

    def run(self):
        while True:
            print(f'Waiter running: {len(self.array)} Philosophers on queue. \n')
            time.sleep(3)
            self.serve()


if __name__ == '__main__':
    global philosophers
    global chopsticks
    global waiter

    philosophers = (Philosopher(0), Philosopher(1), Philosopher(2), Philosopher(3), Philosopher(4))
    chopsticks = (Chopstick(0), Chopstick(1), Chopstick(2), Chopstick(3), Chopstick(4))

    waiter = Waiter()
    waiter.start()

    print("Program started")

    for person in philosophers:
        print("Starting philosopher Threads. \n")
        person.start()
