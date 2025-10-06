import time
import random
import numpy as np

class RLAgent:
    def __init__(self, env, algorithm='q_learning', alpha=0.5, gamma=0.95, epsilon=0.2, n_planning=5):
        self.env = env
        self.algorithm = algorithm
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_planning = n_planning
        self.q_table = {}
        self.model = {}
        self.rewards_per_episode = []
        self.avg_rewards_per_episode = []
        self.steps_per_episode = []
        self.total_time = 0
        self.best_reward = -float('inf')
        self.best_q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 5.0)

    def set_q_value(self, state, action, value):
        self.q_table[(state, action)] = value
        current_reward = np.sum(self.rewards_per_episode) if self.rewards_per_episode else 0
        if current_reward > self.best_reward:
            self.best_reward = current_reward
            self.best_q_table = self.q_table.copy()

    def choose_action(self, state, epsilon=None):
        if epsilon is None:
            epsilon = self.epsilon
        if random.random() < epsilon:
            return random.randint(0, 2)
        q_values = [self.get_q_value(state, a) for a in range(3)]
        max_q = max(q_values)
        best_actions = [a for a, q in enumerate(q_values) if q == max_q]
        return random.choice(best_actions)

    def update_model(self, state, action, reward, next_state):
        self.model[(state, action)] = (reward, next_state)

    def plan(self, n_steps):
        for _ in range(n_steps):
            if self.model:
                state_action = random.choice(list(self.model.keys()))
                reward, next_state = self.model[state_action]
                state, action = state_action
                next_q_values = [self.get_q_value(next_state, a) for a in range(3)]
                max_next_q = max(next_q_values) if next_q_values else 0
                current_q = self.get_q_value(state, action)
                new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
                self.set_q_value(state, action, new_q)

    def train_episode(self, max_steps=1000):
        start_time = time.time()
        state = self.env.reset()
        total_reward = 0
        steps = 0

        if self.algorithm == 'sarsa':
            action = self.choose_action(state)

        while steps < max_steps and not self.env.done:
            if self.algorithm == 'sarsa':
                next_state, reward, done = self.env.step(action)
                total_reward += reward
                steps += 1
                next_action = self.choose_action(next_state)
                current_q = self.get_q_value(state, action)
                next_q = self.get_q_value(next_state, next_action)
                new_q = current_q + self.alpha * (reward + self.gamma * next_q - current_q)
                self.set_q_value(state, action, new_q)
                state, action = next_state, next_action

            elif self.algorithm == 'q_learning':
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                total_reward += reward
                steps += 1
                current_q = self.get_q_value(state, action)
                next_q_values = [self.get_q_value(next_state, a) for a in range(3)]
                max_next_q = max(next_q_values) if next_q_values else 0
                new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
                self.set_q_value(state, action, new_q)
                state = next_state

            elif self.algorithm == 'dyna_q':
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                total_reward += reward
                steps += 1
                current_q = self.get_q_value(state, action)
                next_q_values = [self.get_q_value(next_state, a) for a in range(3)]
                max_next_q = max(next_q_values) if next_q_values else 0
                new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
                self.set_q_value(state, action, new_q)
                self.update_model(state, action, reward, next_state)
                self.plan(self.n_planning)
                state = next_state

            elif self.algorithm == 'td_zero':
                action = random.randint(0, 2)
                next_state, reward, done = self.env.step(action)
                total_reward += reward
                steps += 1
                current_value = max([self.get_q_value(state, a) for a in range(3)])
                next_value = max([self.get_q_value(next_state, a) for a in range(3)])
                for a in range(3):
                    current_q = self.get_q_value(state, a)
                    new_q = current_q + self.alpha * (reward + self.gamma * next_value - current_q)
                    self.set_q_value(state, a, new_q)
                state = next_state

        self.rewards_per_episode.append(total_reward)
        self.avg_rewards_per_episode.append(total_reward / steps if steps > 0 else 0)
        self.steps_per_episode.append(steps)
        self.total_time += time.time() - start_time
        return total_reward, steps

    def train(self, episodes=200, max_steps=1000):
        print(f"Training {self.algorithm} for {episodes} episodes...")
        for episode in range(episodes):
            reward, steps = self.train_episode(max_steps)
            self.epsilon = max(0.01, 0.2 * (0.99 ** episode))
            if (episode + 1) % 20 == 0:
                print(f"Episode {episode+1}: Reward = {reward:.2f}, Steps = {steps}, ε = {self.epsilon:.3f}")

    # ----------------------------------------------------------------------
    # Animation logic (with visible trash)
    # ----------------------------------------------------------------------
    def generate_animation_frames(self, max_steps=200):
        frames = []
        original_q_table = self.q_table
        self.q_table = self.best_q_table if self.best_q_table else self.q_table
        state = self.env.reset()
        steps = 0

        while steps < max_steps and not self.env.done:
            grid_frame = np.copy(self.env.grid)
            for r in range(self.env.rows):
                for c in range(self.env.cols):
                    if self.env.grid[r, c] == 0 and not self.env.cleaned[r, c]:
                        grid_frame[r, c] = 3  # trash
            r, c = self.env.robot_pos
            grid_frame[r, c] = 2
            frames.append(grid_frame.tolist())

            action = self.choose_action(state, epsilon=0)
            state, _, _ = self.env.step(action)
            steps += 1

        grid_frame = np.copy(self.env.grid)
        for r in range(self.env.rows):
            for c in range(self.env.cols):
                if self.env.grid[r, c] == 0 and not self.env.cleaned[r, c]:
                    grid_frame[r, c] = 3
        r, c = self.env.robot_pos
        grid_frame[r, c] = 2
        frames.append(grid_frame.tolist())

        self.q_table = original_q_table
        return frames
