import os
import time

data__ = "data1"
def child():
    while True:
        data__ = "child"
        time.sleep(5)
def parent():
    while True:
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d\n" % pids)


parent()