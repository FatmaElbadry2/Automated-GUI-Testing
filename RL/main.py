#from imports import MY_DIRNAME
import time
from yoloInterface import *
from YOLOv3_PyTorch.test import *
from detect import *

from InrefaceAgent import keyboard as k, mouse, shortcuts as sh
print("starting")
# c = wmi.WMI()
#
# process_watcher = c.Win32_Process.watch_for("operation")
# sh.OpenApp("C:\\Program Files\\Apprentice Video", "apprenticevideo.exe")
# executable = ""
# caption = ""
# i = 0
# PID = -1
# user32 = ctypes.windll.user32
# while str(executable) != "C:\\Program Files\\Apprentice Video\\apprenticevideo.exe":
#     new_process = process_watcher()
#     PID = new_process.ProcessId
#     caption = new_process.Caption
#     executable = new_process.ExecutablePath
# print("opened")
# print(PID)
# current_pid = -1
# while PID != current_pid:
#     h_wnd = user32.GetForegroundWindow()
#     pid = wintypes.DWORD()
#     user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
#     current_pid = pid.value
#     print(pid.value)
# print("window is now in the foreground")

sh.open_app_foreground("C:\\Program Files\\Apprentice Video", "apprenticevideo.exe")
time.sleep(2)
sh.max()
time.sleep(1)

image = save_image()


print(image.shape)

time.sleep(1)
# for i in range(len(elements)):

