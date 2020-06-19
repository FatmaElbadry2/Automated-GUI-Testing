from InrefaceAgent import mouse, keyboard as k, Element_to_Action as eta, shortcuts as sh
from global_imports import *
from RL.imports import *
from tree import *
from RNInterface import *


def OpenApp(app_path, app_name):
    print("starting")
    sh.open_app_foreground(app_path, app_name)
    # sh.OpenApp("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
    time.sleep(2)
    sh.max()
    time.sleep(1)

def GetState(i):
    state = np.zeros(250)
    #state = []
    time.sleep(1)
    image, path = save_image(i)
    elements = buildElements(path, i, [Width, Height])
    if img_exists(elements, image):
        print("state already exists")
        img_states[path][0] += 1
    else:
        img_states[path] = [1, elements]
        states[path]=[]
        tree,IDs = buildTree(elements)

        for id in IDs:
            available_actions = np.where(np.array(action_space) == id)[0]
            if len(available_actions) > 0:
                [states[path].append(action_id) for action_id in available_actions]
    state[0:min(len(state), len(states[path]))] = states[path][0:min(len(state), len(states[path]))]
    #state = states[path]
    print(state)
    print(len(state))
    return state, path

def SetReward(state, action, path, new_actions):
    if action in state and action != 0:
        state_occurences = img_states[path][0]
        reward = (1/state_occurences) * new_actions
    else:
        reward = -1
    return reward

def GetNewActions(state, next_state):
    #print("STATE: ", state)
    #print("NEXT STATE: ", next_state)
    new_actions = list(set(next_state) - set(state[0]))
    return len(new_actions)


def ElementMapper(idx_element):
    print("Element ID INT: ",int(idx_element))
    print(tree)
    element = tree[int(idx_element)]
    return element.x_center, element.y_center