import threading
import datetime

def worker():
    print('Worker')

thread = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()