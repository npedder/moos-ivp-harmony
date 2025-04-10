from MissionArea import MissionArea
import networkx as nx
from collections import deque
from cellDecomposition import group_by_x, _add_node_and_update_pos

# Input: MissionArea
# Combines cells to account for the sensor range of a vehicle. Done after assignments and cell decomposition
# TODO: Sometimes a pass can have 3 nodes connected
def sensor_range_decomposition(mission: MissionArea):
        new_graph = nx.Graph()
        new_pos = {}
        new_vehicle_assignments = {}
        combined_nodes = set()
        for vehicle in mission.vehicles:
                remaining_nodes = set(mission.vehicle_assignments[vehicle])
                new_vehicle_assignments[vehicle] = []
                while remaining_nodes:
                        start_node = _find_leftmost_node(remaining_nodes)
                        # Find the extremes. The average of the x vals and extremes of y vals will be used for new top and bottom
                        largest_x, smallest_x, largest_y, smallest_y, combined_nodes = _bfs_combine_bordering_cells(mission, vehicle, start_node, combined_nodes)

                        new_x = int((largest_x + smallest_x)/2)

                        top_cell = (new_x, largest_y)
                        bottom_cell = (new_x, smallest_y)

                        if top_cell not in new_graph.nodes() and bottom_cell not in new_graph.nodes(): # TODO: bandaid fix to problem with more than top and bottom in a cell

                                _add_node_and_update_pos(new_graph, new_pos, top_cell)
                                _add_node_and_update_pos(new_graph, new_pos, bottom_cell)

                                if top_cell[1] != bottom_cell[1]:
                                        new_graph.add_edge(top_cell, bottom_cell)

                                remaining_nodes.difference_update(combined_nodes)

                                new_vehicle_assignments[vehicle].append(top_cell)

                                if bottom_cell != top_cell: new_vehicle_assignments[vehicle].append(bottom_cell)


        mission.grid_graph.graph = new_graph
        mission.grid_graph.pos = new_pos
        mission.vehicle_assignments = new_vehicle_assignments

        for vehicle in mission.vehicles:
                _add_node_and_update_pos(mission.grid_graph.graph, mission.grid_graph.pos, mission.original_positions[vehicle])









# BFS combine neighboring cells according to sensor range
# Only combines nodes to the right.
def _bfs_combine_bordering_cells(mission: MissionArea, region, start_node, combined_cells):
        graph = mission.grid_graph.graph
        sensor_radius = graph.nodes[region]["sensorRange"]  # Gets sensor range of the vehicle assigned to the region
        queue = deque([start_node])

        largest_x = start_node[0]
        largest_y = graph.nodes[start_node]["top"][1]
        smallest_x = start_node[0]
        smallest_y = graph.nodes[start_node]["bottom"][1]
        combined_cells = combined_cells # The cells that are visited that wont be visited again
        visited = set()

        while queue:
                node = queue.popleft()

                # if node in mission.vehicles: visited.add(node)  # Ignore vehicles TODO: This may not work if vehicle is in center of cell
                if node not in mission.vehicle_assignments[region]: visited.add(node)  # ignore if not in same region
                if node in combined_cells: visited.add(node)

                if node not in visited:
                        visited.add(node)
                        # Track width of cell
                        if node[0] - start_node[0] >= sensor_radius * 2:  # cell is out of sensor range
                                cellTooLarge = True
                        else: cellTooLarge = False

                        if node[0] < start_node[0]: # cell is to the left of prev
                                cellToTheLeft = True
                        else: cellToTheLeft = False

                        # If cell not to wide
                        if not cellTooLarge and not cellToTheLeft:
                                # Check for extremes
                                if node[0] > largest_x:
                                        largest_x = node[0]
                                if node[0] < smallest_x:
                                        smallest_x = node[0]
                                if graph.nodes[node]["top"][1] > largest_y:
                                        largest_y = graph.nodes[node]["top"][1]
                                if graph.nodes[node]["bottom"][1] < smallest_y:
                                        smallest_y = graph.nodes[node]["bottom"][1]

                                # Keep track of cells to remove
                                combined_cells.add(node)

                                #Continue search
                                queue.extend(graph[node])  # Enqueue all adjacent nodes






        return largest_x, smallest_x, largest_y, smallest_y, combined_cells








# Find leftmost node in region to start decomposition
def _find_leftmost_node(nodes):
        sorted_nodes = sorted(nodes, key=lambda x: x[0])
        return sorted_nodes[0]

def _add_node_and_update_pos(cell_graph, pos, node):
    cell_graph.add_node(node)
    pos[node] = node

