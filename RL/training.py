from global_imports import *
from agent import *
from actionHandler import *
from Utils import *
action_space = np.empty(2501)
action_space.fill(-1)
action_count=np.zeros(2501)
tree = []
img_states = {}
states = {}
unique_states = {}

if __name__ == "__main__":

    #actionSpace = ActionSpace()
    action_size = 2501
    state_size = 2502
    optimizer = tf.keras.optimizers.Adam(learning_rate = 0.01)
    agent = Agent(state_size, action_size, optimizer)

    app_path = "C:\\Program Files\\Elmer 8.4-Release\\bin"
    app_name = "ElmerGUI.exe"
    app_pid = OpenApp(app_path, app_name)

    state, path = GetState(0,img_states,states,tree,action_space,action_count,unique_states, "RL\\Training")

    img_counter = 1
    batch_size = 32
    num_of_episodes = 10
    timesteps_per_episode = 1000
    agent.q_network.summary()

    #create
    app_close_bug = False
    q_pid = queue.Queue()
    q_pid.put(app_pid)
    q_error_check = queue.Queue()
    q_error_check.put(0)
    q_check_responding = queue.Queue()
    threading.Thread(target=ErrorHandler, args=(q_pid, q_error_check, q_check_responding)).start()
    goal_reached = False
    repeat = False
    for e in range(0, num_of_episodes):
        try:
            if e>0 and not app_close_bug:
                # old_pid = q_pid.get()
                print("---------------------RESET--------------------")
                q_error_check.put(0)
                app_pid,action_count,img_states,states,unique_states = reset(app_pid, app_path, app_name, "\\RL\\Training\\images", "\\RL\\Training\\output", unique_states)
                q_pid.put(app_pid)
                state, path = GetState(img_counter,img_states,states,tree,action_space,action_count,unique_states, "RL\\Training")
                img_counter += 1
            app_close_bug = False
            state = np.reshape(state, [2, state_size])

            # Initialize variables
            reward = 0
            terminated = False

            bar = progressbar.ProgressBar(maxval=timesteps_per_episode / 10,
                                          widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
            bar.start()

            for timestep in range(timesteps_per_episode):
                if (not q_error_check.empty()) and (q_error_check.queue[-1]==0):
                    q_error_check.put(1)
                # Run Action
                action = agent.act(state)
                action = action[0]
                action = int(action)
                idx_element = action_space[action]
                #print(idx_element)
                # Take action
                action_to_do = ActionDecoder(action)
                print("---------------------" + str(action) + "----------------------")
                if action != 0 and int(idx_element) != -1 :
                    x, y = ElementMapper(idx_element,tree)
                    ActionExecuter(action_to_do, x, y)
                    action_count[action]+=1
                    # next_state, reward, terminated, info = enviroment.step(action)
                    if e == 0:
                        states[path][1][states[path][0]==action]+=1
                    next_state, path = GetState(img_counter, img_states, states, tree, action_space, action_count,unique_states, "RL\\Training")
                    img_counter += 1
                    new_actions = 0
                    if state[0].tolist() != next_state[0].tolist():
                        if action not in unique_states :
                            unique_states[action]=[[],[]]

                        path_index = np.where(np.array(unique_states[action][0])==path)[0]

                        if len(path_index) ==0 :
                            unique_states[action][0].append(path)
                            unique_states[action][1].append(1)
                        else:
                            unique_states[action][1][path_index[0]] += 1
                        new_actions = GetNewActions(state, next_state,action_count)
                else:
                    next_state=state
                    new_actions = 0
                    break
                reward = SetReward(state, action, action_to_do, path, new_actions, img_states, next_state, action_count)
                '''print(tree)
                print(action_space)
                print(unique_states)'''

                next_state = np.reshape(next_state, [2, state_size])
                terminated = CheckTerminated(e, states, unique_states, action_space, action_count, repeat)

                agent.store(state, action, reward, next_state, terminated)
                state = next_state

                if terminated:
                    agent.align_target_model()
                    goal_reached = True
                    repeat = False
                    break

                if timestep==999 and not goal_reached:
                    repeat=True


                if len(agent.history) > batch_size:
                    agent.retrain(batch_size)

                if timestep % 10 == 0:
                    bar.update(timestep / 10 + 1)

            bar.finish()
            if (e + 1) % 2 == 0:
                print("**********************************")
                print("Episode: {}".format(e + 1))

                agent.save(MY_DIRNAME + "\\RL\\Weights\\dexter-dqn.h5")
                #----save tree and action space----
                SaveActionSpace(action_space, "Files\\action_space.txt")
                SaveTree(tree, "Files\\tree.csv")
                SaveUniqueStates(unique_states, "Files\\unique_states.txt")

                print("**********************************")
        except KeyboardInterrupt:
            responding = q_check_responding.get()
            if responding == 0: # not responding
                os.kill(app_pid, 9)
            app_pid = OpenApp(app_path, app_name)
            #print("1st in main", app_pid)
            q_pid.put(app_pid)
            #print("2nd in main", q_pid.queue[-1])
            app_close_bug = True
            state, path = GetState(img_counter, img_states, states, tree, action_space,action_count, unique_states, "RL\\Training")
            img_counter += 1
            print("exception caught")
            continue



