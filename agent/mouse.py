from imports import *


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


def RelativeDrag(x,y,Button): # (x,y,button)  x+ ->right y+->down
    pyautogui.drag(x, y, button=Button)


def Drag(x,y,button):
    pyautogui.dragTo(x,y, button=button)


def clicks(x,y,numbersofclicks,button):
    pyautogui.click(x, y, clicks=numbersofclicks, button=button)


LeftClick(200,300)