import networkx as nx
import matplotlib.pyplot as plt
from gridGraph import gridGraph
from gridVisualizer import GridVisualizer
from gridArrayGenerator import genGrid
from UxV import UxV



class MissionArea:
    def __init__(self, name, gridArray, cellDimension):
        self.name = name
        self.grid_visualizer = GridVisualizer(gridArray, cellDimension)
        self.cellDimension = cellDimension
        nrows = self.grid_visualizer.nrows
        ncols = self.grid_visualizer.ncols
        self.vehicles = []
        self.vehicle_assignments = {}
        self.grid_graph = gridGraph(nrows, ncols, cellDimension, scale="equal")
        self.neighbors = {}
        self.__remove_obstacle_nodes__()

        
    def draw(self, show_neighbors = False):
        pos = self.grid_graph.pos

        node_colors = ['red' if node in self.vehicles else 'blue' for node in self.grid_graph.graph.nodes()] # Init vehicles as red and empty space as blue
        colors = [
            "yellow", "purple","green", "orange", "cyan", "magenta",
            "lime", "pink", "brown", "gray", "olive", "teal",
            "navy", "maroon", "gold", "indigo", "violet", "turquoise"
        ]

        # Assign region colors
        i = 0
        for assignment in self.vehicle_assignments:
            for index, val in enumerate(self.grid_graph.graph.nodes()):
                if val in self.vehicle_assignments[assignment]:
                    node_colors[index] = colors[i % len(colors)]
            i += 1

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
                edge_color="black",
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
        nx.draw_networkx_labels(self.grid_graph.graph, self.grid_graph.pos, labels, font_size=12, font_color='r')

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
                self.grid_graph.graph.add_node(node_label)

            self.vehicles.append(node_label)
            self.vehicle_assignments[node_label] = []
            nx.set_node_attributes(self.grid_graph.graph,
                                       {node_label: {'name': node.name, 'type': node.type, "position": node.position,
                                                        "speed": node.speed, "sensorRange": node.sensorRange,
                                                        "endurance": node.endurance, "color": node.color}})
            self.grid_graph.__update_pos__(node_label)
            self.grid_graph.graph.nodes[node_label]['region'] = self.vehicles.index(node_label)


    def add_vehicles_to_graph(self, nodesArray):
        for node in nodesArray:
            self.add_vehicle_to_graph(node)
            self.vehicles.append(node)

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


if __name__ == '__main__':

    grid_data = genGrid(50,75,10)

    mission = MissionArea("alpha", grid_data, 10)
    mission.draw()