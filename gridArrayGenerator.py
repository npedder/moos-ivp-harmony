import numpy as np

exampleArray = np.array
import numpy as np
from scipy.ndimage import gaussian_filter

def genGrid(seed):
    # For reproducibility
    np.random.seed(seed)

    # Create random noise over a 75x50 area
    noise = np.random.rand(50, 75)

    # Apply Gaussian smoothing to group similar values together.
    # Adjust sigma to control cluster size
    smooth_noise = gaussian_filter(noise, sigma=4)

    # Threshold the smoothed noise:
    # Values > 0.5 become 1 (empty space),
    # Values <= 0.5 become 0 (obstacles)
    grid = (smooth_noise > 0.5).astype(int)
    return grid




