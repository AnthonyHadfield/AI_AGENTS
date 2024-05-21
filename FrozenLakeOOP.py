import gym
import numpy as np
import warnings
import sys

"""Filter out the DeprecationWarning"""
warnings.filterwarnings("ignore", category=DeprecationWarning)

class FrozenLake:
    def __init__(self):
        """Initialize the FrozenLake environment, Q-table, hyperparameters, and target counter"""
        self.env = gym.make('FrozenLake-v1', render_mode='human')
        self.Q = np.zeros((self.env.observation_space.n, self.env.action_space.n))
        """Learning rate"""
        self.alpha = 0.5
        """Discount factor"""
        self.gamma = 0.99
        """Initial exploration rate"""
        self.epsilon_start = 1.0
        """Final exploration rate"""
        self.epsilon_end = 0.01
        """Exploration decay rate"""
        self.epsilon_decay = 0.0005
        """Number of episodes"""
        self.episodes = 60000
        """Counter for reaching the target"""
        self.targets = 0

    def choose_action(self, state, epsilon):
        """Choose an action based on the epsilon-greedy policy"""
        if np.random.uniform() < epsilon:
            """Explore"""
            action = self.env.action_space.sample()
        else:
            """Exploit"""
            action = np.argmax(self.Q[state])
        return action

    def update_q_table(self, state, action, reward, next_state):
        """Update the Q-table based on the observed reward and next state"""
        self.Q[state, action] += self.alpha * (reward + self.gamma * np.max(self.Q[next_state]) - self.Q[state, action])

    def train(self):
        """Train the agent using Q-learning"""
        for episode in range(self.episodes):
            """Reset environment and get initial state"""
            state = self.env.reset()[0]
            done = False
            """Decaying epsilon"""
            epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * np.exp(-self.epsilon_decay * episode)

            while not done:
                action = self.choose_action(state, epsilon)
                """Take action and get next state"""
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                """Check if the episode is done"""
                done = terminated or truncated

                """Increment target counter and print message when the agent reaches the target"""
                if reward == 1:
                    self.targets += 1

                self.update_q_table(state, action, reward, next_state)

                state = next_state

            """Print Average Rewards, Goal Targets, Episodes, and Efficiency"""
            average_reward = sum(self.Q[self.env.reset()[0]]) / self.env.observation_space.n
            efficiency = (self.targets / (episode + 1)) * 100
            sys.stdout.write(f"\rAverage Rewards {average_reward:.3f}, Goal Targets = {self.targets}, Episodes = "
                             f"{episode + 1}, Efficiency = {efficiency:.2f}%")
            sys.stdout.flush()

            """Print Q-table every 10 cycles"""
            if (episode + 1) % 10 == 0:
                print("\nQ-table:")
                print(np.round(self.Q, 3))

    def test(self):
        """Test the trained agent"""
        state = self.env.reset()[0]
        done = False
        while not done:
            action = np.argmax(self.Q[state])
            next_state, _, terminated, truncated, _ = self.env.step(action)
            done = terminated or truncated
            state = next_state
            self.env.render()


"""Create an instance of the FrozenLake class"""
data = FrozenLake()

"""Train the agent"""
data.train()

"""Test the trained agent"""
data.test()