# env.py
import numpy as np
import random

class GridWorld:
    def __init__(self, grid_size=(4, 5), obstacles=None, start_pos=(0, 0), start_dir=0):
        self.grid_size = grid_size
        self.rows, self.cols = grid_size
        self.grid = np.zeros(grid_size, dtype=int)
        if obstacles:
            for obs in obstacles:
                self.grid[obs] = 1
        self.start_pos = start_pos
        self.start_dir = start_dir
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.reset()

    def reset(self):
        self.robot_pos = self.start_pos
        self.robot_dir = self.start_dir
        self.cleaned = np.zeros(self.grid_size, dtype=bool)
        self.visited = np.zeros(self.grid_size, dtype=int)
        self.total_reward = 0
        self.steps = 0
        self.done = False
        self.visited[self.robot_pos] = 1
        return self.get_state()

    def get_state(self):
        """Simplify state to (row, col, direction) to reduce dimensionality."""
        return (self.robot_pos[0], self.robot_pos[1], self.robot_dir)

    def step(self, action):
        reward = 0
        self.steps += 1

        if action == 0:  # move forward
            dr, dc = self.directions[self.robot_dir]
            new_pos = (self.robot_pos[0] + dr, self.robot_pos[1] + dc)
            if (0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols
                and self.grid[new_pos] == 0):
                self.robot_pos = new_pos
                self.visited[new_pos] += 1
                if not self.cleaned[new_pos]:
                    self.cleaned[new_pos] = True
                    reward = +2    # reward for cleaning new cell
                else:
                    reward = -0.5  # small penalty for revisiting
            else:
                reward = -5       # smaller penalty for wall/obstacle
        elif action == 1:
            self.robot_dir = (self.robot_dir - 1) % 4
            reward = -0.1        # small turn penalty
        elif action == 2:
            self.robot_dir = (self.robot_dir + 1) % 4
            reward = -0.1

        self.total_reward += reward

        # task completion bonus
        if np.sum(self.cleaned) == np.sum(self.grid == 0):
            self.done = True
            reward += 50

        return self.get_state(), reward, self.done
