import MissionArea

# Pre-condition: A mission area
# Post-condtion: Returns a dictionary mapping an integer representing region to a set of nodes that neighbor that region
def find_neighbor_nodes (mission: MissionArea):
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

# Pre-condition: A mission area, the number of iterations the fine tuning should run for, and the account balances
#                for the vehicles/regions
# Post-condition: Updates mission area with new regions which should more closely reflect optimal vehicle assignments
#
# **NOTE** This implementation is derived from the CDM and EDM paper ("Exact and Heuristic Multi-Robot Dubins Coverage Path Planning for Known Environments")
#          and is NOT derived from the psuedocode from the paper we used ("Complete Coverage Problem of Multiple Robots with Different Velocities".)

def region_fine_tuning (mission, iterations, account_balances):
    i = iterations
    while(i > 0):
        # Region with the highest balance is set to be the buyer
        largestAccountBal = account_balances[0]
        for j in range(len(account_balances) - 1):
            if account_balances[j] > largestAccountBal:
                largestAccountBal = account_balances[j]
        buyer = j

        # Out of neighbors of the buyer, the one with the most debt will be the seller
        regionNeighborNodes = find_neighbor_nodes(mission)
        smallestAccountBal = account_balances[0]
        smallestAccountBalNode = regionNeighborNodes[0]
        for node_key in regionNeighborNodes[buyer]:
            node_data = mission.grid_graph.graph.nodes[node_key]
            if account_balances[node_data['region']] < smallestAccountBal:   
                smallestAccountBal = account_balances[node_data['region']]
                smallestAccountBalNode = node_data
        seller = smallestAccountBalNode['region']

        # Determine what is kept and what is sold     
        keptNodes = find_kept_nodes(mission, buyer, seller, account_balances)
        mission.vehicleAssignment[buyer] = mission.vehicleAssignments[seller] - keptNodes
        mission.vehicleAssignments[seller] = keptNodes

        i = i - 1

    print(str(account_balances))
    print(str(buyer) + " is the buyer with a balance of: " + str(account_balances[buyer]))
    print(str(seller) + " is the seller with a balance of: " + str(account_balances[seller]))


# Pre-condition: Receives mission area, the buyer region, and the seller region
# Post-condition: Returns the subtree that when kept by the seller region, leads to an ideal transaction,
#                 otherwise if no trees are found that lead to an ideal transaction, -1 is returned (for now)
def find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances) :
    print("Begin finding kept nodes")

    # Largest cell in the set of buyer that belongs to the seller is selected for candidate trade
    # AC
    sellerNeighborsToBuyer = regionNeighborNodes[buyer].intersection(mission.vehicle_assignments[seller])
    
    largest_weight = -1
    for node_key in sellerNeighborsToBuyer:
        node_data = mission.grid_graph.graph.nodes[node_key]
        if node_data['weight'] > largest_weight:
            largest_weight = node_data['weight']
            largest_weight_node = node_key

    candidate = largest_weight_node
    stack = [largest_weight_node]
    visited = set()
    bestTradeIndex = float('inf')

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
        
        candidateTrade = mission.vehicle_assignments[seller] - visited
        tradeSum = sum_weights(candidateTrade)
        currTradeIndex = max(abs(buyer - tradeSum), abs(seller + tradeSum))
        
        if currTradeIndex < bestTradeIndex:
            bestTradeIndex = currTradeIndex

        regionSubgraph = mission.gridGraph.graph.subgraph(mission.vehicleAssignments)
        for neighbor in regionSubgraph[node]:
            if neighbor not in visited:
                stack.push(neighbor)
    
    

# Pre-condition: Takes a mission graph, and set of nodes to sum in the graph
# Post-condition: Sums nodes and returns sum
def sum_weights(mission, graph):
    
    weightSum = 0
    for node_key in graph:
        node_data = mission.grid_graph.graph.nodes[node_key]
        weightSum += node_data['weight']
    return weightSum
    

