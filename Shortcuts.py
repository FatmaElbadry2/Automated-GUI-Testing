import pyautogui
import pyscreenshot as ImageGrab
import pyperclip  # handy cross-platform clipboard text handler
import time
import subprocess
import win32gui

def OpenApp(PATH,APPNAME): #APPName with extention
    x = (PATH + "\\" + APPNAME)
    raw_string = r"{}".format(x)
    subprocess.Popen(raw_string)

def IsRunning(ProgramName): #program name without extention
   if win32gui.FindWindow(None, ProgramName):
      return True
   else:
      return False

def IsOpen(PATH, APPNAME,APPWINDOW): #APPNAME=APPNAME.exe   APPWINDOW=APPNAME without ext.
    OpenApp(PATH,APPNAME)
    x=IsRunning(APPWINDOW)
    while(x!=True):
        print("waiting")
        time.sleep(1)
        x = IsRunning(APPWINDOW)

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

def Close():
    pyautogui.hotkey('alt','f4')

def ScreenShot():
    im = ImageGrab.grab()

def Highlight(x1,y1,x,y):
    pyautogui.click(x1,y1)
    pyautogui.drag(x, y, button='left')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)
    print(pyperclip.paste())




