import MissionArea
from collections import defaultdict
import heapq

# Pre-condition: A mission area, the number of iterations the fine tuning should run for, and the account balances
#                for the vehicles/regions
# Post-condition: Updates mission area with new regions which should more closely reflect optimal vehicle assignments
def region_fine_tuning (mission, iterations, account_balances):
    graph = mission.grid_graph.graph
    i = iterations
    pairsTimeOut = dict() # frozen set of two regions to a counter for how many turns they are in time out (if untradeable)

    regionNeighborNodes = find_neighbor_nodes(mission)
    while(i > 0):
        # Select buyer and seller
        pairFound = False
        kthBestBuyer = 1 # Increase to get next largest
        kthBestSeller = 1 # Increase to get next smallest

        # Update timeouts each iteration
        for pair in pairsTimeOut.keys():
            if pairsTimeOut[pair] > 0:
                pairsTimeOut[pair] -= 1

        print("Selecting seller and buyer...")
        while pairFound == False:
            buyer = heapq.nlargest(kthBestBuyer, range(len(account_balances)), key=lambda i: account_balances[i])[-1]
            sellerKey = heapq.nsmallest(kthBestSeller, regionNeighborNodes[buyer], key=lambda node_key: account_balances[graph.nodes[node_key]['region']])[-1]
            seller = graph.nodes[sellerKey]['region']
            try:
                tradeable = pairsTimeOut[frozenset({buyer, seller})] == 0
            except KeyError:
                tradeable = True
            if tradeable == False:
                print("Pair is on timeout, searhcing for next best pair")
            if tradeable:
                pairFound = True
                print("Seller and buyer successfully found")
            else: 
                if kthBestBuyer == kthBestSeller:
                    kthBestBuyer += 1
                else: 
                    kthBestSeller += 1
        print("================================================")
        # Find tasks to trade and update vehicle assignments
        keptNodes = find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, pairsTimeOut)
        mission.vehicle_assignments[mission.vehicles[buyer]] =  mission.vehicle_assignments[mission.vehicles[buyer]].union(mission.vehicle_assignments[mission.vehicles[seller]]) - keptNodes
        mission.vehicle_assignments[mission.vehicles[seller]] = keptNodes

        # Update regions post trade
        for node_key in mission.vehicle_assignments[mission.vehicles[seller]]:
            graph.nodes[node_key]['region'] = seller
        for node_key in mission.vehicle_assignments[mission.vehicles[buyer]]:
            graph.nodes[node_key]['region'] = buyer

        # Update neighbors
        tradedNodes = mission.vehicle_assignments[mission.vehicles[seller]] - keptNodes
        regionNeighborNodes[buyer] = regionNeighborNodes[buyer] - tradedNodes
        
        buyerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[buyer]])
        for node_key in buyerRegionSubgraph:
            node_data = graph.nodes[node_key]
            for neighbor_key in graph[node_key]:
                neighbor_data = graph.nodes[neighbor_key]
                if neighbor_data['region'] != node_data['region']:
                    # if neighbor_key not in regionNeighborNodes[buyer]:
                    #     print("New region neighbor found: " + str(neighbor_key))
                    regionNeighborNodes[node_data['region']].add(neighbor_key)

        sellerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[seller]])
        for node_key in sellerRegionSubgraph:
            node_data = graph.nodes[node_key]
            for neighbor_key in graph[node_key]:
                neighbor_data = graph.nodes[neighbor_key]
                if neighbor_data['region'] != node_data['region']:
                    regionNeighborNodes[node_data['region']].add(neighbor_key)

        print(str(account_balances))
        print(str(buyer) + " is the buyer with a balance of: " + str(account_balances[buyer]))
        print(str(seller) + " is the seller with a balance of: " + str(account_balances[seller]))
        i = i - 1

# Pre-condition: Receives mission area, the buyer region, and the seller region
# Post-condition: Returns the subtree that when kept by the seller region, leads to an ideal transaction,
#                 otherwise if no trees are found that lead to an ideal transaction, no trade occurs and pair is marked
#                 untradeable for some amount of iterations
def find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, pairsTimeOut) :
    graph = mission.grid_graph.graph
    print("Entering finding kept nodes")
    # Largest cell in the set of buyer that belongs to the seller is selected for candidate trade
    # AC
    buyerNeighborsInSeller = regionNeighborNodes[buyer].intersection(mission.vehicle_assignments[mission.vehicles[seller]])
    # print("Buyer's neighbor nodes: " + str(regionNeighborNodes[buyer]))

    sellerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[seller]])
    buyerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[buyer]])

    if not buyerNeighborsInSeller:
        # return empty and mark the pair as untradable
        print("Pairs are untradeable")
        pairsTimeOut[frozenset({buyer, seller})] = 3
        return mission.vehicle_assignments[mission.vehicles[seller]]
    
    largest_weight_node = max(buyerNeighborsInSeller, key=lambda node_key: graph.nodes[node_key]['weight'])
    candidate = largest_weight_node

    # Determine if candidate is the cut point
    # Pick a neighbor of the candidate that is in the seller's region. Treat candidate as traded, then search all nodes in the region, if visited
    # matches seller - candidate, then it's not a cut point, otherwise it is

    # grab candidate neighbor in the sell graph
    start = None
    for e in sellerRegionSubgraph[candidate]:
        start = e
        break

    print("Starting point: " + str(start))
    print("Candidate: " + str(candidate))

    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        visited.add(node)
        for neighbor in sellerRegionSubgraph[node]:
            if neighbor not in visited and neighbor != candidate:
                stack.append(neighbor)

    # print("Nodes visited: " + str(visited))
    # print("Seller assignments " + str(mission.vehicle_assignments[mission.vehicles[seller]]))

    if mission.vehicle_assignments[mission.vehicles[seller]] - {candidate} == visited:
        isCutPoint = False
    else:
        isCutPoint = True
    
    if isCutPoint:
        print("Candidate is the cut point, searching q subtrees")
        return find_q_subtrees(candidate, mission, buyer, seller, account_balances, sellerRegionSubgraph, pairsTimeOut)
    else:
        print("Candidate is not the cut point, using candidate as trade")
        print("Candidate weight: " + str(graph.nodes[candidate]['weight']))
        account_balances[buyer] = account_balances[buyer] - graph.nodes[candidate]['weight']
        account_balances[seller] = account_balances[seller] + graph.nodes[candidate]['weight']
        return mission.vehicle_assignments[mission.vehicles[seller]] - {candidate}

def find_q_subtrees(candidate, mission, buyer, seller, account_balances, sellerRegionSubgraph, pairsTimeOut):
    print("========================================================")

    bestTradeIndex = float('inf')
    bestTradeSum = 0
    bestTrade = {}

    for neighbor in sellerRegionSubgraph[candidate]:
        stack = [neighbor]
        visited = set()
        # DFS Traversal of all subtrees from the selected root node to determine the best trade
        # ** NOTE ** Avoids loops by using a visited node
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
            for neighbor in sellerRegionSubgraph[node]:
                if neighbor not in visited and neighbor != candidate:
                    stack.append(neighbor)

        candidateTrade = mission.vehicle_assignments[mission.vehicles[seller]] - visited
        tradeSum = sum_weights(mission, candidateTrade)
        currTradeIndex = max(abs(account_balances[buyer] - tradeSum), abs(account_balances[seller] + tradeSum))
        if currTradeIndex < bestTradeIndex:
            print("The current trade index: " + str(currTradeIndex) + " is less than the best trade index: "
            + str(bestTradeIndex))
            print("Thus current trade is the new best trade.")
            print("Buyer's balance: " + str(account_balances[buyer] - tradeSum))
            print("Seller's balance: " + str(account_balances[seller] + tradeSum))
            print("Trade sum: " + str(tradeSum))
            bestTradeIndex = currTradeIndex
            bestTradeSum = tradeSum
            bestTrade = visited.copy()
        else:
            print("Candidate trade is not better than best trade")
            print("Buyer's balance would have been: " + str(account_balances[buyer] - tradeSum))
            print("Seller's balance would have been: " + str(account_balances[seller] + tradeSum))
            print("Trade sum: " + str(tradeSum))

    if max(abs(account_balances[buyer]), abs(account_balances[seller])) < bestTradeIndex:
        # mark pair as untradeable for 3 turns
        pairsTimeOut[frozenset({buyer, seller})] = 3
        # Don't make the trade
        print("No available trades are better, trading nothing and moving on")
        print("=============================================================")
        return mission.vehicle_assignments[mission.vehicles[seller]]

    account_balances[buyer] = account_balances[buyer] - bestTradeSum
    account_balances[seller] = account_balances[seller] + bestTradeSum
    print("Trading " + str(bestTradeSum) + " from the seller to the buyer")
    print("=============================================================")
    return bestTrade



# Pre-condition: A mission area
# Post-condtion: Returns a dictionary mapping an integer representing region to a set of nodes that neighbor that region
def find_neighbor_nodes (mission: MissionArea):
    graph = mission.grid_graph.graph
    print("Entering findNeighborNodes")
    # initalize a dictionary of empty sets for holding the neighbors of each region
    regionNeighborNodes = {key: set() for key in range(len(mission.vehicles))}
    # Iterate through the keys of each node and then the keys of that node's neighbors
    for node_key in graph.nodes:
        node_data = graph.nodes[node_key]
        for neighbor_key in graph[node_key]:
            neighbor_data = graph.nodes[neighbor_key]
            if neighbor_data['region'] != node_data['region']:
                 regionNeighborNodes[node_data['region']].add(neighbor_key)
    return regionNeighborNodes

def sum_weights(mission, subgraph):
    print("\tCalculating weight sum...")
    graph = mission.grid_graph.graph
    weightSum = 0
    for node_key in subgraph:
        node_data = graph.nodes[node_key]
        weightSum += node_data['weight']
        # print("\t" + str(node_data['weight']) + " + ", end="")
    print("\n\t" + str(weightSum))
    return weightSum
