import networkx as nx
import matplotlib.pyplot as plt
from gridGraph import gridGraph
from gridVisualizer import GridVisualizer
from gridArrayGenerator import genGrid
from UxV import UxV
import math
from scipy.spatial import distance

import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm


class MissionArea:
    def __init__(self, name, gridArray, cellDimension):
        self.name = name
        self.grid_visualizer = GridVisualizer(gridArray, cellDimension)
        self.cellDimension = cellDimension
        nrows = self.grid_visualizer.nrows
        ncols = self.grid_visualizer.ncols
        self.vehicles = []
        self.vehicle_assignments = {} # Key - vehicle as tuple: Value - assigned nodes as tuple
        self.grid_graph = gridGraph(nrows, ncols, cellDimension, scale="equal")
        self.neighbors = {}
        self.__remove_obstacle_nodes__()

        
    def draw(self, show_neighbors = False, node_color = False, edge_color = "dimgray"):

        pos = self.grid_graph.pos

        node_colors = ['red' if node in self.vehicles else 'blue' for node in self.grid_graph.graph.nodes()] # Init vehicles as red and empty space as blue
        colors = [
            "yellow", "purple","green", "orange", "cyan", "magenta",
            "lime", "pink", "brown", "gray", "olive", "teal",
            "navy", "maroon", "gold", "indigo", "violet", "turquoise"
        ]

        # Assign region colors
        if node_color is False:
            i = 0
            for assignment in self.vehicle_assignments:
                for index, val in enumerate(self.grid_graph.graph.nodes()):
                    if val in self.vehicle_assignments[assignment]:
                        node_colors[index] = colors[i % len(colors)]
                i += 1
        else:
            node_colors = node_color

        # Assign bordering nodes color (for testing)
        if show_neighbors:
            for neighbors in list(self.neighbors.values()):
                for neighbor in neighbors:
                    index = list(self.grid_graph.graph.nodes()).index(neighbor)
                    node_colors[index] = "turquoise"

        node_size = [50 if node in self.vehicles else 25 for node in self.grid_graph.graph.nodes()]
        nx.draw(self.grid_graph.graph, pos=pos, ax=self.grid_visualizer.ax,
                with_labels=False,
                node_color=node_colors,
                # edge_color='black',
                edge_color= edge_color,
                node_size=node_size,
                font_color='yellow')

        # Square the cells in the graph
        self.grid_visualizer.ax.set_aspect('equal')

        # Adjust plot limits and add a title.
        self.grid_visualizer.ax.set_xlim(-0.7, self.grid_visualizer.scaledNCols)
        self.grid_visualizer.ax.set_ylim(-0.7, self.grid_visualizer.scaledNRows + 0.2)
        self.grid_visualizer.ax.set_title(self.name)

        labels = {}
        for node in self.vehicles:
            labels[node] = node
#        nx.draw_networkx_labels(self.grid_graph.graph, self.grid_graph.pos, labels, font_size=12, font_color='r')

        plt.show()


    def add_vehicle_to_graph(self, node):
        # Input node as a tuple or vehicle object. Must be consistent throughout graph
        if isinstance(node, tuple):
            # self.grid_graph.__add_vehicle_to_graph__(node)
            if self.grid_graph.graph.has_node(node) is False:
                self.grid_graph.graph.add_node(node)

            self.vehicles.append(node)
            self.grid_graph.__update_pos__(node)


        if isinstance(node, UxV): # TODO: this may need to change with implementation of vehicles in algorithm
            node_label = node.position
            if self.grid_graph.graph.has_node(node_label) is False:
                node_label = self._normalize_vehicle_to_graph(node_label)

            self.vehicles.append(node_label)
            self.vehicle_assignments[node_label] = []
            nx.set_node_attributes(self.grid_graph.graph,
                                       {node_label: {'name': node.name, 'type': node.type, "position": node.position,
                                                        "speed": node.speed, "sensorRange": node.sensorRange,
                                                        "endurance": node.endurance, "color": node.color}})
            self.grid_graph.__update_pos__(node_label)
            self.grid_graph.graph.nodes[node_label]['region'] = self.vehicles.index(node_label)


    def add_vehicles_to_graph(self, vehicles):
        for vehicle in vehicles:
            self.add_vehicle_to_graph(vehicle)


    def get_vehicle_attributes(self):
        vehicle_attributes = {node: self.grid_graph.nodes[node] for node in self.vehicles if node in self.grid_graph.graph}
        return vehicle_attributes


    def __remove_obstacle_nodes__(self):
        obstacle_nodes = []
        for node in self.grid_graph.graph.nodes():
            index_tuple = (int((node[0] - .5 * self.cellDimension) / self.cellDimension), int((node[1]- .5 * self.cellDimension) / self.cellDimension))
            if(self.grid_visualizer.gridArray[index_tuple[1], index_tuple[0]] == 0):
                obstacle_nodes.append(node)

        for o_node in obstacle_nodes:
            self.grid_graph.graph.remove_node(o_node)


    # Redraw colormesh after cell decomposition
    def redraw_grid_colormesh(self):
        colors = [
            "black", "white", "yellow", "purple", "green", "orange", "cyan", "magenta",
            "lime", "pink", "brown", "gray", "olive", "teal",
            "navy", "maroon", "gold", "indigo", "violet", "turquoise"
        ]
        updated_grid = self.grid_visualizer.gridArray.copy()

        # Assign a color to each of the unit cells in grid.
        color_index = 2
        for vehicle_assignment in self.vehicle_assignments:
            for node in self.vehicle_assignments[vehicle_assignment]:
                top_node = self.grid_graph.graph.nodes[node]["top"]
                bottom_node = self.grid_graph.graph.nodes[node]["bottom"]
                num_cells_between = int((top_node[1] - bottom_node[1]) / self.cellDimension)
                for i in range(0, num_cells_between + 1):
                    cell_to_change = (top_node[0], top_node[1] - self.cellDimension * i)
                    index_tuple = (int((cell_to_change[0] - .5 * self.cellDimension) / self.cellDimension), int((cell_to_change[1] - .5 * self.cellDimension) / self.cellDimension))
                    updated_grid[index_tuple[1], index_tuple[0]] = color_index
            color_index += 1

        # Rescale the updated grid
        self.grid_visualizer.scaledGrid = np.kron(updated_grid, np.ones((self.grid_visualizer.scale_x, self.grid_visualizer.scale_y)))


        # Add verticle lines to distinguish cells
        # Set every 10th column (0-based index) to 0
        self.grid_visualizer.scaledGrid[:, self.cellDimension-1::self.cellDimension] = 0  # 9::10 selects columns at index 9, 19, etc.


        # Clear the previous plot
        self.grid_visualizer.ax.clear()

        # Redraw the colormesh with updated data
        x = np.arange(self.grid_visualizer.scaledGrid.shape[1] + 1)
        y = np.arange(self.grid_visualizer.scaledGrid.shape[0] + 1)
        cmap = ListedColormap(colors)

        # Generate dynamic boundaries for whole numbers from 0 to len(vehicle_assignments), 0 and 1 are not vehicles
        max_value = len(self.vehicle_assignments) + 2
        boundaries = [i - 0.5 for i in range(max_value + 2)]

        norm = BoundaryNorm(boundaries, len(self.vehicle_assignments) + 3, clip=False)

        c = self.grid_visualizer.ax.pcolormesh(x, y, self.grid_visualizer.scaledGrid, shading='flat', norm=norm, cmap=cmap, rasterized=True)

        # Add colorbar again
        cbar = self.grid_visualizer.fig.colorbar(c, ax=self.grid_visualizer.ax, ticks=range(max_value))

        # Generate labels
        labels = [""] * max_value
        labels[0] = "Dead space"
        labels[1] = "Uncovered"
        for i in range(2,max_value):
            vehicle_speed = self.grid_graph.graph.nodes[self.vehicles[i - 2]]['speed']
            vehicle_sensor_range = self.grid_graph.graph.nodes[self.vehicles[i - 2]]['sensorRange']
            labels[i] = f"Speed: {vehicle_speed}, Sensor Radius: {vehicle_sensor_range}"

        cbar.ax.set_yticklabels(labels)

        self.grid_visualizer.ax.text(1, -20, f"Cell Width: {self.cellDimension}", ha="left", fontsize=12)


    # Vehicle position will be set inside the grid graph. Stores original position and distance from original position
    def _normalize_vehicle_to_graph(self, vehiclePos):  # TODO: This could be made more efficient
            closest_node = min(list(self.grid_graph.graph.nodes()), key=lambda n: distance.euclidean(vehiclePos, n))
            distance_from_graph = distance.euclidean(vehiclePos,closest_node)
            self.grid_graph.graph.nodes[closest_node]["displacement"] = distance_from_graph
            self.grid_graph.graph.nodes[closest_node]["originalPos"] = vehiclePos

            return closest_node




def calculate_sensor_range_gcd(vehicles):
    if len(vehicles) < 2:
        return vehicles[0].sensorRange

    gcd = math.gcd(vehicles[0].sensorRange, vehicles[1].sensorRange)
    for i in range(2, len(vehicles)):
        gcd = math.gcd(gcd, vehicles[i].sensorRange)
        print("GCD: ", gcd)

    return gcd

if __name__ == '__main__':

    grid_data = genGrid(50,75,10)

    mission = MissionArea("alpha", grid_data, 10)
    mission.draw()