from MissionArea import MissionArea
import networkx as nx



# Performs a dfs to remove nodes between two endpoints. Replaces mission.grid.grid_graph with a list of nodes representing
# the decomposed cells. Each cell has a  "top" and "bottom" attribute, keeping track of the endpoints.
# Input: Mission Area


def cell_decomposition(mission: MissionArea):
    vehicle_node_objects = [mission.grid_graph.graph.nodes(v) for v in mission.vehicles] #get vehicles and data

    cell_graph = nx.Graph() # A new graph that will hold a node representing each decomposed cell
    cell_graph_pos = {}
    removed_nodes = set()
    center_nodes_old_neighbors = {} # A dictionary with key center cell and value of neighbors before decomp. Can be used to determine bordering nodes

    # for region in mission.vehicle_assignments:
    #     decomposed_vehicle_assignments[region] = []
    for node in mission.grid_graph.graph.nodes:
        vehicles_in_cell = []
        if node not in removed_nodes:
            removed_nodes.add(node)
            nodes_to_combine = [node]
            visited = set()
            highest_node = node
            lowest_node = node
            highest_node, lowest_node = _dfs_combine_nodes(mission.grid_graph.graph, node, visited, nodes_to_combine, highest_node, lowest_node)
            print(" Highest Node: " ,highest_node, "   Lowest Node: ",  lowest_node)

            # Add a node in new graph representing a decomposed cell
            center_node = (int((highest_node[0] + lowest_node[0]) / 2), int((highest_node[1] + lowest_node[1]) / 2))
            _add_node_and_update_pos(cell_graph, cell_graph_pos, center_node)

            center_nodes_old_neighbors[center_node] = set()
            # Track the neighbors of the nodes in to be combined. Add nodes to be removed/visited
            weight = 0
            for cell_node in nodes_to_combine:
                weight += 1     # The amount of nodes to be combined will be the weight of the cell
                if cell_node in mission.vehicles:
                    vehicles_in_cell.append(cell_node)

                # Check if a vehicle is attached but x is not normalized to grid
                # for neighbor in list(mission.grid_graph.graph[cell_node]):
                #     if neighbor in mission.vehicles and mission.grid_graph.graph.nodes[neighbor]["displacement"] != 0:
                #         vehicles_in_cell.append(neighbor)

                center_nodes_old_neighbors[center_node].update(set(mission.grid_graph.graph[cell_node]))
                removed_nodes.add(cell_node)

            # Assign weight of cell
            cell_graph.nodes[center_node]["weight"] = weight


            # mission.grid_graph.graph.remove_edges_from(list(mission.grid_graph.graph.edges(highest_node)))
            # mission.grid_graph.graph.remove_edges_from(list(mission.grid_graph.graph.edges(lowest_node)))

            # Add an edge between highest_node and lowest node. TODO: this does not matter as of now.
            if highest_node != lowest_node:
                mission.grid_graph.graph.add_edge(highest_node, lowest_node)

            # Keep track of top and bottom of cells to determine bordering cells
            cell_graph.nodes[center_node]['top'] = highest_node
            cell_graph.nodes[center_node]['bottom'] = lowest_node



            # Add vehicle node and make an edge between the vehicle and the cell containing it
            for vehicle in vehicles_in_cell:
                #_add_node_and_update_pos(cell_graph, cell_graph_pos, vehicle)
                # Center node becomes new vehicle start location
                cell_graph.nodes[center_node].update(mission.grid_graph.graph.nodes[vehicle])  # Transfer attributes to center node
                cell_graph.nodes[center_node]['region'] = center_node
                mission.vehicles[mission.vehicles.index(vehicle)] = center_node
                mission.vehicle_assignments[center_node] = mission.vehicle_assignments.pop(vehicle)
                mission.vehicle_assignments[center_node].append(center_node)


    center_nodes_grouped_by_x = group_by_x(set(cell_graph.nodes).difference(set(mission.vehicles))) # Makes it easier to find bordering cells
    distance_between_nodes = mission.cellDimension
    # Create edges between bordering cells.
    for center_node in center_nodes_old_neighbors:
        for neighbor in center_nodes_old_neighbors[center_node]:
            # Get all cells to left and right of target
            left_x = center_node[0] - distance_between_nodes
            right_x = center_node[0] + distance_between_nodes
            if left_x in center_nodes_grouped_by_x.keys() and right_x in center_nodes_grouped_by_x.keys():
                possible_bordering_cells = center_nodes_grouped_by_x[left_x] + center_nodes_grouped_by_x[right_x]
            elif left_x not in center_nodes_grouped_by_x.keys() and right_x in center_nodes_grouped_by_x.keys():
                possible_bordering_cells = center_nodes_grouped_by_x[right_x]
            elif right_x not in center_nodes_grouped_by_x.keys() and left_x in center_nodes_grouped_by_x.keys():
                possible_bordering_cells = center_nodes_grouped_by_x[left_x]
            else:
                break

            for possible_bordering_cell in possible_bordering_cells:
                if neighbor in center_nodes_old_neighbors[possible_bordering_cell]:
                    cell_graph.add_edge(center_node, possible_bordering_cell)


    # Replace mission graph with new decomposed graph
    mission.grid_graph.graph = cell_graph
    mission.grid_graph.pos = cell_graph_pos

    # for vehicle in mission.vehicles:
    #     _add_node_and_update_pos(cell_graph, cell_graph_pos, normalized_vehicle)
    #mission.vehicle_assignments = decomposed_vehicle_assignments






# DFS that returns the two endpoints for a cell. The nodes in between the endpoints will be removed.
def _dfs_combine_nodes(graph, node, visited, nodes_to_combine, highest_node, lowest_node):
    if node not in visited:
        visited.add(node)
        if node[0] == nodes_to_combine[0][0]: # If same X value as start node
            if node != nodes_to_combine[0]:
                nodes_to_combine.append(node) # Don't append start node again
            if node[1] > highest_node[1]:
                highest_node = node
            if node[1] < lowest_node[1]:
                lowest_node = node
            for neighbor in list(graph[node]):
                highest_node, lowest_node = _dfs_combine_nodes(graph, neighbor, visited, nodes_to_combine, highest_node, lowest_node)

    return highest_node, lowest_node


def _add_node_and_update_pos(cell_graph, pos, node):
    cell_graph.add_node(node)
    pos[node] = node

# Group the cells by their x values. Assists with finding neighboring nods
def group_by_x(tuples):
    groups = {}

    # Group tuples by their x-values
    for x, y in tuples:
        groups.setdefault(x, []).append((x, y))

    # Sort each group by y-value
    for x in groups:
        groups[x].sort(key=lambda t: t[1])

    return groups