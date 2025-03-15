from scipy.ndimage import gaussian_filter

def genGrid(x, y, seed):
    # For reproducibility
    np.random.seed(seed)

    # Create random noise over a 75x50 area
    noise = np.random.rand(y, x)

    # Apply Gaussian smoothing to group similar values together.
    # Adjust sigma to control cluster size
    smooth_noise = gaussian_filter(noise, sigma=4)

    # Threshold the smoothed noise:
    # Values > 0.5 become 1 (empty space),
    # Values <= 0.5 become 0 (obstacles)
    grid = (smooth_noise > 0.5).astype(int)
    return grid


import numpy as np
import matplotlib.pyplot as plt
import random


def genConnectedGrid(x, y, obstacle_prob, seed):
    """Generates a grid where all empty spaces (1s) are connected, and obstacles (0s) are randomly placed."""
    np.random.seed(seed)
    random.seed(seed)

    # Step 1: Start with an empty grid
    grid = np.ones((y, x), dtype=int)

    # Step 2: Randomly place obstacles while ensuring connectivity
    available_spaces = [(i, j) for i in range(y) for j in range(x)]
    random.shuffle(available_spaces)  # Shuffle for randomness

    def is_fully_connected(grid):
        """Check if all empty spaces are connected using flood-fill."""
        visited = set()
        start = next(((i, j) for i in range(y) for j in range(x) if grid[i, j] == 1), None)

        if not start:
            return False  # No empty space exists

        # Simple DFS for connectivity check
        stack = [start]
        while stack:
            i, j = stack.pop()
            if (i, j) in visited:
                continue
            visited.add((i, j))
            # Explore neighbors
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < y and 0 <= nj < x and grid[ni, nj] == 1:
                    stack.append((ni, nj))

        # Grid is fully connected if all empty spaces are visited
        return len(visited) == np.sum(grid)

    # Step 3: Add obstacles while keeping the space connected
    num_obstacles = int(obstacle_prob * x * y)

    for i, j in available_spaces:
        if num_obstacles <= 0:
            break
        grid[i, j] = 0  # Temporarily place obstacle
        if not is_fully_connected(grid):
            grid[i, j] = 1  # Revert if it disconnects empty space
        else:
            num_obstacles -= 1  # Successfully placed obstacle

    return grid


if __name__ == "__main__":
    width, height = 50, 30
    obstacle_density = 0.3  # 30% of the grid will be obstacles
    seed = 42

    grid = genConnectedGrid(width, height, obstacle_density, seed)

    # Display the grid
    plt.figure(figsize=(10, 6))
    plt.imshow(grid, cmap="gray_r", interpolation="nearest")
    plt.title("Random Obstacles with Fully Connected Empty Space")
    plt.show()


