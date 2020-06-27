from RL.imports import *
#from tree import *

class Agent:
    def __init__(self, state_size, action_size, optimizer):
        self._state_size = state_size
        self._action_size = action_size
        self._optimizer = optimizer
        self.history = deque(maxlen=2000)
        self.gamma = 0.85
        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.q_network = self._build_network()
        self.target_network = self._build_network()
        self.align_target_model()

    def store(self, state, action, reward, next_state, terminated):
        self.history.append((state, action, reward, next_state, terminated))

    def _build_network(self):
        '''model = tf.keras.Sequential()
        model.add(tf.keras.layers.Embedding(self._state_size, 10, input_length=1))
        model.add(tf.keras.layers.Reshape((10,)))
        model.add(tf.keras.layers.Dense(50, activation='relu'))
        model.add(tf.keras.layers.Dense(50, activation='relu'))
        model.add(tf.keras.layers.Dense(self._action_size, activation='linear'))
        model.compile(loss='mse', optimizer=self._optimizer)'''
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(50, input_dim=self._state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(50, activation='relu'))
        model.add(tf.keras.layers.Dense(self._action_size, activation='linear'))
        model.compile(loss='mse', optimizer=self._optimizer)
        return model

    def align_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, self.epsilon_min)
        available_actions = np.where(state[0] == 1)[0]
        if len(available_actions) == 0:
            return [0]
        if np.random.rand() <= self.epsilon:
            return random.sample(list(available_actions), 1)
        q_values = self.q_network.predict(state)
        q_values=np.array([q_values[0][int(x)] for x in available_actions ])
        id_max = np.argmax(q_values)
        action_max = available_actions[id_max]
        return [action_max]

    def predict_action(self, state):
        available_actions = np.where(state[0] == 1)[0]
        if len(available_actions) == 0:
            return [0]
        q_values = self.q_network.predict(state)
        q_values = np.array([q_values[0][int(x)] for x in available_actions])
        id_max = np.argmax(q_values)
        action_max = available_actions[id_max]
        return [action_max]

    def retrain(self, batch_size):
        minibatch = random.sample(self.history, batch_size)

        for state, action, reward, next_state, terminated in minibatch:

            target = self.q_network.predict(state)

            if terminated:
                target[0][action] = reward

            else:
                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)

            self.q_network.fit(state, target, epochs=1, verbose=0)

    def load(self, name):
        self.q_network.load_weights(name)

    def save(self, name):
        self.q_network.save_weights(name)