from threading import Thread, Lock
import time
import csv
import psutil

def get_metric(point, named, lock: Lock):   #используем одну функция для 2-х метрик, т.к. меняется лишь один аргумент
    print(point)
    now_time = (time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time())))
    points = [now_time, point, named]
    with open('base.csv', 'a') as file:     #добавляем массив значений в файл каждую минуту
        writer = csv.writer(file)
        writer.writerow(points)

#n = int(input("minutes: "))
n = 5
for i in range(0, n):
    lock = Lock()                           #за 60 сек один поток успеет дождаться другой, но с куда меньшим временем это не работало, поэтому делаем лок
    t1 = Thread(target=get_metric, args=(psutil.cpu_freq().current,'CPU frequency', lock,), daemon=True)
    t2 = Thread(target=get_metric, args=(round((psutil.virtual_memory().used)/8388608, 2),'RAM using (MB)', lock,), daemon=True)
    t1.start()
    t2.start()
    if i != n:                              #если постать слип тут, то всё будет секнда в секунду
        time.sleep(60)
t1.join()
t2.join()