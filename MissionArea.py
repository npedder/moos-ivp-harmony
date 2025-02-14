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
        nrows = self.grid_visualizer.nrows
        ncols = self.grid_visualizer.ncols
        self.vehicles = []
        self.grid_graph = gridGraph(nrows, ncols, cellDimension, scale="equal")

    def draw(self):
        pos = self.grid_graph.pos
        node_colors = ['red' if node in self.vehicles else 'blue' for node in self.grid_graph.graph.nodes()]
        node_size = [50 if node in self.vehicles else 1 for node in self.grid_graph.graph.nodes()]
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
           # self.grid_graph.__add_vehicle_to_graph__(node.position)
            if self.grid_graph.graph.has_node(node.position) is False:
                self.grid_graph.graph.add_node(node.position)

            self.vehicles.append(node.position)
            nx.set_node_attributes(self.grid_graph.graph,
                                       {node.position: {'name': node.name, 'type': node.type, "position": node.position,
                                                        "speed": node.speed, "sensorRange": node.sensorRange,
                                                        "endurance": node.endurance, "color": node.color}})



    def add_vehicles_to_graph(self, nodesArray):
        for node in nodesArray:
            self.add_vehicle_to_graph(node)
            self.vehicles.append(node)

    def print_vehicle_attributes(self):
        vehicle_attributes = {node: self.grid_graph.nodes[node] for node in self.vehicles if node in self.grid_graph.graph
}

if __name__ == '__main__':

    grid_data = genGrid(42)

    mission = MissionArea("alpha", grid_data, 10)
    mission.draw()