import pyautogui
import pyscreenshot as ImageGrab
import pyperclip  # handy cross-platform clipboard text handler
import time
import subprocess

def OpenApp(PATH,APPNAME):

    subprocess.Popen([PATH+'\\'+APPNAME, '-nc'])

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




