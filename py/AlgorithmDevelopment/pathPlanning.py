import networkx
from networkx.algorithms import approximation as approx

from MissionArea import MissionArea
import math
import networkx as nx


# To be done after sensor range decomposition.
def calculate_vehicle_paths(mission: MissionArea):
    vehicle_paths = {}   # Key: vehicle name. Value: list of nodes in order of traversal TODO: not vehicle name yet


    for vehicle in mission.vehicles:
        vehicle_sorted_nodes = sort_by_x_then_y(list(mission.vehicle_assignments[vehicle]))
        vehicle_entrance_exit_pairs = {}  # Each entry node has a corresponding exit node
        vehicle_graph = nx.DiGraph()

        vehicle_graph.add_node(mission.original_positions[vehicle])
        vehicle_entrance_exit_pairs[mission.original_positions[vehicle]] = mission.original_positions[vehicle]

        # Loop to determine whether pass is up or down
        last_x = None
        topIsEntrance = True # A flag that will determine if node is entrance or exit. Alternates for each pass
        for i, node in enumerate(vehicle_sorted_nodes):
            if node != 0:  # 0 if pose is already determined:
                neighbors = list(mission.grid_graph.graph[node])  # Should be length 1 connecting top and bottom pos
                if len(neighbors) > 1:
                    raise Exception("Error: More than two nodes in group")

                if len(neighbors) == 0:
                    vehicle_entrance_exit_pairs[node] = [node]
                    vehicle_sorted_nodes[vehicle_sorted_nodes.index(node)] = 0
                else:
                    neighbor = neighbors[0]
                    if node[1] > neighbor[1]:
                        top_cell = node
                        bottom_cell = neighbor
                    else:
                        top_cell = neighbor
                        bottom_cell = node

                    if last_x == node[0]:
                        topIsEntrance = not topIsEntrance

                    if topIsEntrance:
                        vehicle_entrance_exit_pairs[top_cell] = bottom_cell
                    else:
                        vehicle_entrance_exit_pairs[bottom_cell] = top_cell


                    topIsEntrance = not topIsEntrance

                    last_x = vehicle_sorted_nodes[i][0]
                    vehicle_sorted_nodes[i] = 0
                    vehicle_sorted_nodes[vehicle_sorted_nodes.index(neighbor)] = 0

        # After determining direction of each pass create a new connected graph with entrance nodes only
        for key in vehicle_entrance_exit_pairs.keys():
            vehicle_graph.add_node(key)

        connect_nodes_in_graph_with_distances(vehicle_graph, vehicle_entrance_exit_pairs)

        # Find the order of traversal
        name_key = [key for key, val in mission.original_positions.items() if isinstance(key, str) and val == mission.original_positions[vehicle]]
        vehicle_paths[name_key[0]] = approx.simulated_annealing_tsp(vehicle_graph, "greedy", source=mission.original_positions[vehicle])
        cost = sum(vehicle_graph[n][nbr]["weight"] for n, nbr in nx.utils.pairwise(vehicle_paths[name_key[0]]))


        # Add exit nodes back in between each entrance node
        # Iterate over the vehicle paths
        index = 1
        while index < len(vehicle_paths[name_key[0]]) - 1:  # Ensure there's always an entrance node to pair with
            entrance_node = vehicle_paths[name_key[0]][index]

            # Insert the exit node after the entrance node
            # TODO: Messy fix, data type changes are required to truly fix
            vehicle_paths[name_key[0]].insert(index + 1, vehicle_entrance_exit_pairs[entrance_node])

            # Move index forward by 2 (because we just added an exit node after the entrance node)
            index += 2

        # del vehicle_paths[vehicle][0]
        print("Path")
        print(vehicle_paths[name_key[0]])
        print("Cost")
        print(cost)


    return vehicle_paths




    # print("Pairs ", vehicle_entrance_exit_pairs)
    # print("Sorted Nodes", vehicle_sorted_nodes)


def sort_by_x_then_y(tuples):
    groups = {}

    # Group tuples by their x-values
    for x, y in tuples:
        groups.setdefault(x, []).append((x, y))

    # Sort x-values and then sort each group by y-value
    sorted_x_values = sorted(groups.keys())
    result = []

    for x in sorted_x_values:
        result.extend(sorted(groups[x], key=lambda t: t[1]))

    return result


def connect_nodes_in_graph_with_distances(G, entrance_exit_pairs):
    nodes = list(G.nodes())  # Get all nodes (which are tuples representing positions)
    num_nodes = len(nodes)

    # Iterate twice, once for exit and entrance directions
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):  # Ensure each pair is processed only once
            x1, y1 = nodes[i]
            x2, y2 = entrance_exit_pairs[nodes[j]]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Euclidean distance
            G.add_edge(nodes[i], nodes[j], weight=distance)

    for i in range(num_nodes- 1, -1, -1):
        for j in range(num_nodes -1, -1, -1):  # Ensure each pair is processed only once
            x1, y1 = nodes[i]
            x2, y2 = entrance_exit_pairs[nodes[j]]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Euclidean distance
            G.add_edge(nodes[i], nodes[j], weight=distance)