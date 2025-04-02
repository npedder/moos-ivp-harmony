import networkx as nx

class gridGraph:
    def __init__(self, xNumNodes, yNumNodes, distanceBetweenNodes, scale="equal"):
        self.graph = nx.grid_2d_graph(yNumNodes, xNumNodes)
        mapping = {}
        self.normalized_nodes = {(x, y) for x, y in self.graph.nodes()}

        for x, y in self.graph.nodes:
            mapping[(x,y)] = (x * distanceBetweenNodes + distanceBetweenNodes/2, y * distanceBetweenNodes + distanceBetweenNodes/2)
        self.graph = nx.relabel_nodes(self.graph, mapping, copy=False)

        #self.old_pos = {(x, y): (y, x) for x, y in self.graph.nodes()}
        # Setting scale to "equal" uses matplotlib coordinates to position nodes TODO: This is no longer true
        # Setting scale to auto will automatically adjust to a gridVisualizer
        if scale == "auto":
            self.pos = {(x, y): (y/distanceBetweenNodes+ .5, x/distanceBetweenNodes+ .5) for x, y in self.graph.nodes()}
        if scale == "equal":
            self.pos = {(x, y): (x, y) for x, y in self.graph.nodes()}

        nx.set_edge_attributes(self.graph, values=distanceBetweenNodes, name='weight')
        nx.set_node_attributes(self.graph,values=1, name='weight')
        nx.set_node_attributes(self.graph, values=-1, name='region')
        nx.set_node_attributes(self.graph, values=0, name='displacement')

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
                #print(edge)
                u, v = edge
                # Update the edge with the new weight
                self.graph[u][v]['weight'] = weight
                #print(self.graph[u][v]['weight'])

    def print_node_attributes(self):
        for node, attributes in self.graph.nodes(data=True):
            print(node, attributes)

    def print_edge_weights(self):
        for (u, v, wt) in self.graph.edges(data=True):
            print(f"Edge ({u}, {v}) has weight {wt['weight']}")
    #
    # def __add_vehicle_to_graph__(self,node):
    #     vehicle_graph = nx.Graph()
    #     vehicle_graph.add_node(node)
    #     pos = {(x, y): (y, x) for x, y in vehicle_graph.nodes()}
    #     # print(pos)
    #
    #     if(self.graph.has_node(node)): # Replace node if already in graph
    #         self.graph.remove_node(node)
    #
    #     self.graph = nx.union(vehicle_graph, self.graph)
    #
    #     self.pos.update(pos)  # combines the two pos dictionaries

    def __add_vehicles_to_graph__(self, nodeList):
        print("does nothing")

    def __update_pos__(self, node):
        self.pos[(node[0], node[1])] =  (node[0], node[1])








    # edge_weights = [SurveyAreaGraph[u][v]['weight'] for u, v in SurveyAreaGraph.edges()]


if __name__ == '__main__':
    gg = gridGraph(20,10,10)
    print(gg.normalized_nodes)
