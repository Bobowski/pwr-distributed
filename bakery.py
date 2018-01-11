from threading import Thread
from time import sleep
import random

NUM_THREADS = 10
Entering = [False for _ in range(NUM_THREADS)]
Number = [0 for _ in range(NUM_THREADS)]

resource = 0
def use_resource(uid):
    global resource
    if resource != 0:
        print("Resource is in use but", uid, " aquires it")

    resource = uid
    print("[", uid, "] using resource")
    sleep(random.random())
    resource = 0

class MyThread(Thread):
    def __init__(self, i):
        Thread.__init__(self)
        self.i = i

    def lock(self):
        i = self.i

        # Get number
        Entering[i] = True
        Number[i] = max(Number) + 1
        Entering[i] = False

        for j in range(NUM_THREADS):
            while Entering[j]:
                pass

            while Number[j] != 0 and (Number[j] < Number[i] or (Number[j] == Number[i] and j < i)):
                pass

    def unlock(self):
        Number[self.i] = 0

    def run(self):
        while True:
            self.lock()
            use_resource(self.i)
            self.unlock()


if __name__ == "__main__":
    threads = [MyThread(i) for i in range(NUM_THREADS)]
    for t in threads:
        t.start()
