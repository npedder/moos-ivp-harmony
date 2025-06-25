import networkx as nx

def region_fine_tuning(mission):
    # First form the region graph
    region_neighbor_nodes = find_neighbor_nodes(mission)

    print("Printing through region neighbor nodes...")
    # for (region, node_set) in region_neighbor_nodes.items():
    #     print(f"Region: {str(region)}\nSet:{str(node_set)}")
    print(f"{str(region_neighbor_nodes.items())}")
    # region_graph = form_region_graph(mission, region_neighbor_nodes)
    # print(f" Region graph: {str(region_graph.edges)}")

# Pre-condition: A mission area
# Post-condtion: Returns a dictionary mapping an integer representing region to a set of nodes that neighbor that region
def find_neighbor_nodes (mission):
    graph = mission.grid_graph.graph
    print("Entering findNeighborNodes")
    # initalize a dictionary of empty sets for holding the neighbors of each region
    regionNeighborNodes = {key: set() for key in mission.vehicles}
    # Iterate through the node keys in the graph and then the keys of that node's neighbors\
    print(f"All of the nodes in the graph: {str(graph.nodes)}")
    for node_key in graph.nodes:
        node_data = graph.nodes[node_key]
        for neighbor_key in graph[node_key]:
            neighbor_data = graph.nodes[neighbor_key]
            if neighbor_data['region'] != node_data['region']:
                 print(f"{str(node_data['region'])} has a region neighbor of {str(neighbor_data['region'])}")
                 regionNeighborNodes[node_data['region']].add(neighbor_key)
    return regionNeighborNodes

def form_region_graph(mission, region_neighbor_nodes) :
    print("Forming region graph...")
    mission_graph = mission.grid_graph.graph
    region_graph = nx.Graph()
    for (region, nodeSet) in region_neighbor_nodes.items():
        if region not in region_graph:
            print(f"Adding {region} to the region graph")
            region_graph.add_node(region)
        neighbor_regions = set()
        for node_key in nodeSet:
            node_data = mission_graph.nodes[node_key]
            if node_data['region'] not in neighbor_regions:
                neighbor_regions.add(node_data['region'])
                if node_data['region'] not in region_graph:
                    print(f"Adding {node_data['region']} to the graph")
                    region_graph.add_node(node_data['region'])
                if (region, node_data['region']) not in region_graph.edges():
                    print(f"Adding an egde between {region} and {node_data['region']}") 
                    region_graph.add_edge(region, node_data['region'])    
    return region_graph
# Set of connected regions
    