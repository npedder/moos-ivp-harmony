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
        summation_v_k += velocity_k

    p_k = (velocity_r / summation_v_k) * w(mission)

    return p_k


def w(mission: MissionArea):  # would only work if all cells are the same size?
    V = mission.grid_graph.graph.number_of_nodes()
    print("Total number of nodes: ", V)
    summation_node_weights = V #* mission.cellDimension # just assumes that each cell is same size

    return summation_node_weights

def gcd_of_list(numList):
    gcd = math.gcd(numList[0], numList[1])
    for i in range(2, len(numList)):
        gcd = math.gcd(gcd, numList[i])
        print("GCD: ", gcd)

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

        print("NVK ", NV_K)

    return NV_K



def cylcic_region_growth(mission: MissionArea, R, OptimalTasks):
    assigned_nodes = set() # not sure if this is right
    N = mission.grid_graph.graph.number_of_nodes()
    rate = [0] * len(R)
    NV_k = [0] * len(R) # The set of each robot's adjacent unassigned tasks, separated by lists
    f = [0] * len(R) # each robot's capital (optimal number of tasks
    for i in range(len(R)):
        f[i] = OptimalTasks[i]
        rate[i] = int(OptimalTasks[i]/gcd_of_list(OptimalTasks))
        print(OptimalTasks[i])
        print(list(mission.grid_graph.graph[R[i]].keys()))
        NV_k[i] = set((mission.grid_graph.graph[R[i]].keys()))


    last_updated_cell = 0;
    while (N > (len(R))):  #TODO: this is len R because the once the last nodes are updated, the if statement is not triggered to N-1 again.
        for k in range(0, len(R)):
            print("-----------------------------------", "K = ", k)
            for j in range(0, rate[k]):
                for n in range(0,len(R)): # Update NV_K
                    NV_k[n] = update_NV_K(mission, NV_k[n], n, last_updated_cell, assigned_nodes)
                if NV_k[k]: #Checks if list of NVs are empty
                    last_updated_cell =  list(NV_k[k])[0] # select a cell from NV_k
                    mission.vehicle_assignments[mission.vehicles[k]].append(last_updated_cell)
                    assigned_nodes.add(last_updated_cell)
                    print("last updated cell: ", last_updated_cell)
                    mission.grid_graph.graph.nodes[last_updated_cell]['weight'] = 1 + 0.1 * k;
                    f[k] = f[k] - 1
                    N = N - 1
                    print("N = ", N)

    #return f




def region_fine_tuning(mission: MissionArea, f):
    print("none")





# Create UxV obejects to be added as nint odes
uxv1 = UxV(name="alpha", position=(5,15), speed=(10), sensorRange=(10), type="UUV", endurance=200)
uxv2 = UxV(name="bravo", position=(35,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv3 = UxV(name="Charlie", position=(155,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv4 = UxV(name="Delta", position=(315, 345), speed=(20), sensorRange=(15), type="UUV", endurance=100)


grid_data = genConnectedGrid(75, 50, .2, 5) #Generate a random 2D numpy array to represent mission area
mission_3 = MissionArea("Misison3", grid_data, 10)
mission_3.add_vehicle_to_graph(uxv1)
mission_3.add_vehicle_to_graph(uxv2)
mission_3.add_vehicle_to_graph(uxv3)
mission_3.add_vehicle_to_graph(uxv4)



# Optimal number of tasks for vehicle rk
print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv1.position))
print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv2.position))
print("Optimal number of nodes for ", uxv3.name, ": " ,calculate_pk(mission_3, uxv3.position))


pk = [calculate_pk(mission_3, uxv1.position), calculate_pk(mission_3, uxv2.position), calculate_pk(mission_3, uxv3.position), calculate_pk(mission_3, uxv4.position)]
pk = [int(x) + 1 for x in pk]
# print(pk)
# print("GCG", gcd_of_list(pk))
for vehicle in mission_3.vehicles:
    mission_3.vehicle_assignments[vehicle] = []

cylcic_region_growth(mission_3, mission_3.vehicles, pk)


mission_3.draw()

plt.show()





