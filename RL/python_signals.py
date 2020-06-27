
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

# q = queue.Queue()
# q.put(2)
#
# q.put(3)
# q.put(4)
# print(q.queue[-1])
# q.queue.clear()
# print(q.empty())
# print(q.queue[-1])
'''import cv2 as cv
from PIL import ImageChops
import numpy as np
# PatternAuto (243).png
#PatternAuto (247).png
# images/image_0.png
img_1 = cv.imread('images/image_123.png')
img_2 = cv.imread('images/image_124.png')

img_1=cv.cvtColor(img_1, cv.COLOR_BGR2GRAY)
img_2=cv.cvtColor(img_2, cv.COLOR_BGR2GRAY)
# img_1=np.array([0,2,3])
# img_2=np.array([0,2,4])

img_3=np.zeros((img_1.shape[0],img_1.shape[1]))
img_3[img_1==img_2]=1
cv.imshow('image',img_3)
cv.waitKey(0)
diff = img_3[img_3==0].shape[0]
similar = img_3[img_3==1].shape[0]
print("difference: ",diff)
print("similar: ",similar)
print("ratio_similar: ",100*similar/(diff+similar))
print("ratio_diff: ",100*diff/(diff+similar))
print("diff to similar: ",100*diff/(similar))
'''
import sys
import numpy as np
unique_states={1:[['path_1','path_2'],[1,1]],2:[['path_1','path_2'],[1,0]]}

action = 3
path = 'path_3'
if action not in unique_states :
    unique_states[action]=[[],[]]
x=np.array(unique_states[action][0])
path_index = np.where(x==path)[0]
if len(path_index) ==0 :
    unique_states[action][0].append(path)
    unique_states[action][1].append(1)
else:
    unique_states[action][1][path_index[0]] += 1
print(unique_states)

