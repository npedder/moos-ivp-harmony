import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap, BoundaryNorm
from gridGraph import gridGraph
from gridArrayGenerator import genGrid


class GridVisualizer:
    def __init__(self, gridArray):
        self.gridArray = gridArray
        self.nrows, self.ncols = gridArray.shape

        # Define grid edges (pcolormesh uses edges, so one more than number of cells)
        x = np.arange(self.ncols + 1)
        y = np.arange(self.nrows + 1)

        # Create a ListedColormap for our discrete colors:
        # Order: black (for 0), white (for 1), green (for 1.1), blue (for 1.2)
        cmap = ListedColormap(['black', 'white', 'green', 'blue'])

        # Define boundaries that separate our values.
        # Since our values are 0, 1, 1.1, and 1.2, we can choose boundaries in-between.
        boundaries = [-0.5, 0.5, 1.05, 1.15, 1.25]
        norm = BoundaryNorm(boundaries, cmap.N, clip=True)
        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=(20, 20))

        # Draw the colormesh grid with our custom colormap and normalization.
        c = self.ax.pcolormesh(x, y, gridArray, shading='flat', cmap=cmap, norm=norm)

        # Add a colorbar with tick marks at our data values.
        cbar = self.fig.colorbar(c, ax=self.ax, ticks=[0, 1, 1.1, 1.2])
        cbar.ax.set_yticklabels(['black (0)', 'white (1)', 'green (1.1)', 'blue (1.2)'])

        # For visual reference, mark the grid corners.
        # X, Y = np.meshgrid(x, y)
        # ax.plot(X.flat, Y.flat, 'o', color='m')


