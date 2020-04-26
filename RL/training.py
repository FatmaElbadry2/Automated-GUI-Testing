from imports import *
from agent import *
from actionHandler import *

actionSpace = ActionSpace()
optimizer = tf.keras.Adam(learning_rate = 0.01)
agent = Agent(actionSpace, optimizer)
# state= menYOLO
state = None
batch_size = 32
num_of_episodes = 100
timesteps_per_episode = 1000
agent.q_network.summary()
for e in range(0, num_of_episodes):
    state = np.reshape(state, [1, 1])

    # Initialize variables
    reward = 0
    terminated = False

    bar = progressbar.ProgressBar(maxval=timesteps_per_episode / 10,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for timestep in range(timesteps_per_episode):
        # Run Action
        action = agent.act(state)

        # Take action
        # next_state, reward, terminated, info = enviroment.step(action)
        next_state = np.reshape(next_state, [1, 1])
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

        print("**********************************")