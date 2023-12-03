from threading import Thread, Lock
import time
import csv
import psutil

def get_metric(named, n, lock: Lock):
    for i in range(0, n):
        now_time = (time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time())))
        if named == 'cpu':
            points = [now_time, psutil.cpu_freq().current, 'CPU frequency']
        if named == 'ram':
            points = [now_time, round((psutil.virtual_memory().used)/8388608, 2), 'RAM using (MB)']
        lock.acquire()
        with open('base.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(points)
        lock.release()
        if i != n - 1:
            time.sleep(60)

#n = int(input("minutes: "))
n = 5
lock = Lock()
t1 = Thread(target=get_metric, args=('cpu', n, lock,), daemon=True)
t2 = Thread(target=get_metric, args=('ram', n, lock,), daemon=True)
t1.start()
t2.start()
t1.join()
t2.join()
