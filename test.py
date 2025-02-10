import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap, BoundaryNorm


def plot_custom_grid_with_graph(grid_data):
    """
    Plots a grid where:
      - 0 is black
      - 1 is white
      - 1.1 is green
      - 1.2 is blue
    and overlays a NetworkX grid graph so that each grid cell contains one node.

    Parameters:
        grid_data (np.ndarray): 2D array of values {0, 1, 1.1, 1.2}.
    """

    grid_data = grid_data[::-1, :]

    nrows, ncols = grid_data.shape
    # Define grid edges (pcolormesh uses edges, so one more than number of cells)
    x = np.arange(ncols + 1)
    y = np.arange(nrows + 1)

    # Create a ListedColormap for our discrete colors:
    # Order: black (for 0), white (for 1), green (for 1.1), blue (for 1.2)
    cmap = ListedColormap(['black', 'white', 'green', 'blue'])

    # Define boundaries that separate our values.
    # Since our values are 0, 1, 1.1, and 1.2, we can choose boundaries in-between.
    boundaries = [-0.5, 0.5, 1.05, 1.15, 1.25]
    norm = BoundaryNorm(boundaries, cmap.N, clip=True)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw the colormesh grid with our custom colormap and normalization.
    c = ax.pcolormesh(x, y, grid_data, shading='flat', cmap=cmap, norm=norm)

    # Optionally, add a colorbar with tick marks at our data values.
    cbar = fig.colorbar(c, ax=ax, ticks=[0, 1, 1.1, 1.2])
    cbar.ax.set_yticklabels(['black (0)', 'white (1)', 'green (1.1)', 'blue (1.2)'])

    # For visual reference, mark the grid corners.
    X, Y = np.meshgrid(x, y)
    ax.plot(X.flat, Y.flat, 'o', color='m')

    # Create a grid graph with one node per grid cell using NetworkX.
    # The nodes are identified by (row, col).
    G = nx.grid_2d_graph(nrows, ncols)

    # Position each node at the center of its corresponding grid cell.
    # pcolormesh draws a cell from [col, col+1] and [row, row+1], so the center is (col + 0.5, row + 0.5).
    pos = {(row, col): (col + 0.5, row + 0.5) for row, col in G.nodes()}

    # Draw the graph on top of the grid.
    nx.draw(G, pos=pos, ax=ax,
            with_labels=True,
            node_color='red',
            edge_color='black',
            node_size=500,
            font_color='white')
    #square graph
    ax.set_aspect('equal')

    # Adjust plot limits and add a title.
    ax.set_xlim(-0.7, ncols)
    ax.set_ylim(-0.7, nrows + 0.2)
    ax.set_title("Custom Grid with Overlaid NetworkX Graph")

    plt.show()


# Example grid data: 3 rows x 5 columns
grid_data = np.array([
    [0, 1, 1.1, 1.2, 1, 0, 0, 1],
    [1, 0, 1.1, 1.2, 0,1,1.2,1.3],
    [1.2, 1.1, 1, 0, 1,1,1.2,1.2]
])

plot_custom_grid_with_graph(grid_data)
