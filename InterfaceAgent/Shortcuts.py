import pyautogui
import pyscreenshot as ImageGrab
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


