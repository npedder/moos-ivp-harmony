import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

from gridGraph import gridGraph
from gridVisualizer import GridVisualizer
from MissionArea import MissionArea
from gridArrayGenerator import genGrid
from UxV import UxV
from networkx.algorithms import approximation as approx

# ------------------------ Mission 1 ----------------------------
# Uses tuples
VehicleArray = [(1,50) , (10,-90), (-30, 70), (-60,-60)]
grid_data = genGrid(75,50,22)
mission_alpha = MissionArea("Alpha", grid_data, 10)
# mission_alpha.add_vehicle_to_graph(VehicleArray[0])
# mission_alpha.add_vehicle_to_graph(VehicleArray[1])
# mission_alpha.add_vehicle_to_graph(VehicleArray[2])

mission_alpha.add_vehicles_to_graph(VehicleArray)

# print(list(mission_alpha.grid_graph.graph.nodes()))

# print(mission_alpha.grid_graph.pos)

# vehicle_graph = nx.Graph()
# vehicle_graph.add_node(VehicleArrays[1])
# pos = {(x, y): (y, -x) for x, y in v1_graph.nodes()}

mission_alpha.draw()

# ------------------------ Mission 2 ----------------------------
# Create UxV obejects to be added as nodes
uxv1 = UxV(name="alpha", position=(5,15), speed=(10), sensorRange=(10), type="UUV", endurance=200)
uxv2 = UxV(name="bravo", position=(35,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv3 = UxV(name="Charlie", position=(12,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)

grid_data = genGrid(75, 50, 92)
mission_bravo = MissionArea("Bravo", grid_data, 10)
print(list(mission_bravo.grid_graph.graph.nodes()))
mission_bravo.add_vehicle_to_graph(uxv1)
mission_bravo.add_vehicle_to_graph(uxv2)
mission_bravo.grid_graph.print_node_attributes()

mission_bravo.draw()

plt.show()

#---------------------------------------------------------------------------------------------------------------
# Lame solution using a weight offset to account for how many nodes are visited. Doesnt really make sense
# print("starting comparion...")
# v1_weight_offset = 0
# v2_weight_offset = 0
#
# G = mission_bravo.grid_graph.graph
# vehicles = mission_bravo.vehicles
#
# # Add edges for each vehicle with weight of distance between edges
# for vehicle in vehicles:
#         for node in G.nodes:
#             G.add_edge(vehicle, node, weight=math.dist(vehicle,node) * G.nodes[vehicle]["speed"])
#
#
# print(G.nodes[vehicles[1]])
#
# print()



# for v in G.edges:
#     v2_edge = ((50,50), v1_edge[1])
#
#     if G[v1_edge[0]][v1_edge[1]]['weight'] + v1_weight_offset < v2_graph[v2_edge[0]][v2_edge[1]]['weight'] + v2_weight_offset:
#         print(G[v1_edge[0]][v1_edge[1]]['weight'] + v1_weight_offset, "is less than" , v2_graph[v2_edge[0]][v2_edge[1]]['weight'] + v2_weight_offset)
#         v1_weight_offset += 10
#         # solution_graph.add_edge(v1_edge[0], v1_edge[1])
#     else:
#         print(v1_graph[v1_edge[0]][v1_edge[1]]['weight'] + v1_weight_offset, "is greater than" , v2_graph[v2_edge[0]][v2_edge[1]]['weight'] + v2_weight_offset)
#         v2_weight_offset += 10
#
# for v in G.edges:
#     for in
# Lame Solution ends

#--------------------------------------------------------------------------------



