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


# ------------- Mission 3 --------------------
def calculate_pk(mission: MissionArea, vehicle):
    velocity_r = mission.grid_graph.graph.nodes[vehicle]['speed']
    summation_v_k = 0
    R = mission.vehicles
    for r in R:
        velocity_k = mission.grid_graph.graph.nodes[r]['speed']
        summation_v_k+= velocity_k

    p_k = (velocity_r / summation_v_k) * w(mission)

    return p_k


def w(mission: MissionArea):  # would only work if all cells are the same size?
    V = mission.grid_graph.graph.number_of_nodes()
    print("Total number of nodes: ", V)
    summation_node_weights = 0
    summation_node_weights = V #* mission.cellDimension # just assumes that each cell is same size

    return summation_node_weights

def gcd_of_list(numList):
    gcd = math.gcd(numList[0], numList[1])
    for i in range(2, len(numList)):
        gcd = math.gcd(gcd, numList[i])
        print("GCD: ", gcd)

    return gcd


def update_NV_K(mission: MissionArea, NV_K, cell, assigned_nodes):
    if(cell in NV_K):
        newNodes = set(mission.grid_graph.graph[cell].keys())
        for node in assigned_nodes: # TODO: questionable for statement
            if node in newNodes:
                newNodes.remove(node)

        NV_K.update(newNodes)
        NV_K.remove(cell)
        print("NVK ", NV_K)

    return NV_K



def cylcic_region_growth(mission: MissionArea, R, OptimalTasks):
    assigned_nodes = set() # not sure if this is right
    N = mission.grid_graph.graph.number_of_nodes()
    rate = [0] * len(R)
    NV_K = set() # The set of all adjacent unassigned tasks
    NV_k = [0] * len(R) # The set of each robot's adjacent unassigned tasks, separated by lists
    f = [0] * len(R) # each robot's capital (optimal number of tasks
    for i in range(len(R)):
        f[i] = OptimalTasks[i]
        rate[i] = int(OptimalTasks[i]/gcd_of_list(OptimalTasks))
        print(OptimalTasks[i])
        print(list(mission.grid_graph.graph[R[i]].keys()))
        NV_K.update(set(mission.grid_graph.graph[R[i]].keys())) # Should return node names for neighboring nodes
        NV_k[i] = set((mission.grid_graph.graph[R[i]].keys()))


    last_updated_cell = 0;
    while (N > 0):
        for k in range(0, len(R)):
            if k == 1: print("-----------------------------------", rate[k])
            if k == 2: print("-----------------------------------", rate[k])
            for j in range(0, rate[k]):
                NV_K = update_NV_K(mission, NV_K, last_updated_cell, assigned_nodes) #NV_K is the task set that has not been purchased yet, adjacent to Vk
                NV_k[k] = update_NV_K(mission, NV_k[k], last_updated_cell, assigned_nodes)
                print(rate[k])
                if NV_k[k]: #Checks if list of NVs are empty
                    last_updated_cell =  list(NV_k[k])[j] # select a cell from NV_k
                    mission.vehicle_assignments[mission.vehicles[k]].append(last_updated_cell)
                    assigned_nodes.add(last_updated_cell)

                    print("last updated cell: ", last_updated_cell)
                    # TODO: some sort of logic for changing node color or assigning nodes to vehicles
                    mission.grid_graph.graph.nodes[last_updated_cell]['weight'] = 1 + 0.1 * k;
                    f[k] = f[k] - 1
                    N = N - 1
                    print("K = ", k)









# Create UxV obejects to be added as nodes
uxv1 = UxV(name="alpha", position=(5,15), speed=(10), sensorRange=(10), type="UUV", endurance=200)
uxv2 = UxV(name="bravo", position=(35,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv3 = UxV(name="Charlie", position=(15,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
grid_data = genGrid(75, 50, 92)
mission_3 = MissionArea("Misison3", grid_data, 10)
mission_3.add_vehicle_to_graph(uxv1)
mission_3.add_vehicle_to_graph(uxv2)
mission_3.add_vehicle_to_graph(uxv3)
print(mission_3.grid_graph.graph[(uxv3.position)])

# Optimal number of tasks for vehicle rk
print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv1.position))
print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv2.position))
print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv3.position))


pk = [calculate_pk(mission_3, uxv1.position), calculate_pk(mission_3, uxv2.position), calculate_pk(mission_3, uxv3.position)]
pk = [int(x) + 1 for x in pk]
# print(pk)
# print("GCG", gcd_of_list(pk))
for vehicle in mission_3.vehicles:
    mission_3.vehicle_assignments[vehicle] = []
cylcic_region_growth(mission_3, mission_3.vehicles, pk)



mission_3.draw()

plt.show()





