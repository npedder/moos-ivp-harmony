import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap, BoundaryNorm
from gridGraph import gridGraph
from gridArrayGenerator import genGrid


class GridVisualizer:
    def __init__(self, gridArray, cellDimension):
        self.gridArray = gridArray
        self.nrows, self.ncols = self.gridArray.shape  # New expanded grid size

        self.scale_x = cellDimension
        self.scale_y = cellDimension

        # Expand the grid array so each cell is scale_y × scale_x in size
        self.scaledGrid = np.kron(gridArray, np.ones((self.scale_x, self.scale_y)))
        self.scaledNRows, self.scaledNCols = self.scaledGrid.shape  # New expanded grid size

        # Define grid edges (pcolormesh uses edges, so one more than number of cells)
        x = np.arange(self.scaledNCols + 1)
        y = np.arange(self.scaledNRows + 1)



        # Create a ListedColormap for our discrete colors:
        # Order: black (for 0), white (for 1),
        colors = [
            "black", "yellow", "purple", "green", "orange", "cyan", "magenta",
            "lime", "pink", "brown", "gray", "olive", "teal",
            "navy", "maroon", "gold", "indigo", "violet", "turquoise"
        ]
        cmap = ListedColormap(colors)

        # Define boundaries that separate our values.
        # Since our values are 0, 1, 1.1, and 1.2, we can choose boundaries in-between.
        max_value = len(colors) - 1  # Ensure boundaries cover all possible values
        boundaries = [i - 0.5 for i in range(max_value + 2)]
        norm = BoundaryNorm(boundaries, cmap.N, clip=True)
        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10,10))

        # Draw the colormesh grid with our custom colormap and normalization.
        c = self.ax.pcolormesh(x, y, self.scaledGrid, shading='flat', cmap=cmap, norm=norm, rasterized=True)


        # For visual reference, mark the grid corners.
        # X, Y = np.meshgrid(x, y)
        # ax.plot(X.flat, Y.flat, 'o', color='m')


