import networkx as nx

class gridGraph:
    def __init__(self, xNumNodes, yNumNodes, distanceBetweenNodes, scale="auto"):
        self.graph = nx.grid_2d_graph(xNumNodes, yNumNodes)
        mapping = {}
        for x, y in self.graph.nodes:
            mapping[(x,y)] = (x * distanceBetweenNodes, y * distanceBetweenNodes)
        self.graph = nx.relabel_nodes(self.graph, mapping, copy=False)

        # Setting scale to "equal" uses matplotlib coordinates to position nodes
        # Setting scale to auto will automatically adjust to a gridVisualizer
        if scale == "auto":
            self.pos = {(x, y): (y/distanceBetweenNodes+ .5, x/distanceBetweenNodes+ .5) for x, y in self.graph.nodes()}
        if scale == "equal":
            self.pos = {(x, y): (y, -x) for x, y in self.graph.nodes()}

        nx.set_edge_attributes(self.graph, values=distanceBetweenNodes, name='weight')


    def drawGraph(self):
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels)
        nx.draw(self.graph, pos=self.pos,
                node_color='lightgreen',
                with_labels=True,
                node_size=600)

    # possibly useless
    def update_edge_weights(self, weight):
            for edge in self.graph.edges():
                print(edge)
                u, v = edge
                # Update the edge with the new weight
                self.graph[u][v]['weight'] = weight
                print(self.graph[u][v]['weight'])

    def print_node_attributes(self):
        for node, attributes in self.graph.nodes(data=True):
            print(node, attributes)

    def print_edge_weights(self):
        for (u, v, wt) in self.graph.edges(data=True):
            print(f"Edge ({u}, {v}) has weight {wt['weight']}")

    def __add_vehicle_to_graph__(self,node):
        vehicle_graph = nx.Graph()
        vehicle_graph.add_node(node)
        pos = {(x, y): (y, x) for x, y in vehicle_graph.nodes()}
        # print(pos)

        self.graph = nx.union(vehicle_graph, self.graph)

        self.pos.update(pos)  # combines the two pos dictionaries

    def __add_vehicles_to_graph__(self, nodeList):
        print("does nothing")




    # edge_weights = [SurveyAreaGraph[u][v]['weight'] for u, v in SurveyAreaGraph.edges()]
