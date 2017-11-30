#!/usr/bin/env python
import Queue
import random
import threading
import time

def main_thread():
    queue = Queue.Queue()
    thread = threading.Thread(target=run_in_other_thread,args=(queue,))
    thread.daemon = True  # so you can quit the demo program easily :)
    thread.start()
    while True:
        val = queue.get()
        print "from main-thread", val

def run_in_other_thread(queue):
    while True:
        queue.put(random.random())
        time.sleep(1)

if __name__ == '__main__':
    main_thread()
