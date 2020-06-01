from agent.imports import *


def OpenApp(PATH,APPNAME): #APPName with extention
    x = (PATH + "\\" + APPNAME)
    raw_string = r"{}".format(x)
    subprocess.Popen(raw_string)


def IsRunning(ProgramName): #program name without extention
    if win32gui.FindWindow(None, ProgramName):
        return True
    else:
        return False


def IsOpen(PATH, APPNAME,APPWINDOW): # APPNAME=APPNAME.exe   APPWINDOW=APPNAME without ext.
    OpenApp(PATH,APPNAME)
    x = IsRunning(APPWINDOW)
    while x != True:
        print("waiting")
        time.sleep(1)
        x = IsRunning(APPWINDOW)
    print("your app is ready")


def Undo():
    pyautogui.hotkey('ctrl', 'z')


def Redo():
    pyautogui.hotkey('ctrl', 'y')


def Cut():
    pyautogui.hotkey('ctrl','x')


def Copy():
    pyautogui.hotkey('ctrl', 'c')


def MarkAll():
    pyautogui.hotkey('ctrl', 'a')


def Paste():
    pyautogui.hotkey('ctrl','v')


def Save():
    pyautogui.hotkey('ctrl','s')


def Print():
    pyautogui.hotkey('ctrl','p')


def Find():
    pyautogui.hotkey('ctrl','f')


def Close():
    pyautogui.hotkey('alt','f4')


def ScreenShot():
    im = ImageGrab.grab()

    return im


def Highlight(x1,y1,x,y):
    pyautogui.click(x1,y1)
    pyautogui.drag(x, y, button='left')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)
    print(pyperclip.paste())


# IsOpen("C:\Program Files (x86)\Google\Chrome\Application", "chrome.exe", "Google Chrome (2)")



