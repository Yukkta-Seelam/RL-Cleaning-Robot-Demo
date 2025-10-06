import matplotlib.pyplot as plt
import numpy as np
from train_and_run import run_simulation

algorithm = "q_learning"
print(f"🧠 Running algorithm: {algorithm.upper()}")

frames = run_simulation(algorithm, (5,5), 3, episodes=50)
print(f"✅ Simulation complete using {algorithm.upper()}!")

# Define a simple color map for: 0=clean, 1=obstacle, 2=robot, 3=trash
from matplotlib.colors import ListedColormap
cmap = ListedColormap(["white", "black", "blue", "brown"])

for i, f in enumerate(frames):
    plt.imshow(f, cmap=cmap, vmin=0, vmax=3)
    plt.title(f"{algorithm.upper()} - Step {i+1}")
    plt.axis('off')
    plt.pause(0.25)

plt.show()
