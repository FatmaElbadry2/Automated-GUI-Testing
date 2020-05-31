from agent.imports import *


def LeftClick(x,y):
    pyautogui.click(x,y)


def Rightclick(x,y):
    pyautogui.click(x,y,button='right')


def DoubleRightClick(x,y):
    pyautogui.click(x,y,clicks=2,button='right')


def DoubleLeftClick(x, y):
    pyautogui.click(x, y, clicks=2)


def ClickeithInterval(x,y,button,interval):
    pyautogui.click(x, y, clicks=2, button=button,interval=interval)


def scroll(clicks): #positive-> scroll up
    pyautogui.scroll(clicks)


def RelativeDrag(x,y): # (x,y,button)  x+ ->right y+->down
    pyautogui.drag(x, y, button='left')


def Drag(x,y):
    pyautogui.dragTo(x,y, button='left')


def clicks(x,y,numbersofclicks,button):
    pyautogui.click(x, y, clicks=numbersofclicks, button=button)

