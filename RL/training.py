from global_imports import *
from agent import *
from actionHandler import *
from Utils import *
action_space = np.empty(2901)
action_space.fill(-1)
action_count=np.zeros(2901)
tree = []
img_states = {}
states = {}

if __name__ == "__main__":

    #actionSpace = ActionSpace()
    action_size = 2901
    state_size = 250
    optimizer = tf.keras.optimizers.Adam(learning_rate = 0.01)
    agent = Agent(state_size, action_size, optimizer)

    app_path = "C:\\Program Files\\Elmer 8.4-Release\\bin"
    app_name = "ElmerGUI.exe"
    app_pid = OpenApp(app_path, app_name)

    state, path = GetState(0,img_states,states,tree,action_space)

    img_counter = 1
    batch_size = 32
    num_of_episodes = 10
    timesteps_per_episode = 1000
    agent.q_network.summary()

    #agent.load("./save/dexter-dqn.h5")

    #create
    app_close_bug = False
    q_pid = queue.Queue()
    q_pid.put(app_pid)
    q_error_check = queue.Queue()
    q_error_check.put(0)
    q_check_responding = queue.Queue()
    threading.Thread(target=ErrorHandler, args=(q_pid, q_error_check, q_check_responding)).start()

    for e in range(0, num_of_episodes):
        try:
            if e>0 and not app_close_bug:

                # old_pid = q_pid.get()
                print("---------------------RESET--------------------")
                q_error_check.put(0)
                app_pid,action_count,img_states,states = reset(app_pid, app_path, app_name, "\\RL\\images", "\\RL\\output")
                q_pid.put(app_pid)
                state, path = GetState(img_counter,img_states,states,tree,action_space)
                img_counter += 1
            app_close_bug = False
            state = np.reshape(state, [1, state_size])

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

                    next_state, path = GetState(img_counter,img_states,states,tree,action_space)
                    img_counter+=1
                    new_actions = GetNewActions(state, next_state,action_count)
                else:
                    next_state=state
                    new_actions = 0
                    break
                SetReward(state, action, path, new_actions,img_states)

                next_state = np.reshape(next_state, [1, state_size])
                terminated = CheckTerminated(action_count,action_space)

                agent.store(state, action, reward, next_state, terminated)
                state = next_state

                if terminated:
                    agent.align_target_model()
                    break

                if len(agent.history) > batch_size:
                    agent.retrain(batch_size)

                if timestep % 10 == 0:
                    bar.update(timestep / 10 + 1)

            bar.finish()
            if (e + 1) % 10 == 0:
                print("**********************************")
                print("Episode: {}".format(e + 1))
                agent.save(MY_DIRNAME + "\\RL\\Weights\\dexter-dqn.h5")

                print("**********************************")
        except KeyboardInterrupt:
            responding = q_check_responding.get()
            if responding == 0: # not responding
                os.kill(app_pid, 9)
            app_pid = OpenApp(app_path, app_name)
            print("1st in main", app_pid)
            q_pid.put(app_pid)
            print("2nd in main", q_pid.queue[-1])
            app_close_bug = True
            state, path = GetState(img_counter, img_states, states, tree, action_space)
            img_counter += 1
            print("exception caught")
            continue



