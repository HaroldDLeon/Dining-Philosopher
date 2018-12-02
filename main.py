import random
import threading
import time


class ChopsticksCheck(threading.Thread):
    def run(self):
        while True:
            chopstick_list = [fork.id for fork in chopsticks if not fork.is_free()]
            time.sleep(1.5)
            print(f'Chopsticks being used are {chopstick_list}')


class Philosopher(threading.Thread):

    def __init__(self, idx):
        super(Philosopher, self).__init__()
        if idx is None:
            idx = random.randrange(1, 10)
        self.idx = idx

        self.eating: bool = False
        self.has_eaten: int = 0
        self.hungry_threshold = 10
        self.thinking_threshold = 5

        self.hungriness = 0
        self.thinking = False

        self.left_chopstick: Chopstick = None
        self.right_chopstick: Chopstick = None

    def __str__(self):
        hungry: bool = self.hungriness <= self.thinking_threshold
        if hungry:
            return f'Added Philosopher {self.idx} is hungry. '
        else:
            return f'Added Philosopher {self.idx} is still thinking. '

    def try_to_eat(self):
        left_chopstick = chopsticks[(self.idx - 1) % 5]
        right_chopstick = chopsticks[self.idx % 5]

        if left_chopstick.is_free() and right_chopstick.is_free():
            print(f'Philosopher {self.idx} got hungry and is taking the chopsticks. ')

            self.left_chopstick = left_chopstick
            self.right_chopstick = right_chopstick

            self.left_chopstick.assign_philosopher()
            self.right_chopstick.assign_philosopher()

            self.eat()
            time.sleep(10)
            self.release_chopsticks()

    def release_chopsticks(self):
        print(f'Philosopher {self.idx} is putting down the chopsticks')
        self.left_chopstick.release()
        self.right_chopstick.release()

        self.left_chopstick = None
        self.right_chopstick = None

    def is_eating(self):
        return self.eating

    def eat(self):
        self.eating = True
        self.has_eaten += 1
        self.hungriness = 0

    def consult_stomach(self):
        print(f'Philosopher {self.idx} has eaten {self.has_eaten} time(s).')

    def print_status(self):
        hungry: bool = self.hungriness >= self.thinking_threshold
        if not hungry or self.eating:
            print(f'Philosopher {self.idx} is currently thinking. ')
        else:
            print(f'Philosopher {self.idx} is hungry. ')

    def run(self):
        while True:
            self.print_status()
            if self.thinking_threshold <= self.hungriness <= self.hungry_threshold:
                self.try_to_eat()
            else:
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
            return f'Chopstick #{self.id} status is hold. '
        return f'Chopstick #{self.id} status is free. '

    def is_free(self):
        return not self.is_held

    def assign_philosopher(self):
        self.is_held = True

    def release(self):
        self.is_held = False


if __name__ == '__main__':
    global philosophers
    global chopsticks

    philosophers = (Philosopher(0), Philosopher(1), Philosopher(2), Philosopher(3), Philosopher(4))
    chopsticks = (Chopstick(0), Chopstick(1), Chopstick(2), Chopstick(3), Chopstick(4))

    print("Program started")

    check = ChopsticksCheck()
    # check.start()

    for person in philosophers:
        print("Starting philosopher Threads. ")
        person.start()
