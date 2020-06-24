from InrefaceAgent.imports import *
import psutil

def OpenDir(PATH):
    webbrowser.open(PATH)

def open_app_foreground(path, name):
    # c = wmi.WMI()
    #process_watcher = c.Win32_Process.watch_for()
    PID = OpenApp(path, name)
    caption = ""
    executable = ""
    # PID = -1
    user32 = ctypes.windll.user32
    # while str(executable) != path+"\\"+name:
    #     new_process = process_watcher()
    #     PID = new_process.ProcessId
    #     executable = new_process.ExecutablePath
    #     caption = new_process.Caption
    print("opened")
    print(PID)
    current_pid = -1
    while PID != current_pid:
        h_wnd = user32.GetForegroundWindow()
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
        current_pid = pid.value
    print(current_pid)
    print("window is now in the foreground")
    return current_pid


def OpenApp(PATH,APPNAME): #APPName with extention
    x = (PATH + "\\" + APPNAME)
    raw_string = r"{}".format(x)
    process = subprocess.Popen(raw_string)
    return process.pid

def IsTerminated(pid):
    if psutil.pid_exists(pid):
        return False
    return True



# def IsRunning(ProgramName): #program name without extention
#    if win32gui.FindWindow(None, ProgramName):
#       return True
#    else:
#       return False
#
#
# def IsOpen(PATH, APPNAME,APPWINDOW): #APPNAME=APPNAME.exe   APPWINDOW=APPNAME without ext.
#     OpenApp(PATH,APPNAME)
#     x=IsRunning(APPWINDOW)
#     print(x)
#     while(x!=True):
#         print("waiting")
#         time.sleep(1)
#         x = IsRunning(APPWINDOW)
#
#
# def IsRunning2(ProgramName): #program name with extention
#     c = wmi.WMI()
#     for process in c.Win32_Process():
#         if(ProgramName==process.Name):
#             return True
#     return False
#

# def IsOpen2(PATH, APPNAME): #APPNAME=APPNAME.exe
#     OpenApp(PATH,APPNAME)
#     x=IsRunning2(APPNAME)
#     while(x!=True):
#         print("waiting")
#         time.sleep(1)
#         x = IsRunning2(APPNAME)



def Cut():
    pyautogui.hotkey('ctrl','x')


def Copy():
    pyautogui.hotkey('ctrl', 'c')


def Paste():
    pyautogui.hotkey('ctrl','v')


def Save():
    pyautogui.hotkey('ctrl','s')


def Print():
    pyautogui.hotkey('ctrl','p')


def Find():
    pyautogui.hotkey('ctrl','f')

    
def MarkAll():
    pyautogui.hotkey('ctrl','a')


def Close():
    pyautogui.hotkey('alt','f4')


def max():
    pyautogui.hotkey('win', 'up')


def ScreenShot():
    im = ImageGrab.grab()
    return im


def Highlight(x1,y1,x,y):
    pyautogui.click(x1,y1)
    pyautogui.drag(x, y, button='left')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)
    print(pyperclip.paste())


def Delete():
    pyautogui.press('backspace')

