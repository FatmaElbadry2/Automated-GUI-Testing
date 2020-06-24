
import threading, queue

'''def func1(num, q):
    while num < 100000000:
        num =  num**2
        q.put(num)

def func2(num, q):
    while num < 100000000:
        num = q.get()
        print (num)

num = 2
q = queue.Queue()
thread1 = threading.Thread(target=func1,args=(num,q))

#thread2 = threading.Thread(target=func2,args=(num,q))
print ('setup')
thread1.start()
#thread2.start()
func2(num, q)'''

q = queue.Queue()
q.put(2)

q.put(3)
q.put(4)
print(q.queue[-1])
q.queue.clear()
print(q.empty())
print(q.queue[-1])