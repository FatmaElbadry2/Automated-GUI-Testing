from global_imports import *
from agent import *
from actionHandler import *
from Utils import *
from Statistics import *

tree = LoadTree("Files\\tree.csv")
action_space = LoadActionSpace("Files\\action_space.txt")
unique_states = LoadUniqueStates("Files\\unique_states.txt")
unique_states = AdjustUniqueStates(unique_states)
action_count=np.zeros(2501)
states = {}
img_states = {}
action_size = 2501
state_size = 2502

if __name__ == "__main__":

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
    agent = Agent(state_size, action_size, optimizer)
    agent.load("./save/dexter-dqn.h5")

    app_path = "C:\\Program Files\\Elmer 8.4-Release\\bin"
    app_name = "ElmerGUI.exe"
    app_pid = OpenApp(app_path, app_name)
    img_counter = 0
    crash_count=0
    #Threading
    q_pid = queue.Queue()
    q_pid.put(app_pid)
    q_error_check = queue.Queue()
    q_error_check.put(0)
    q_check_responding = queue.Queue()
    threading.Thread(target=ErrorHandler, args=(q_pid, q_error_check, q_check_responding)).start()

    for i in range(500):
        try:
            state, path = GetState(img_counter, img_states, states, tree, action_space, action_count, unique_states, "RL\\Testing")
            state = np.reshape(state, [2, state_size])
            img_counter += 1

            if i!=0 and state[0].tolist() != previous_state[0].tolist():
                if action not in unique_states:
                    unique_states[action] = [[], []]

                path_index = np.where(np.array(unique_states[action][0]) == path)[0]

                if len(path_index) == 0:
                    unique_states[action][0].append(path)
                    if len(unique_states[action][0])==len(unique_states[action][1]):
                        unique_states[action][1].append(1)
                    else:
                        unique_states[action][1][len(unique_states[action][0])-1]+=1
                else:
                    unique_states[action][1][path_index[0]] += 1

            action = agent.predict_action(state)
            action = action[0]
            action = int(action)
            idx_element = action_space[action]
            action_to_do = ActionDecoder(action)
            print("---------------------" + str(action) + "----------------------")

            if action != 0 and int(idx_element) != -1:
                x, y = ElementMapper(idx_element, tree)
                ActionExecuter(action_to_do, x, y)
                action_count[action] += 1
            else:
                break

            previous_state = state

        except KeyboardInterrupt:
            responding = q_check_responding.get()
            if responding == 0:  # not responding
                os.kill(app_pid, 9)
            app_pid = OpenApp(app_path, app_name)
            q_pid.put(app_pid)
            crash_count+=1
            state, path = GetState(img_counter, img_states, states, tree, action_space, action_count, unique_states, "RL\\Training")
            img_counter += 1
            print("exception caught")
            continue

    unique_states_count = GetUniqueStatesNum(img_states)
    state_occurence = GetStateOccurences(img_states)
    action_vs_states = GetActionVsStateNum(unique_states)
    coverage = GetCoverage(unique_states)





