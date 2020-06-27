<<<<<<< HEAD:agent/keyBoard.py

from agent.imports import *
=======
from InrefaceAgent.imports import *
>>>>>>> master:InrefaceAgent/keyboard.py


def Write(Word):
    pyautogui.write(Word, interval=0.25)


def WriteLetters():
    pyautogui.write("abCD", interval=0.25)


def WriteNumbers():
    pyautogui.write(1234, interval=0.25)


def WriteSpecialCha():
    pyautogui.write('_', interval=0.25)


def TwoKeys(FirstKey,SecondKey):
    pyautogui.hotkey(FirstKey,SecondKey)


def KeyPress(Key):
    pyautogui.press(Key)


def ThreeKeys(FirstKey,SecondKey,ThirdKey):
    pyautogui.hotkey(FirstKey,SecondKey,ThirdKey)


<<<<<<< HEAD:agent/keyBoard.py
def pressArrow(Arrow,numberofpresses): # arrow can be left , right, up ,down
=======
def pressArrow(Arrow,numberofpresses):
>>>>>>> master:InrefaceAgent/keyboard.py
    pyautogui.press(Arrow, presses=numberofpresses)


