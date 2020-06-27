import time, threading, _thread, signal

def long_running():
    while True:
        print('Hello')

def stopper(sec):
    time.sleep(sec)
    print('Exiting...')
    _thread.interrupt_main()
    return True





threading.Thread(target = stopper, args = (2, )).start()


try:
    long_running()
except KeyboardInterrupt:
    print("a5eeraaan")

