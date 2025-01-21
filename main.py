import networkx as nx
import matplotlib.pyplot as plt
from gridGraph import gridGraph
import math



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
pos.update(SurveyAreaGraph.pos) #combines the two pos dictionaries

v1_node = (90,0)
nodes = list(v1_graph.nodes())
print(nodes)
for node in nodes:
    if node != v1_node :
        weight = math.dist(v1_node, node) #distance between the two nodes is the weight
        v1_graph.add_edge(v1_node, node, weight=weight)

print(v1_graph.edges())

edge_labels = nx.get_edge_attributes(v1_graph, 'weight')
nx.draw_networkx_edge_labels(v1_graph, pos, edge_labels=edge_labels)

nx.draw(v1_graph, pos=pos,
        node_color='blue',
        with_labels=True,
        node_size=600)
#-------------------------------
# Graph for vehicle 2 from vehicle graph
plt.figure(3, figsize=(6,6))
v2_graph = nx.Graph()
v2_graph.add_node(list(VehiclesGraph.nodes())[1])
v2_graph = nx.union(v2_graph, SurveyAreaGraph.graph)
pos = {(x,y):(y,-x) for x,y in v2_graph.nodes()}
pos.update(SurveyAreaGraph.pos) #combines the two pos dictionaries

v2_node = (50, 50)
nodes = list(v2_graph.nodes())
print(nodes)
for node in nodes:
    if node != v2_node :
        weight = math.dist(v2_node, node) #distance between the two nodes is the weight
        v2_graph.add_edge(v2_node, node, weight=weight)

print(v2_graph.edges())

edge_labels = nx.get_edge_attributes(v2_graph, 'weight')
nx.draw_networkx_edge_labels(v2_graph, pos, edge_labels=edge_labels)

nx.draw(v2_graph, pos=pos,
        node_color='blue',
        with_labels=True,
        node_size=600)

#--------------------------------
# v1 and v2 straight line distance comparison

plt.figure(4, figsize=(6,6))
solution_graph = nx.Graph()
solution_graph.add_node(list(VehiclesGraph.nodes())[0])
solution_graph = nx.union(solution_graph, SurveyAreaGraph.graph)
pos = {(x,y):(y,-x) for x,y in solution_graph.nodes()}
pos.update(SurveyAreaGraph.pos) #combines the two pos dictionaries



# Lame solution using a weight offset to account for how many nodes are visited. Doesnt really make sense
print("starting comparion...")
v1_weight_offset = 0
v2_weight_offset = 0


for v1_edge in v1_graph.edges((90,0)):
    v2_edge = ((50,50), v1_edge[1])

    if v1_graph[v1_edge[0]][v1_edge[1]]['weight'] + v1_weight_offset < v2_graph[v2_edge[0]][v2_edge[1]]['weight'] + v2_weight_offset:
        print(v1_graph[v1_edge[0]][v1_edge[1]]['weight'] + v1_weight_offset, "is less than" , v2_graph[v2_edge[0]][v2_edge[1]]['weight'] + v2_weight_offset)
        v1_weight_offset += 10
        # solution_graph.add_edge(v1_edge[0], v1_edge[1])
    else:
        print(v1_graph[v1_edge[0]][v1_edge[1]]['weight'] + v1_weight_offset, "is greater than" , v2_graph[v2_edge[0]][v2_edge[1]]['weight'] + v2_weight_offset)
        v2_weight_offset += 10
# Lame Solution ends

#--------------------------------------------------------------------------------
v1_min_edge = min(v1_graph.edges((90,0),data=True), key=lambda x: x[2]['weight'])
v2_min_edge = min(v2_graph.edges((50,50),data=True), key=lambda x: x[2]['weight'])

for u, v in nx.bfs_edges(SurveyAreaGraph.graph, (40,0)):
    v1_graph[(90,0)][(v)]['weight'] +=10
    print(v1_graph[(90,0)][(v)]['weight'])
    print(u,v)


edge_labels = nx.get_edge_attributes(solution_graph, 'weight')
nx.draw_networkx_edge_labels(solution_graph, pos, edge_labels=edge_labels)

nx.draw(solution_graph, pos=pos,
        node_color='blue',
        with_labels=True,
        node_size=600)

#-------------------------------
shortest_path = dict(nx.all_pairs_dijkstra_path(v1_graph))
print("Shortest Path ",  shortest_path[(0,0)][(0,0)])

plt.show()

