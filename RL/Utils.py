import _thread
from InrefaceAgent import mouse, keyboard as k, Element_to_Action as eta, shortcuts as sh
from global_imports import *
from RL.imports import *
from tree import *
from RNInterface import *
import shutil
import operator
import csv


def OpenApp(app_path, app_name):
    print("starting")
    pid = sh.open_app_foreground(app_path, app_name)
    print(pid)
    # sh.OpenApp("C:\\Program Files (x86)\\FreeMat\\bin", "FreeMat.exe")
    time.sleep(2)
    sh.max()
    time.sleep(1)
    return pid

def GetState(i, img_states, states, tree, action_space, action_count, unique_states, Folder):
    state = np.zeros((2,2502))
    time.sleep(1)
    image, path = save_image(i, Folder)
    elements = buildElements(path, i, [Width, Height], Folder)
    print("lenght of elemets before:  ", len(elements))
    elements=[e for e in elements if not ((e.y_center >42 and e.y_center<72) and((e.x_center >35 and e.x_center<127)or (e.x_center>411 and e.x_center<440))) ]
    print("lenght of elemets after:  ",len(elements))
    elements.sort(key=operator.attrgetter('x_center'))
    elements.sort(key=operator.attrgetter('y_center'))
    exists, old_state, diff = img_exists(elements, img_states, image)

    if exists:
        print("state already exists")
        img_states[old_state][0] += 1
        state[0][states[old_state][0]] = 1
        state[1] = GetPotentialActions(action_count,unique_states)
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
        state[0][states[path][0]] = 1
        state[1] = GetPotentialActions(action_count,unique_states)

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
    actions = [action_type_enum.click_no_change, action_type_enum.write_letters, action_type_enum.write_numbers, action_type_enum.write_short,
               action_type_enum.write_long, action_type_enum.write_alphanumeric, action_type_enum.delete]
    if (action_type in actions):
        reward = 1/action_count[action]
    elif state[0].tolist()==next_state[0].tolist():
        reward=-1
    elif state[0][action]==1 and action != 0:
        state_occurences = img_states[path][0]
        reward = (1/state_occurences) * new_actions
    else:
        reward = -1
    return reward

def GetNewActions(state, next_state, unique_states):
    next_actions= np.where(next_state[0] == 1)[0]
    current_actions= np.where(state[0] == 1)[0]
    new_actions = list(set(next_actions) - set(current_actions))
    new_actions=[x for x in new_actions if x in unique_states]
    print(current_actions)
    if len(new_actions)>0:
        new_actions = [unique_states[int(x)][1] for x in new_actions if (np.array(unique_states[int(x)][1])==0).any()]
    return len(new_actions)

def ElementMapper(idx_element,tree):
    element = tree[int(idx_element)]
    return element.x_center, element.y_center

def CheckTerminated(episode, states, unique_states, action_space, action_count, repeat):
    if episode == 0 or repeat:
        '''for state in states:
            if (states[state][1] == 0).any():'''

        #print(action_space[1:][action_space[(action_space[1:]).astype(int)]!=-1])
        #print(action_count[1:][action_space[(action_space[1:]).astype(int)]!=-1])

        if (action_count[1:][action_space[(action_space[1:]).astype(int)]!=-1]>0).all():
            return True
        return False
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

def SaveActionSpace(action_space, txt_file):
    action_space = action_space.tolist()
    file = open(txt_file,"w")
    file.writelines(str(action_space)[1:len(str(action_space))-1])
    file.close() #to change file access modes

def LoadActionSpace(txt_file):
    file = open(txt_file,"r+")
    file_lines = file.read()
    array = file_lines.split(",")
    array = np.array(array)
    return array.astype(int)

def SaveTree(tree, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for element in tree:
            x_center= element.x_center/Width
            width=element.width/Width
            y_center=element.y_center/Height
            height=element.height/Height
            csv_writer.writerow([element.type, x_center, y_center, width, height, element.text, element.color, element.hex])

def LoadTree(csv_file_path):
    tree = []
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            e = Element()
            e.type = row[0]
            e.x_center = row[1] * Width
            e.y_center = row[2] * Height
            e.width = row[3] * Width
            e.height = row[4] * Height
            e.text = row[5]
            e.color = row[6]
            e.hex = row[7]
            tree.append(e)
            line_count += 1
    return tree

def SaveUniqueStates(unique_states, txt_file):
    key_list = list(unique_states.keys())
    val_list = list(unique_states.values())
    file = open(txt_file,"w")
    for i in range(len(key_list)):
        #print(key_list[i], val_list[i][1][0])
        file.writelines(str(key_list[i]))
        file.writelines(",")
        file.writelines(str(val_list[i][1][0]))
        file.writelines("\n")
    file.close()

def LoadUniqueStates(txt_file):
    unique_states = {}
    file = open(txt_file,"r+")
    file_lines = file.read()
    line_count = 0
    array = []
    for i in range(len(file_lines)):
        if i%2==0:
            line = int(file_lines[i])
            if len(array) == 2:
                unique_states[array[0]] = array [1]
                array = []
                array.append(line)
            else:
                array.append(line)
                if i == len(file_lines)-2:
                    unique_states[array[0]] = array [1]
    return unique_states

def AdjustUniqueStates(unique_states):
    for state in unique_states:
        #print(unique_states[state])
        zeros = np.zeros(unique_states[state]).astype(int).tolist()
        unique_states[state] = [[],zeros]
    return unique_states

