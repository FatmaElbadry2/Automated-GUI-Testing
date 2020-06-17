#from imports import MY_DIRNAME

from tree import *
from RNInterface import *


from InrefaceAgent import keyboard as k, mouse, shortcuts as sh

from win32api import GetSystemMetrics


if __name__ == "__main__":

    print("starting")
    sh.open_app_foreground("C:\\Program Files\\Elmer 8.4-Release\\bin", "ElmerGUI.exe")
    #sh.OpenApp("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
    time.sleep(2)
    sh.max()
    time.sleep(1)


    for i in range(1):
        Width = GetSystemMetrics(0)
        Height = GetSystemMetrics(1)
        image, path = save_image(i)

        elements = buildElements(path,i,[Width,Height])

        print(Width, Height)

        mouse.LeftClick(elements[-4].x_center,elements[-4].y_center)
        if state_exists(elements, image):
            print("state already exists")
            # give negative reward
        else:
            states[path] = elements
            buildTree(elements)
        print("length of tree: ",len(tree))
        time.sleep(1)






    # for i in range(len(elements)):

