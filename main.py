import random
import threading
import time

g



class Chopstick:
    def __init__(self, number=None):
        if number is None:
            number = random.randrange(1, 10)
        self.id = number
        self.is_hold = False
        self.held_by = None

    def __str__(self):
        if self.is_hold:
            return f'Chopstick #{self.id} status is hold.'
        return f'Chopstick #{self.id} status is free.'

    def get_status(self):
        return self.is_hold


class Philosopher:
    def __init__(self):
        pass

    def __str__(self):
        return True


class CustomThread(threading.Thread):
    def run(self):
        print(f'{self.getName()} started!')  # "Thread-x started!"
        time.sleep(1)  # Pretend to work for a second
        print(f'{self.getName()}finished')  # "Thread-x finished!"


if __name__ == '__main__':
    for x in range(4):  # Four times...
        my_thread = CustomThread(name="Thread-{}".format(x + 1))  # ...Instantiate a thread and pass a unique ID to it
        my_thread.start()  # ...Start the thread
        time.sleep(.9)  # ...Wait 0.9 seconds before starting another
