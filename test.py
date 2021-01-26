from queue import Queue
from threading import Thread
from time import sleep


def function(queue):
    seconds = 20

    while seconds > 0:
        seconds -= 1
        print(seconds)
        queue.put('eat ghost')
    queue.put('normal')


queue = Queue()
thread = Thread(target=function(queue))
thread.start()
print(queue.get())
