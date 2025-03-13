import MissionArea
import math


def cyclic_region_growth(mission: MissionArea):
    R = mission.vehicles
    OptimalTasks = [calculate_optimal_tasks(mission, r) for r in R]  # p_k
    assigned_nodes = set()
    N = mission.grid_graph.graph.number_of_nodes()
    rate = [0] * len(R) # How many times a region will grow before switching off
    NV_k = [0] * len(R) # A list of sets that contain each robot's adjacent unassigned tasks
    account_balances = [0] * len(R) # Each robot's capital

    for i in range(len(R)):
        account_balances[i] = OptimalTasks[i]
        rate[i] = int(OptimalTasks[i]/min(OptimalTasks))
        NV_k[i] = set((mission.grid_graph.graph[R[i]].keys()))

    #print("Total cell weight: " + str(w(mission)))
    #print("Original balances according to capabilities: " + str(account_balances))
    last_updated_cell = 0
    while (N > (len(R))):  # This is len R because the once the last nodes are updated, if statement doesn't N-1 again.
        for k in range(0, len(R)):
            for j in range(0, rate[k]):
                # Update NV_K:
                for n in range(0,len(R)):
                    NV_k[n] = update_NV_K(mission, NV_k[n], n, last_updated_cell, assigned_nodes)
                # Assign nodes
                if NV_k[k]: # Checks if list of NVs are empty
                    last_updated_cell =  list(NV_k[k])[0] # select a cell from NV_k
                    mission.vehicle_assignments[mission.vehicles[k]].append(last_updated_cell)  # Assign selected cell
                    assigned_nodes.add(last_updated_cell)
                    mission.grid_graph.graph.nodes[last_updated_cell]['region'] = k
                    account_balances[k] = account_balances[k] - mission.grid_graph.graph.nodes[last_updated_cell]['weight']
                    N = N - 1
                    # print("Remaining Nodes: ", N - 4)

    return account_balances


def calculate_optimal_tasks(mission: MissionArea, vehicle):
    velocity_r = mission.grid_graph.graph.nodes[vehicle]['speed']
    summation_v_k = 0
    R = mission.vehicles
    for r in R:
        velocity_k = mission.grid_graph.graph.nodes[r]['speed']
        summation_v_k += velocity_k

    p_k = (velocity_r / summation_v_k) * w(mission)

    return int(p_k)


def w(mission: MissionArea):  # TODO: would only work if all cells are the same size?
    V = mission.grid_graph.graph.number_of_nodes()
    # print("Total number of nodes: ", V)
    summation_node_weights = 0
    for node in mission.grid_graph.graph.nodes():
        if node not in mission.vehicles:
            # print("A nodes weight: " + str(mission.grid_graph.graph.nodes[node]["weight"]))
            summation_node_weights += mission.grid_graph.graph.nodes[node]["weight"]

    return summation_node_weights


def gcd_of_list(numList):
    gcd = math.gcd(numList[0], numList[1])
    for i in range(2, len(numList)):
        gcd = math.gcd(gcd, numList[i])
        # print("GCD: ", gcd)

    return gcd


def update_NV_K(mission: MissionArea, NV_K, k, cell, assigned_nodes):
    if cell in NV_K and cell in mission.vehicle_assignments[mission.vehicles[k]]:
        newNodes = set(mission.grid_graph.graph[cell].keys())
        for node in assigned_nodes:
            if node in newNodes:
                newNodes.remove(node)

        for node in mission.vehicles:
            if node in newNodes:
                newNodes.remove(node)

        NV_K.remove(cell)
        NV_K.update(newNodes)

    elif cell in NV_K:
        NV_K.remove(cell)

        # print("NVK ", NV_K)

    return NV_K



