import MissionArea

# Pre-condition: A mission area, the number of iterations the fine tuning should run for, and the account balances
#                for the vehicles/regions
# Post-condition: Updates mission area with new regions which should more closely reflect optimal vehicle assignments
def region_fine_tuning (mission, iterations, account_balances):
    print("Enter region fine tuning")
    i = iterations
    untradeablePairs = dict() # set of two regions to a value true
    while(i > 0):
        # Region with the highest balance is set to be the buyer
        # Out of neighbors of the buyer, the one with the most debt will be the seller
        buyer = max(range(len(account_balances)), key=lambda index: account_balances[index])
        regionNeighborNodes = find_neighbor_nodes(mission)
        seller_key = min(regionNeighborNodes[buyer], key=lambda node_key: account_balances[mission.grid_graph.graph.nodes[node_key]['region']])
        seller = mission.grid_graph.graph.nodes[seller_key]['region']
  
        # Find tasks to trade and update vehicle assignments
        keptNodes = find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, untradeablePairs)
        mission.vehicle_assignments[mission.vehicles[buyer]] =  mission.vehicle_assignments[mission.vehicles[buyer]].union(mission.vehicle_assignments[mission.vehicles[seller]]) - keptNodes
        mission.vehicle_assignments[mission.vehicles[seller]] = keptNodes

        print(str(account_balances))
        print(str(buyer) + " is the buyer with a balance of: " + str(account_balances[buyer]))
        print(str(seller) + " is the seller with a balance of: " + str(account_balances[seller]))
        i = i - 1

# Pre-condition: Receives mission area, the buyer region, and the seller region
# Post-condition: Returns the subtree that when kept by the seller region, leads to an ideal transaction,
#                 otherwise if no trees are found that lead to an ideal transaction, no trade occurs and pair is marked
#                 untradeable for some amount of iterations
def find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, untradeablePairs) :
    print("Entering finding kept nodes")
    # Largest cell in the set of buyer that belongs to the seller is selected for candidate trade
    # AC
    buyerNeighborsInSeller = regionNeighborNodes[buyer].intersection(mission.vehicle_assignments[mission.vehicles[seller]])

    sellerRegionSubgraph = mission.grid_graph.graph.subgraph(mission.vehicle_assignments[mission.vehicles[seller]])
    buyerRegionSubgraph = mission.grid_graph.graph.subgraph(mission.vehicle_assignments[mission.vehicles[buyer]])

    if not buyerNeighborsInSeller:
        # return empty and mark the pair as untradable
        print("Pairs are untradeable")
        # print("AC candidates in seller: " + str(buyerNeighborsInSeller))
        # print("Buyer neigbors: " + str(regionNeighborNodes[buyer] ))
        # print("Seller cells: " + str(set(mission.vehicle_assignments[mission.vehicles[seller]])))
        untradeablePairs[(buyer, seller)] = True
        return mission.vehicle_assignments[mission.vehicles[seller]]
    
    largest_weight = -1
    for node_key in buyerNeighborsInSeller:
        node_data = mission.grid_graph.graph.nodes[node_key]
        # print("Weight of neighbor " + str(node_key) + "is " + str(node_data['weight']))
        if node_data['weight'] > largest_weight:
            largest_weight = node_data['weight']
            largest_weight_node = node_key

    candidate = largest_weight_node

    # Determine if candidate is the cut point
    isCutPoint = False
    
    for neighbor_key in sellerRegionSubgraph[candidate]:
        neighbor_data = mission.grid_graph.graph.nodes[neighbor_key]
        # Check if the neighbor's only connection to the rest of the region is through the cut point
        for neighborNeighbor_key in mission.grid_graph.graph[neighbor_key]:
            neighborNeighbor_data = node_data = mission.grid_graph.graph.nodes[neighborNeighbor_key]
            # If the neighbor does not have a have another neighbor in the seller region that isn't the candidate
            # then the candidate is the cut point and turn is cut point to true
            if neighborNeighbor_data['region'] == neighbor_data['region'] and neighborNeighbor_key != neighbor_key:
                isCutPoint = False 
    
    if isCutPoint:
        print("Candidate is the cut point, searching q subtrees")
        return find_q_subtrees(candidate, mission, buyer, seller, account_balances, sellerRegionSubgraph)
    else:
        print("Candidate is not the cut point, using candidate as trade")
        print("Candidate weight: " + str(mission.grid_graph.graph.nodes[candidate]['weight']))
        account_balances[buyer] = account_balances[buyer] - mission.grid_graph.graph.nodes[candidate]['weight']
        account_balances[seller] = account_balances[seller] + mission.grid_graph.graph.nodes[candidate]['weight']
        return mission.vehicle_assignments[mission.vehicles[seller]] - {candidate}

def find_q_subtrees(candidate, mission, buyer, seller, account_balances, sellerRegionSubgraph):
    print("Node: " + str(candidate) + " is chosen as the root for q-subtrees checking")
    stack = [candidate]
    visited = set()
    bestTradeIndex = float('inf') # Set to high number to start

    # DFS Traversal of all subtrees from the selected root node to determine the best trade
    # ** NOTE ** Avoids loops by using a visited node
    while stack:
        node = stack.pop()
        print("Searching all subtrees from root node: " + str(node))
        # print("Visiting node: " + str(node))
        if node not in visited:
            visited.add(node)
        
        candidateTrade = mission.vehicle_assignments[mission.vehicles[seller]] - visited
        tradeSum = sum_weights(mission, candidateTrade)
        currTradeIndex = max(abs(buyer - tradeSum), abs(seller + tradeSum))
        
        if currTradeIndex < bestTradeIndex:
            print("The current trade index: " + str(currTradeIndex) + " is less than the best trade index: "
            + str(bestTradeIndex))
            print("Thus current trade is the new best trade.")
            bestTradeIndex = currTradeIndex
            bestTrade = candidateTrade
        else:
            print("Candidate trade is not better than best trade")

        # print("Neighbor nodes: " + str(regionSubgraph[node]))
        for neighbor in sellerRegionSubgraph[node]:
            # print("Appending node: " + str(neighbor))
            if neighbor not in visited:
                stack.append(neighbor)
        # print("Seller nodes: " + str(set(mission.vehicle_assignments[mission.vehicles[seller]])))

    account_balances[buyer] = account_balances[buyer] - bestTradeIndex
    account_balances[seller] = account_balances[seller] + bestTradeIndex
    print("Leaving finding kept nodes")
    return bestTrade



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

# Pre-condition: Takes a mission graph, and set of nodes to sum in the graph
# Post-condition: Sums nodes and returns sum
def sum_weights(mission, graph):
    weightSum = sum(graph, key=lambda node_key: mission.grid_graph.graph.nodes[node_key]['weight'])
    return weightSum
