import matplotlib.pyplot as plt
import math

from MissionArea import MissionArea
from gridArrayGenerator import genGrid, genConnectedGrid
from UxV import UxV



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
    # print("Total number of nodes: ", V)
    summation_node_weights = V #* mission.cellDimension # just assumes that each cell is same size

    return summation_node_weights

def gcd_of_list(numList):
    gcd = math.gcd(numList[0], numList[1])
    for i in range(2, len(numList)):
        gcd = math.gcd(gcd, numList[i])
        # print("GCD: ", gcd)

    return gcd


def update_NV_K(mission: MissionArea, NV_K, k, cell, assigned_nodes):
    if(cell in NV_K and cell in mission.vehicle_assignments[mission.vehicles[k]]):
        newNodes = set(mission.grid_graph.graph[cell].keys())
        for node in assigned_nodes: # TODO: questionable for statement
            if node in newNodes:
                newNodes.remove(node)

        for node in mission.vehicles: # TODO: questionable for statement probably a better way
            if node in newNodes:
                newNodes.remove(node)

        NV_K.remove(cell)
        NV_K.update(newNodes)

    elif cell in NV_K:
        NV_K.remove(cell)

        # print("NVK ", NV_K)

    return NV_K



def cyclic_region_growth(mission: MissionArea, R, OptimalTasks):
    assigned_nodes = set() # not sure if this is right
    N = mission.grid_graph.graph.number_of_nodes()
    rate = [0] * len(R)
    NV_k = [0] * len(R) # The set of each robot's adjacent unassigned tasks, separated by lists
    f = [0] * len(R) # each robot's capital (optimal number of tasks
    for i in range(len(R)):
        f[i] = OptimalTasks[i]
        rate[i] = int(OptimalTasks[i]/min(OptimalTasks))
        # print(OptimalTasks[i])
        # print(list(mission.grid_graph.graph[R[i]].keys()))
        NV_k[i] = set((mission.grid_graph.graph[R[i]].keys()))


    last_updated_cell = 0
    while (N > len(R)):  #TODO: this is len R because the once the last nodes are updated, the if statement is not triggered to N-1 again.
        for k in range(0, len(R)):
            # print("-----------------------------------", "K = ", k)
            mission.grid_graph.graph.nodes[mission.vehicles[k]]['region'] = k
            for j in range(0, rate[k]):
                for n in range(0,len(R)): # Update NV_K
                    NV_k[n] = update_NV_K(mission, NV_k[n], n, last_updated_cell, assigned_nodes)
                if NV_k[k]: #Checks if list of NVs are empty
                    last_updated_cell =  list(NV_k[k])[0] # select a cell from NV_k
                    mission.vehicle_assignments[mission.vehicles[k]].append(last_updated_cell)
                    assigned_nodes.add(last_updated_cell)
                    # print("last updated cell: ", last_updated_cell)
                    mission.grid_graph.graph.nodes[last_updated_cell]['weight'] = 1 + 0.1 * k
                    mission.grid_graph.graph.nodes[last_updated_cell]['region'] = k
                    f[k] = f[k] - 1
                    N = N - 1
<<<<<<< HEAD
                    print("N = ", N)
                    
max_Inum = input("enter innumeration as the amount of vehicles: ")
=======
                    # print("N = ", N)


# Precondition: A mission area 
# Postcondtion: Returns a dictionary mapping region to a set of nodes
def findNeighborNodes (mission: MissionArea) :   
    print("Entering findNeighborNodes")
    # initalize a dictionary of empty sets for holding the neighbors of each region
    regionNeighborNodes = {key: set() for key in range(len(mission.vehicles))}

    # Iterate through the keys of each node and then the keys of that node's neighbors
    for node_key in dict(mission.grid_graph.graph.nodes).keys(): 
        node_data = mission.grid_graph.graph.nodes[node_key]
        for neighbor_key in dict(mission.grid_graph.graph[node_key]).keys():  
            neighbor_data = mission.grid_graph.graph.nodes[neighbor_key]
            if neighbor_data['region'] != node_data['region']:
                 regionNeighborNodes[node_data['region']].add(neighbor_key)
    return regionNeighborNodes 
>>>>>>> region-bordering

def region_fine_tuning(mission: MissionArea, N_prime, f_prime, V, max_Inum):
    # Step 1: Initialize variables
    N_two_prime = N_prime.copy()
    max_f = max(abs(x) for x in f_prime)
    iter_number = 0
    
    # Step 2: Generate the set of connected cells of K partitions
    BV = {v: set(mission.grid_graph.graph[v]) for v in V}  # BV_k for each vehicle
    
    # Step 3: Iteratively balance task assignments
    while max_f != 0 and iter_number <= max_Inum:
        # Step 4: Identify the partitions with max and min tasks
        start = f_prime.index(max(f_prime))  # Partition with max tasks
        dest = f_prime.index(min(f_prime))  # Partition with min tasks
        
        # Step 6: Generate a path for task exchange using DFS
        path = [start]
        visited = set()
        stack = [start] 
        
        while stack:
            node = stack.pop()
            if node == dest:
                break
            visited.add(node)
            neighbors = BV[node] - visited
            stack.extend(neighbors)
            path.append(node)
        path.append(dest)
        
        # Step 7: Task exchange along the path
        for i in range(1, len(path) - 1):
            cell = next(iter(BV[path[i - 1]]), None)  # Select a cell to move
            if cell is None:
                continue
            
            # Step 9: Assign cell to new partition
            N_two_prime[cell] = path[i]
            
            # Step 10-11: Update BV sets
            BV[path[i - 1]].remove(cell)
            BV[path[i]].add(cell)
        
        # Step 13-14: Update function values
        f_prime[start] -= 1
        f_prime[dest] += 1
        
        # Step 15-16: Update max_f and iteration count
        max_f = max(abs(x) for x in f_prime)
        iter_number += 1
    
    # Step 18: Return the adjusted partitions
    return N_two_prime









# Create UxV obejects to be added as nodes
uxv1 = UxV(name="alpha", position=(5,15), speed=(10), sensorRange=(10), type="UUV", endurance=200)
uxv2 = UxV(name="bravo", position=(35,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv3 = UxV(name="Charlie", position=(155,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv4 = UxV(name="Delta", position=(315, 345), speed=(1), sensorRange=(15), type="UUV", endurance=100)
uxv5 = UxV(name="Elijah", position=(275, 155), speed=(2), sensorRange=(15), type="UUV", endurance=100)

grid_data = genConnectedGrid(75, 50, .2, 5) #Generate a random 2D numpy array to represent mission area
mission_3 = MissionArea("Mission3", grid_data, 10)
mission_3.add_vehicle_to_graph(uxv1)
mission_3.add_vehicle_to_graph(uxv2)
mission_3.add_vehicle_to_graph(uxv3)
mission_3.add_vehicle_to_graph(uxv4)

<<<<<<< HEAD
for vehicle in mission_3.vehicles:
    mission_3.vehicle_assignments[vehicle] = []
=======
>>>>>>> region-bordering

# Optimal number of tasks for vehicle rk
# print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv1.position))
# print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv2.position))
# print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv3.position))


pk = [calculate_pk(mission_3, uxv1.position), calculate_pk(mission_3, uxv2.position), calculate_pk(mission_3, uxv3.position), calculate_pk(mission_3, uxv4.position)]
pk = [int(x) + 1 for x in pk]
f = cylcic_region_growth(mission_3, mission_3.vehicles, pk)
#finalSolution = region_fine_tuning(mission_3, f)
# print(pk)
# print("GCG", gcd_of_list(pk))
<<<<<<< HEAD
=======
for vehicle in mission_3.vehicles:
    mission_3.vehicle_assignments[vehicle] = []
cyclic_region_growth(mission_3, mission_3.vehicles, pk)
>>>>>>> region-bordering

cylcic_region_growth(mission_3, mission_3.vehicles, pk)
region_fine_tuning(mission_3, f, mission_3.vehicles, max_Inum)

# findBorderNodes(mission_3)
for (region, sets) in findNeighborNodes(mission_3).items():
      print("Region: " + str(region) + " Region Neighbors: " + str(sets))
# print(mission_3.grid_graph.graph.nodes[(20, 15)]['region'])
# print(dict(mission_3.grid_graph.graph[5, 15]).keys()) # Get keys of all neighbor nodes of a node
# print(dict(mission_3.grid_graph.graph.nodes).keys()) # Get key of all nodes in the graph
# print(mission_3.grid_graph.graph.nodes[15, 15]['region'])
mission_3.neighbors = findNeighborNodes(mission_3)
mission_3.draw(show_neighbors=True)

plt.show()





