import networkx as nx
import matplotlib.pyplot as plt

class gridGraph:
    def __init__(self, xNumNodes, yNumNodes, distanceBetweenNodes):
        self.graph = nx.grid_2d_graph(xNumNodes, yNumNodes)
        self.pos = {(x, y): (y * distanceBetweenNodes, -x * distanceBetweenNodes) for x, y in self.graph.nodes()}
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


    # edge_weights = [SurveyAreaGraph[u][v]['weight'] for u, v in SurveyAreaGraph.edges()]
