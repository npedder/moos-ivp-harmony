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

    last_updated_cell = 0;
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
                    account_balances[k] = account_balances[k] - mission.grid_graph.graph.nodes[last_updated_cell]["weight"]
                    N = N - 1
                    print("Remaining Nodes: ", N - 4)

    return account_balances


def calculate_optimal_tasks(mission: MissionArea, vehicle):
    mission_numTasks = mission_weight(mission)  # The number of tasks before cell decomposition

    vehicle_displacement = mission.grid_graph.graph.nodes[vehicle]['displacement']
    vehicle_extra_tasks = vehicle_displacement/mission.cellDimension  #  Extra tasks added to total survey, outside the survey
    vehicle_velocity = mission.grid_graph.graph.nodes[vehicle]['speed']
    vehicle_sensor_range = mission.grid_graph.graph.nodes[vehicle]['sensorRange']
    vehicle_coverage_rate = vehicle_velocity * vehicle_sensor_range

    r_coverage_rate_summation = 0
    r_velocity_summation = 0
    total_extra_tasks = 0
    R = mission.vehicles
    for r in R:
        r_displacement = mission.grid_graph.graph.nodes[vehicle]['displacement']
        r_extra_tasks = vehicle_displacement / mission.cellDimension
        r_velocity = mission.grid_graph.graph.nodes[r]['speed']
        r_sensor_range = mission.grid_graph.graph.nodes[r]['sensorRange']
        r_velocity_summation += r_velocity
        r_coverage_rate = r_velocity * r_sensor_range
        total_extra_tasks += r_extra_tasks
        r_coverage_rate_summation += r_coverage_rate


    if total_extra_tasks == 0:
        final_optimal_tasks = (vehicle_coverage_rate / r_coverage_rate_summation) * mission_weight(mission)
    else:
        new_mission_numTasks = mission_numTasks + total_extra_tasks
        extra_included_optimal_tasks = ((vehicle_coverage_rate / r_coverage_rate_summation) * mission_numTasks
                                        + (vehicle_velocity/r_velocity_summation) * new_mission_numTasks)
        final_optimal_tasks = extra_included_optimal_tasks - vehicle_extra_tasks  # Removes the distance needed to reach SA


    return int(final_optimal_tasks)


def mission_weight(mission: MissionArea):
    V = mission.grid_graph.graph.number_of_nodes()
    print("Total number of nodes: ", V)
    summation_node_weights = 0
    for node in mission.grid_graph.graph.nodes():
        if node not in mission.vehicles:
            summation_node_weights += mission.grid_graph.graph.nodes[node]["weight"]

    return summation_node_weights


def gcd_of_list(numList):
    if len(numList) < 2:
        return numList[0]

    gcd = math.gcd(numList[0], numList[1])
    for i in range(2, len(numList)):
        gcd = math.gcd(gcd, numList[i])
        print("GCD: ", gcd)

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

        print("NVK ", NV_K)

    return NV_K



