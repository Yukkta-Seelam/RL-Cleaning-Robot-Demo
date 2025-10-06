# train_and_run.py
from env import GridWorld
from algorithms import RLAgent

def run_simulation(algorithm_name, grid_size=(4, 5), num_obstacles=3, episodes=100):
    # Randomly place obstacles
    import random
    obstacles = set()
    while len(obstacles) < num_obstacles:
        r = random.randint(0, grid_size[0]-1)
        c = random.randint(0, grid_size[1]-1)
        if (r, c) != (0, 0):
            obstacles.add((r, c))

    env = GridWorld(grid_size=grid_size, obstacles=list(obstacles), start_pos=(0, 0), start_dir=0)
    agent = RLAgent(env, algorithm=algorithm_name, alpha=0.5, gamma=0.95, epsilon=0.2, n_planning=5)
    agent.train(episodes=episodes, max_steps=300)
    frames = agent.generate_animation_frames(max_steps=150)
    return frames
