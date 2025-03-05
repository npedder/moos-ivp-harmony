from MissionArea import MissionArea
import networkx as nx



# Performs a dfs to remove nodes between two endpoints
# Input: Mission Area
def decomposed_vehicle_assignments():
    pass


def cell_decomposition(mission: MissionArea):
    cell_graph = nx.Graph() # A new graph that will hold a node representing each decomposed cell
    cell_graph_pos = {}
    removed_nodes = set()
    decomposed_vehicle_assignments = {}

    for region in mission.vehicle_assignments:
        decomposed_vehicle_assignments[region] = []
        for node in mission.vehicle_assignments[region]:
            if node not in removed_nodes:
                removed_nodes.add(node)
                nodes_to_combine = [node]
                visited = set()
                highest_node = node
                lowest_node = node
                highest_node, lowest_node = _dfs_combine_nodes(mission.grid_graph.graph, node, visited, nodes_to_combine, highest_node, lowest_node)
                print(" Highest Node: " ,highest_node, "   Lowest Node: ",  lowest_node)

                for cell_node in nodes_to_combine:
                    if cell_node != highest_node and cell_node != lowest_node and cell_node not in mission.vehicles:
                        mission.grid_graph.graph.remove_node(cell_node)
                    removed_nodes.add(cell_node)

                mission.grid_graph.graph.remove_edges_from(list(mission.grid_graph.graph.edges(highest_node)))
                mission.grid_graph.graph.remove_edges_from(list(mission.grid_graph.graph.edges(lowest_node)))

                if highest_node != lowest_node:
                    mission.grid_graph.graph.add_edge(highest_node,lowest_node)

                center_node = (int( (highest_node[0] + lowest_node[0]) / 2), int( (highest_node[1] + lowest_node[1]) / 2))
                add_node_and_update_pos(cell_graph, cell_graph_pos, center_node)

                decomposed_vehicle_assignments[region].append(center_node)

    for vehicle in mission.vehicles:
        add_node_and_update_pos(cell_graph,cell_graph_pos,vehicle)

    mission.grid_graph.graph = cell_graph
    mission.grid_graph.pos = cell_graph_pos
    mission.vehicle_assignments = decomposed_vehicle_assignments


    # nx.draw(cell_graph, pos=cell_graph_pos,
    #         with_labels=False,
    #         node_color= 'pink',
    #         edge_color="black",
    #         node_size= 50,
    #         font_color='yellow')







# DFC that returns the two endpoints for a cell. The nodes in between the endpoints will be removed.
def _dfs_combine_nodes(graph, node, visited, nodes_to_combine, highest_node, lowest_node):
    if node not in visited:
        visited.add(node)
        if node[0] == nodes_to_combine[0][0]: # If same X value
            if node != nodes_to_combine[0]:
                nodes_to_combine.append(node) # Don't append start node again
            if node[1] > highest_node[1]:
                highest_node = node
            if node[1] < lowest_node[1]:
                lowest_node = node
            for neighbor in list(graph[node]):
                highest_node, lowest_node = _dfs_combine_nodes(graph, neighbor, visited, nodes_to_combine, highest_node, lowest_node)

    return highest_node, lowest_node


def add_node_and_update_pos(cell_graph, pos, node):
    cell_graph.add_node(node)
    pos[node] = node

