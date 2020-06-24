#from imports import MY_DIRNAME

from tree import *
import tree as t
from RNInterface import *

from Utils import *

from InrefaceAgent import keyboard as k, mouse, shortcuts as sh

from win32api import GetSystemMetrics

action_space = np.empty(2901)
action_space.fill(-1)
action_count=np.zeros(2901)
tree = []
img_states = {}
states = {}
if __name__ == "__main__":

    print("starting")
    pid = sh.open_app_foreground("C:\\Program Files\\Elmer 8.4-Release\\bin", "ElmerGUI.exe")
    #sh.OpenApp("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
    time.sleep(2)
    sh.max()
    time.sleep(1)

    Width = GetSystemMetrics(0)
    Height = GetSystemMetrics(1)

    for i in range(4):

        '''image, path = save_image(i)

        elements = buildElements(path,i,[Width,Height])

        print(Width, Height)

        mouse.LeftClick(elements[-4].x_center,elements[-4].y_center)
        if img_exists(elements, image):
            print("state already exists")
            # give negative reward
        else:
            states[path] = elements
        tree,IDs = buildTree(elements)
        print("length of tree: ",len(tree))
        time.sleep(1)'''

        state, path = GetState(i,img_states,states,tree,action_space)
        print(tree)
        print(img_states)
        print(states)
        print(action_space[action_space != -1])








    # for i in range(len(elements)):

