from InrefaceAgent import mouse, keyboard as k, Element_to_Action as eta, shortcuts as sh
from global_imports import *
from RL.imports import *
from tree import *
from RNInterface import *
import shutil


def OpenApp(app_path, app_name):
    print("starting")
    pid = sh.open_app_foreground(app_path, app_name)
    # sh.OpenApp("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
    time.sleep(2)
    sh.max()
    time.sleep(1)
    return pid

def GetState(i):
    state = np.zeros(250)
    print("ACTION COUNT: ", action_count)
    print("STATES: ", states)
    print("IMG STATES: ", states)
    #state = []
    time.sleep(1)
    image, path = save_image(i)
    elements = buildElements(path, i, [Width, Height])
    exists,old_state=img_exists(elements)
    if exists:
        print("state already exists")
        img_states[old_state][0] += 1
        state[0:min(len(state), len(states[old_state]))] = states[old_state][0:min(len(state), len(states[old_state]))]
        path = old_state
    else:
        img_states[path] = [1, elements]
        states[path]=[]
        IDs = buildTree(elements)

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
        reward = -100
    return reward

def GetNewActions(state, next_state):
    #print("STATE: ", state)
    #print("NEXT STATE: ", next_state)
    new_actions = list(set(next_state) - set(state[0]))
    new_actions = [x for x in new_actions if action_count[int(x)] == 0]
    return len(new_actions)

def ElementMapper(idx_element):
    #print("Element ID INT: ",int(idx_element))
    #print(tree)
    element = tree[int(idx_element)]
    return element.x_center, element.y_center

def CheckTerminated():
    available_actions = action_count[action_space != -1]
    executed_actions = available_actions[available_actions > 0]
    if len(available_actions) == len(executed_actions):
        return True
    return False

def isrespondingPID(PID):
    x = os.system('tasklist /FI "PID eq %d" /FI "STATUS eq running" > tmp.txt' % PID)
    tmp = open('tmp.txt', 'r')
    a = tmp.readlines()
    #print(a)
    tmp.close()
    try:
        if int(a[-1].split()[1]) == PID:
                return True
        else:
            return False
    except:
        return False

def EmptyDirectory(imgs_folder):
    folder = MY_DIRNAME + imgs_folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def reset(pid, path, name, imgs_folder, output_folder):
    terminated = sh.IsTerminated(pid)
    if not terminated:
        os.kill(pid, 9)
    global action_count
    action_count = np.zeros(2901)
    global img_states
    img_states = {}
    global states
    states = {}
    pid = OpenApp(path, name)
    EmptyDirectory(imgs_folder)
    EmptyDirectory(output_folder)
    return pid
