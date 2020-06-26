import _thread
from InrefaceAgent import mouse, keyboard as k, Element_to_Action as eta, shortcuts as sh
from global_imports import *
from RL.imports import *
from tree import *
from RNInterface import *
import shutil
import operator


def OpenApp(app_path, app_name):
    print("starting")
    pid = sh.open_app_foreground(app_path, app_name)
    print(pid)
    # sh.OpenApp("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
    time.sleep(2)
    sh.max()
    time.sleep(1)
    return pid

def GetState(i, img_states, states, tree, action_space, action_count,unique_states):
    state = np.zeros((2,2502))
    #print("ACTION COUNT: ", action_count)
    #print("STATES: ", states)
    #print("IMG STATES: ", states)
    #state = []
    time.sleep(1)
    image, path = save_image(i)
    elements = buildElements(path, i, [Width, Height])
    elements.sort(key=operator.attrgetter('x_center'))
    elements.sort(key=operator.attrgetter('y_center'))
    exists, old_state, diff = img_exists(elements, img_states, image)
    if exists:
        print("state already exists")
        img_states[old_state][0] += 1
        #state[0:min(len(state), len(states[old_state]))] = states[old_state][0:min(len(state), len(states[old_state]))]
        state[0][states[old_state][0]] = 1
        state[1] = GetPotentialActions(action_count,unique_states)
        # state[1][states[old_state]]=action_count[states[old_state]]
        path = old_state
    else:
        img_states[path] = [1, elements]
        states[path]=[[],[]]

        IDs = buildTree(elements, tree, action_space)

        for id in IDs:
            available_actions = np.where(np.array(action_space) == id)[0]
            if len(available_actions) > 0:
                [states[path][0].append(action_id) for action_id in available_actions]
        states[path][1] = (np.zeros(len(states[path][0]))).astype(int)
        states[path][0] = np.array(states[path][0]).astype(int)
        #state[0:min(len(state), len(states[path]))] = states[path][0:min(len(state), len(states[path]))]
        state[0][states[path][0]] = 1
        #state[1][states[old_state]] = action_count[states[old_state]]
        state[1] = GetPotentialActions(action_count,unique_states)
    #state = states[path]
    #print(state)
    #print(len(state))
    state[0][2501] = diff/100
    return state, path

def GetPotentialActions(action_count,unique_states):
    state=np.zeros(2502)
    for i in range(len(action_count)):
        if (action_count[i]==0) or (i not in unique_states and action_count[i]<=5) or (i in unique_states and (np.array(unique_states[i][1])==0).any()):
            state[i]=1
    return state


def SetReward(state, action, action_type, path, new_actions, img_states, next_state, action_count):
    action_type_enum = eta.Actions
    actions = [action_type_enum.click_no_change, action_type_enum.write_letters, action_type_enum.write_numbers, action_type_enum.write_short, action_type_enum.write_long, action_type_enum.write_alphanumeric, action_type_enum.delete]
    if state[0].tolist()==next_state[0].tolist():
        reward=-1
    elif (action_type in actions):
        reward = 1/action_count[action]
    elif state[0][action]==1 and action != 0:
        state_occurences = img_states[path][0]
        reward = (1/state_occurences) * new_actions
    else:
        reward = -1
    return reward

def GetNewActions(state, next_state, unique_states):
    #print("STATE: ", state)
    #print("NEXT STATE: ", next_state)
    new_actions = list(set(next_state[0]) - set(state[0]))
    new_actions = [unique_states[int(x)][1] for x in new_actions if (np.array(unique_states[int(x)][1])==0).any()]
    # new_actions = [x for x in new_actions if action_count[int(x)] == 0]
    return len(new_actions)

def ElementMapper(idx_element,tree):
    #print("Element ID INT: ",int(idx_element))
    #print(tree)
    element = tree[int(idx_element)]
    return element.x_center, element.y_center

def CheckTerminated(episode, states, unique_states):
    if episode == 0:
        for state in states:
            if (states[state][1] == 0).any():
                return False
        return True
    for state in unique_states:
        if (np.array(unique_states[state][1]) == 0).any():
            return False
    return True

    '''available_actions = action_count[action_space != -1]
    executed_actions = available_actions[available_actions > 0]
    if len(available_actions) == len(executed_actions):
        return True
    return False'''

#In the else of the try, this means that the app is not responding so we push 0 to the queue, otherwise we push 1 if the app was terminated
def ErrorHandler(q_pid, q_error_check, q_check_responding):
    while True:
        PID = q_pid.queue[-1]
        os.system('tasklist /FI "PID eq %d" /FI "STATUS eq running" > tmp.txt' % PID)
        tmp = open('tmp.txt', 'r')
        a = tmp.readlines()
        tmp.close()
        os.remove("tmp.txt")
        try:
            if int(a[-1].split()[1]) == PID:
                    pass
            else:
                q_check_responding.put(0)
                _thread.interrupt_main()
                while(PID==q_pid.queue[-1]):
                    pass
        except:
            error_check = q_error_check.queue[-1]
            if error_check == 1:
                q_check_responding.put(1)
                _thread.interrupt_main()
                while (PID == q_pid.queue[-1]):
                    pass


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

def reset(pid, path, name, imgs_folder, output_folder, unique_states):
    terminated = sh.IsTerminated(pid)
    if not terminated:
        os.kill(pid, 9)
    # global action_count
    action_count = np.zeros(2501)
    #global img_states
    img_states = {}
    #global states
    states = {}
    for state in unique_states:
        unique_states[state][1][0:len(unique_states[state][1])] = np.zeros(len(unique_states[state][1])).astype(int).tolist()
    pid = OpenApp(path, name)
    EmptyDirectory(imgs_folder)
    EmptyDirectory(output_folder)
    return pid,action_count,img_states,states,unique_states



