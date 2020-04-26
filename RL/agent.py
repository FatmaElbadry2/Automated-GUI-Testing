from imports import *
from tree import *


class Agent:
    def __init__(self, actionSpace, optimizer):
        self._action_size = len(actionSpace)
        self._optimizer = optimizer
        self.action_space = actionSpace
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

    def _build_network(self, statesize):
        model = tf.keras.Sequential()
        model.add(tf.keras.Embedding(statesize, 10, input_length=1))
        model.add(tf.keras.Reshape((10,)))
        model.add(tf.keras.Dense(50, activation='relu'))
        model.add(tf.keras.Dense(50, activation='relu'))
        model.add(tf.keras.Dense(self._action_size, activation='linear'))
        model.compile(loss='mse', optimizer=self._optimizer)
        return model

    def align_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state, availableActions):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, self.epsilon_min)
        if np.random.rand() <= self.epsilon:
            return random.sample(availableActions, 1)
        q_values = self.q_network.predict(state)
        return np.argmax(q_values[0])

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