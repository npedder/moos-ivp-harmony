import networkx as nx
import matplotlib.pyplot as plt
from gridGraph import gridGraph



plt.figure(1, figsize=(6,6))

# Grid Graph
SurveyAreaGraph = gridGraph(5,5,10)
SurveyAreaGraph.drawGraph()
# print(list(SurveyAreaGraph.graph.nodes()))
# print(SurveyAreaGraph.print_node_attributes())
SurveyAreaGraph.print_edge_weights()
# plt.show()


# --------------------------------------
# Graph for vehicles
VehiclesGraph = nx.Graph()
VehiclesGraph.add_node((90, 0))
VehiclesGraph.add_node((50, 50))
print(VehiclesGraph.nodes())
pos={(x,y):(y,-x) for x,y in VehiclesGraph.nodes()}
print(pos)
nx.draw(VehiclesGraph, pos=pos,
        node_color='blue',
        with_labels=True,
        node_size=600)


#-------------------------------
# Graph for vehicle 1 from vehicle graph
plt.figure(2, figsize=(6,6))
v1_graph = nx.Graph()
v1_graph.add_node(list(VehiclesGraph.nodes())[0])
v1_graph = nx.union(v1_graph, SurveyAreaGraph.graph)
pos = {(x,y):(y,-x) for x,y in v1_graph.nodes()}
pos.update(SurveyAreaGraph.pos)
nx.draw(v1_graph, pos=pos,
        node_color='blue',
        with_labels=True,
        node_size=600)

shortest_path = dict(nx.all_pairs_dijkstra_path(v1_graph))
print("Shortest Path ",  shortest_path[(0,0)][(0,0)])

plt.show()

