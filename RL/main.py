#from imports import MY_DIRNAME

from tree import *
from yoloInterface import *


from InrefaceAgent import keyboard as k, mouse, shortcuts as sh
print("starting")
sh.open_app_foreground("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
time.sleep(2)
sh.max()
time.sleep(1)


for i in range(3):
    image, path = save_image(i)
    elements = buildElements(image,i)
    if state_exists(elements, image):
        print("state already exists")
        # give negative reward
    else:
        states[path] = elements
        buildTree(elements)
    print("length of tree: ",len(tree))
    time.sleep(1)

# for i in range(len(elements)):

