from AlgorithmDevelopment.MissionArea import MissionArea
from collections import defaultdict
import heapq


# Pre-condition: A mission area, the number of iterations the fine tuning should run for, and the account balances
#                for the vehicles/regions
# Post-condition: Updates mission area with new regions which should more closely reflect optimal vehicle assignments
def region_fine_tuning(mission, iterations, account_balances):
    # Create a map from vehicle to index.
    # Needed because of change of nodes.[node]['region'] from int to tuple
    region_map = {}
    for i, v in enumerate(mission.vehicles):
        region_map[v] = i

    graph = mission.grid_graph.graph
    i = iterations
    pairsTimeOut = dict() # frozen set of two regions to a counter for how many turns they are in time out (if untradeable)
    regionNeighborNodes = find_neighbor_nodes(mission)
    while(i > 0):
        printIteration(i, iterations)
        # Select buyer and seller
        pairFound = False
        kthBestBuyer = 1 # Increase to get next largest
        kthBestSeller = 1 # Increase to get next smallest
        pairCounter = 0
        
        print("Selecting seller and buyer...")
        while pairFound == False and pairCounter < len(account_balances) * len(account_balances):
            pairCounter += 1
            buyer = heapq.nlargest(kthBestBuyer, range(len(account_balances)), key=lambda i: account_balances[i])[-1]
            sellerKey = heapq.nsmallest(kthBestSeller, regionNeighborNodes[mission.vehicles[buyer]], key=lambda node_key: account_balances[region_map[graph.nodes[node_key]['region']]])[-1]
            seller = region_map[graph.nodes[sellerKey]['region']]
            try:
                tradeable = pairsTimeOut[frozenset({buyer, seller})] == 0
            except KeyError:
                tradeable = True
            if tradeable == False:
                print("Pair is on timeout, searhcing for next best pair")
            if tradeable and len(mission.vehicle_assignments[mission.vehicles[seller]]) > 1:
                pairFound = True
                print("Seller and buyer successfully found")
                print(f"Buyer's balance {account_balances[buyer]}")
                print(f"Seller's balance {account_balances[seller]}")
            else: 
                if kthBestBuyer == kthBestSeller:
                    kthBestBuyer += 1
                else: 
                    kthBestSeller += 1
         # Subtract timeout from pairs
        for pair in pairsTimeOut.keys():
            if pairsTimeOut[pair] > 0:
                pairsTimeOut[pair] -= 1

        # If none of the pairs are tradeable
        if pairFound == False:
            continue

       
        print("================================================")
        # Find tasks to trade and update vehicle assignments
        keptNodes = find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, pairsTimeOut)
        tradedNodes = mission.vehicle_assignments[mission.vehicles[seller]] - keptNodes
        mission.vehicle_assignments[mission.vehicles[buyer]] =  mission.vehicle_assignments[mission.vehicles[buyer]].union(tradedNodes)
        mission.vehicle_assignments[mission.vehicles[seller]] = keptNodes
        updateRegions(mission, regionNeighborNodes, seller, buyer, tradedNodes, region_map)

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

    sellerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[seller]])
    buyerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[buyer]])
    buyerNeighborsInSeller = regionNeighborNodes[mission.vehicles[buyer]].intersection(mission.vehicle_assignments[mission.vehicles[seller]])

    tradeFound = False
    kthLargest = 1
    while (tradeFound == False and kthLargest <= len(buyerNeighborsInSeller)):
        print(f"All possible cell candidates: {str(buyerNeighborsInSeller)}")
        print("Now checking " + str(kthLargest) + "th largest cell as candidate")
        if not buyerNeighborsInSeller:
            # return empty and mark the pair as untradable if no neighboring nodes (meaning one might be empty or another error?)
            print("Pairs are untradeable")
            pairsTimeOut[frozenset({buyer, seller})] = 1
            return mission.vehicle_assignments[mission.vehicles[seller]]

        # Candidate is kth largets node
        candidate = heapq.nlargest(kthLargest, buyerNeighborsInSeller, key=lambda node_key: graph.nodes[node_key]['weight'])[-1]
        print(f"{candidate} is selected as the candidate, with an area of {graph.nodes[candidate]['weight']}")
        if candidate in regionNeighborNodes[mission.vehicles[buyer]]:
            print("candidate is in buyer's neighbor set")
        else:
            print("candidate is not in buyer's neighbor set")
        if candidate in mission.vehicle_assignments[mission.vehicles[seller]]:
            print("Candidate is in the seller")
        else:
            print("Candidate is not in the seller")
        # Determine if candidate is the cut point
        if isCutPoint(mission, candidate, sellerRegionSubgraph, seller):
            print("Candidate is the cut point, searching q subtrees")
            print("========================================================")
            bestTradeIndex = float('inf')
            bestTradeSum = 0
            bestTrade = {}
            for neighbor in sellerRegionSubgraph[candidate]:
                stack = [neighbor]
                visited = set()
                dfs(visited, stack, candidate, sellerRegionSubgraph)
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
                # Increase K, don't return
                kthLargest += 1
                # Don't make the trade
                print("No available trades are better, checking next best candidate cell")
                print("=============================================================")
            else:
                account_balances[buyer] = account_balances[buyer] - bestTradeSum
                account_balances[seller] = account_balances[seller] + bestTradeSum
                print("Trading " + str(bestTradeSum) + " from the seller to the buyer")
                print("=============================================================")
                tradeFound=True
                pairsTimeOut[frozenset({buyer, seller})] = 1
                return bestTrade
        
        else:
            print("Candidate weight: " + str(graph.nodes[candidate]['weight']))
            account_balances[buyer] = account_balances[buyer] - graph.nodes[candidate]['weight']
            account_balances[seller] = account_balances[seller] + graph.nodes[candidate]['weight']
            tradeFound = True
            pairsTimeOut[frozenset({buyer, seller})] = 1
            return mission.vehicle_assignments[mission.vehicles[seller]] - {candidate}
        # If not returned yet no trade found, time out pair for 3 iterations and return seller assignments
    pairsTimeOut[frozenset({buyer, seller})] = 3
    return mission.vehicle_assignments[mission.vehicles[seller]]

# Pre-condition: A mission area
# Post-condtion: Returns a dictionary mapping an integer representing region to a set of nodes that neighbor that region
def find_neighbor_nodes (mission: MissionArea):
    graph = mission.grid_graph.graph
    print("Entering findNeighborNodes")
    # initalize a dictionary of empty sets for holding the neighbors of each region
    regionNeighborNodes = {key: set() for key in mission.vehicles}
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
    print("\n\t" + str(weightSum))
    return weightSum

def updateRegions(mission, regionNeighborNodes, seller, buyer, tradedNodes, region_map):
        graph = mission.grid_graph.graph
        # Update regions post trade
        for node_key in mission.vehicle_assignments[mission.vehicles[seller]]:
            graph.nodes[node_key]['region'] = mission.vehicles[seller]
        for node_key in mission.vehicle_assignments[mission.vehicles[buyer]]:
            graph.nodes[node_key]['region'] = mission.vehicles[buyer]

        # If a region gains neighboring that they were also neighbors with, they are no longer neighbors
        regionNeighborNodes[mission.vehicles[buyer]] = regionNeighborNodes[mission.vehicles[buyer]] - regionNeighborNodes[mission.vehicles[buyer]].intersection(tradedNodes)
        
        for node_key in tradedNodes:
            for neighbor_key in graph[node_key]:
                neighbor_data = graph.nodes[neighbor_key]
                if region_map[neighbor_data['region']] != seller:
                    regionNeighborNodes[mission.vehicles[seller]] -= {neighbor_key}
        
        # Add new neighbors
        buyerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[buyer]])
        updateNeighbors(mission, buyerRegionSubgraph, regionNeighborNodes)
        sellerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[mission.vehicles[seller]])
        updateNeighbors(mission, sellerRegionSubgraph, regionNeighborNodes)

def updateNeighbors(mission, regionSubgrapgh, regionNeighborNodes):
    graph = mission.grid_graph.graph
    for node_key in regionSubgrapgh:
        node_data = graph.nodes[node_key]
        for neighbor_key in graph[node_key]:
            neighbor_data = graph.nodes[neighbor_key]
            if neighbor_data['region'] != node_data['region']:
                regionNeighborNodes[node_data['region']].add(neighbor_key)

def isCutPoint(mission, candidate, sellerRegionSubgraph, seller):
    start = None
    for e in sellerRegionSubgraph[candidate]:
        start = e
        break
    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        visited.add(node)
        for neighbor in sellerRegionSubgraph[node]:
            if neighbor not in visited and neighbor != candidate:
                stack.append(neighbor)

    if mission.vehicle_assignments[mission.vehicles[seller]] - {candidate} == visited:
        return False
    return True 

def printIteration(i, iterations):
    print("#######################################")
    print(f"Starting {iterations - i}th iteration")
    print("#######################################")

def dfs(visited, stack, candidate, regionSubgraph):
    # DFS Traversal of all subtrees from the selected root node to determine the best trade
    # ** NOTE ** Avoids loops by using a visited node
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
        for neighbor in regionSubgraph[node]:
            if neighbor not in visited and neighbor != candidate:
                stack.append(neighbor)
