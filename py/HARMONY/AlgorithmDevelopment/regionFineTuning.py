from AlgorithmDevelopment.MissionArea import MissionArea
from collections import defaultdict
import heapq

# Pre-condition: A mission area, the number of iterations the fine tuning should run for, and the account balances
#                for the vehicles/regions
# Post-condition: Updates mission area with new regions which should more closely reflect optimal vehicle assignments
def region_fine_tuning(mission, iterations, account_balances : list[int]):
    
    graph = mission.grid_graph.graph
    i = iterations
    pairsTimeOut = dict() # frozen set of two regions to a counter for how many turns they are in time out (if untradeable)
    last2trades = [] # List of pairs that have been traded in the last 2 iterations, and the contents of the trade
    regionNeighborNodes = find_neighbor_nodes(mission)

    while(i > 0):
        printIteration(i, iterations)
        print(f"Account balances: {account_balances}")
        # Select buyer and seller
        pairFound = False
        computedPairs = [] # max heap (min heap but using negated values)

        # Pre-compute the pairs
        for (region, buyerBal) in account_balances.items():
            neighborRegions = set(graph.nodes[node]["region"] for node in regionNeighborNodes[region]) # Set of neighboring regions
            print(f"Region: {region} with balance: {buyerBal} has neighbors: {neighborRegions}")
            print(f"Region neighbor nodes: {regionNeighborNodes[region]}")
            for sellerRegion in neighborRegions:
                sellerBal = account_balances[sellerRegion]
                difference = buyerBal - sellerBal
                print(f"DIFFERENCE: {difference} for buyer: {region} with balance: {buyerBal} and seller: {sellerRegion} with balance: {sellerBal}")
                if difference <= 0 or buyerBal <= sellerBal:
                    continue
                # else
                computedPair = (region, sellerRegion)
                pairObj = ((-1 * buyerBal), (-1 * difference), computedPair)
                heapq.heappush(computedPairs, pairObj)
        print(f"Computed pairs: {computedPairs}")

        while pairFound == False and computedPairs:
            pairObj = heapq.heappop(computedPairs)
            try:
                print(f"Checking pair (buyer, seller): {frozenset({pairObj[2][0], pairObj[2][1]})} with a difference of: {-1 * (pairObj[1])}")
                if pairsTimeOut[frozenset({pairObj[2][0], pairObj[2][1]})] == 0:
                    buyer = pairObj[2][0]
                    seller = pairObj[2][1]
                    pairFound = True
                    print(f"Pair found. The buyer is: {buyer}, The seller is: {seller}")
                    print(f"\tThe buyer has a balance of: {-1 * (pairObj[0])}, The seller has a balance of: {account_balances[seller]}")
                    print(f"\tThe difference is: {-1 * (pairObj[1])}, which should equal {-1 * (pairObj[0])} - {account_balances[seller]}, aka {-1 * (pairObj[0])} - {account_balances[seller]}")
                else:
                    print(f"Pair {frozenset({pairObj[2][0], pairObj[2][1]})} is in timeout for {pairsTimeOut[frozenset({pairObj[2][0], pairObj[2][1]})]} iterations")
            except:
                buyer = pairObj[2][0]
                seller = pairObj[2][1]
                pairFound = True

        # Subtract timeout from pairs
        for pair in pairsTimeOut.keys():
            if pairsTimeOut[pair] > 0:
                pairsTimeOut[pair] -= 1

        # If none of the pairs are tradeable
        if pairFound == False:
            print("No pairs are available for trade.")
            continue
       
        print("================================================")
        # Find tasks to trade and update vehicle assignments
        keptNodes = find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, pairsTimeOut, last2trades)
        tradedNodes = mission.vehicle_assignments[seller] - keptNodes
        mission.vehicle_assignments[buyer] =  mission.vehicle_assignments[buyer].union(tradedNodes)
        mission.vehicle_assignments[seller] = keptNodes
        updateRegions(mission, regionNeighborNodes, seller, buyer, tradedNodes)

        print(str(account_balances))
        print(str(buyer) + " is the buyer with a balance of: " + str(account_balances[buyer]))
        print(str(seller) + " is the seller with a balance of: " + str(account_balances[seller]))
        i = i - 1

# Pre-condition: Receives mission area, the buyer region, and the seller region
# Post-condition: Returns the subtree that when kept by the seller region, leads to an ideal transaction,
#                 otherwise if no trees are found that lead to an ideal transaction, no trade occurs and pair is marked
#                 untradeable for some amount of iterations
def find_kept_nodes(mission, regionNeighborNodes, buyer, seller, account_balances, pairsTimeOut, last2trades) :
    graph = mission.grid_graph.graph
    print("Entering finding kept nodes")

    sellerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[seller])
    if set(sellerRegionSubgraph) - mission.vehicle_assignments[seller] == set() and mission.vehicle_assignments[seller] - set(sellerRegionSubgraph) == set():
        print(f"Seller region subgraph and seller assignments contain the same elements")
    else:
        print(f"Seller region subgraph and seller assignments DO NOT contain the same elements")
        nonSharedElements = (set(sellerRegionSubgraph) - mission.vehicle_assignments[seller]).union(mission.vehicle_assignments[seller] - set(sellerRegionSubgraph))
        print(f"\tHere are the elements not in both sets {nonSharedElements}")
        print(f"The neighbors of (315, 345) in the full mission graph are: {graph.nodes[(315, 345)]}")
    buyerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[buyer])
    buyerNeighborsInSeller = regionNeighborNodes[buyer].intersection(mission.vehicle_assignments[seller])

    tradeFound = False
    kthLargest = 1
    while (tradeFound == False and kthLargest <= len(buyerNeighborsInSeller)):
        print(f"All possible cell candidates: {str(buyerNeighborsInSeller)}")
        print("Now checking " + str(kthLargest) + "th largest cell as candidate")
        if not buyerNeighborsInSeller:
            # return empty and mark the pair as untradable if no neighboring nodes (meaning one might be empty or another error?)
            print("Error: No neighbors of the buyer are in the seller")
            pairsTimeOut[frozenset({buyer, seller})] = 1
            print(f"Type of seller vehicle assignments is: {type(mission.vehicle_assignments[seller])}")
            return mission.vehicle_assignments[seller]

        # Candidate is kth largets node
        candidate = heapq.nlargest(kthLargest, buyerNeighborsInSeller, key=lambda node_key: graph.nodes[node_key]['weight'])[-1]
        print(f"{candidate} is selected as the candidate, with an area of {graph.nodes[candidate]['weight']}")

        # If candidate does not have any neighbors, the trade cannot be made
        if not sellerRegionSubgraph[candidate]:
            print("Candidate has no neighbors, trading nothing. (Cannot trade last cell away)")
            pairsTimeOut[frozenset({buyer, seller})] = 3
            print(f"Type of seller vehicle assignments is: {type(mission.vehicle_assignments[seller])}")
            return mission.vehicle_assignments[seller]

        if candidate in regionNeighborNodes[buyer]:
            print("candidate is in buyer's neighbor set")
        else:
            print("candidate is not in buyer's neighbor set")
        if candidate in mission.vehicle_assignments[seller]:
            print("Candidate is in the seller")
        else:
            print("Candidate is not in the seller")
        # Determine if candidate is the cut point
        if isCutPoint(mission, candidate, sellerRegionSubgraph, seller):
            print("Candidate is the cut point, searching q subtrees")
            print("========================================================")
            bestTradeIndex = max(abs(account_balances[buyer]), abs(account_balances[seller]))
            bestTradeSum = 0
            bestTrade = mission.vehicle_assignments[seller]
            # print(f"Seller region subgraph: {sellerRegionSubgraph.nodes.items()}")

            if set(sellerRegionSubgraph) - mission.vehicle_assignments[seller] == set() and mission.vehicle_assignments[seller] - set(sellerRegionSubgraph) == set():
                print(f"Seller region subgraph and seller assignments contain the same elements")
            else:
                print(f"Seller region subgraph and seller assignments DO NOT contain the same elements")
                nonSharedElements = (set(sellerRegionSubgraph) - mission.vehicle_assignments[seller]).union(mission.vehicle_assignments[seller] - set(sellerRegionSubgraph))
                print(f"\tHere are the elements not in both sets {nonSharedElements}")

            if(set(sellerRegionSubgraph) - set(graph) == set()):
                print(f"All items in the seller region subgraph are in the graph.")
            else:
                print(f"There exists items in the seller region subgraph that are not in the graph")
            assert (set(sellerRegionSubgraph) - set(graph) == set()), "There exists items in the seller region subgraph that are not in the graph."

            for neighbor in sellerRegionSubgraph[candidate]:
                stack = [neighbor]
                visited = set()
                dfs(visited, stack, candidate, sellerRegionSubgraph)
                # print(f"Visited: {visited}")
                # print(f"Seller region: {mission.vehicle_assignments[seller]}")

                candidateTrade = mission.vehicle_assignments[seller] - visited
                print(f"Current candidate trade: {candidateTrade}")
                if candidateTrade - set(graph) == set():
                    print(f"All items in the candidate trade are in the graph")
                else:
                    print(f"There exists items in the candidate trade that are not in the graph: {candidateTrade - set(graph)}")

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

            print("Checking if best trade is actually better than original state... ")
            if not isValidTrade(last2trades, buyer, seller, bestTradeSum) or bestTrade == mission.vehicle_assignments[seller] :
                # Increase K, don't return
                kthLargest += 1
                # Don't make the trade
                print("No available trades are better, checking next best candidate cell")
                print("=============================================================")
            else:
                print("It is valid! :)")
                account_balances[buyer] = account_balances[buyer] - bestTradeSum
                account_balances[seller] = account_balances[seller] + bestTradeSum
                print("Trading " + str(bestTradeSum) + " from the seller to the buyer")
                print("=============================================================")
                tradeFound=True
                # pairsTimeOut[frozenset({buyer, seller})] = 1
                updateTradeList(last2trades, buyer, seller, bestTradeSum)
                print(f"Type of bestTrade is: {type(bestTrade)}")
                return bestTrade
        else:
            if isValidTrade(last2trades, buyer, seller, graph.nodes[candidate]['weight']):
                print("Candidate weight: " + str(graph.nodes[candidate]['weight']))
                account_balances[buyer] = account_balances[buyer] - graph.nodes[candidate]['weight']
                account_balances[seller] = account_balances[seller] + graph.nodes[candidate]['weight']
                tradeFound = True
                # pairsTimeOut[frozenset({buyer, seller})] = 1
                updateTradeList(last2trades, buyer, seller, graph.nodes[candidate]['weight'])
                print(f"Type of seller vehicle assignments - candidate is {type(mission.vehicle_assignments[seller] - {candidate})}")
                return mission.vehicle_assignments[seller] - {candidate}
            # otherwise increase k, don't return
            kthLargest += 1
            # Don't make the trade
            print("No available trades are better, checking next best candidate cell")
            print("=============================================================")

    # If not returned yet no trade found, time out pair for 3 iterations and return seller assignments
    pairsTimeOut[frozenset({buyer, seller})] = 3
    print(f"Type of seller assignments is {type(mission.vehicle_assignments[seller])}")
    return mission.vehicle_assignments[seller]

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
    print(f"{regionNeighborNodes}")
    return regionNeighborNodes

def sum_weights(mission, subgraph):
    print("\tCalculating weight sum...")
    graph = mission.grid_graph.graph
    weightSum = 0
    # print(f"Vehicle start positions: {mission.vehicles}")
    # print(f"\tAll nodes in the subgrapgh: {subgraph}")
    # print(f"\tAll nodes in the graph: {graph.nodes.items()}")
    for node_key in subgraph:
        node_data = graph.nodes[node_key]
        weightSum += node_data['weight']
    print("\n\t" + str(weightSum))
    return weightSum

def updateRegions(mission, regionNeighborNodes, seller, buyer, tradedNodes):
        graph = mission.grid_graph.graph
        # Update regions post trade
        for node_key in mission.vehicle_assignments[seller]:
            graph.nodes[node_key]['region'] = seller
        for node_key in mission.vehicle_assignments[buyer]:
            graph.nodes[node_key]['region'] = buyer

        # If a region gains neighboring that they were also neighbors with, they are no longer neighbors
        regionNeighborNodes[buyer] = regionNeighborNodes[buyer] - regionNeighborNodes[buyer].intersection(tradedNodes)
        
        for node_key in tradedNodes:
            for neighbor_key in graph[node_key]:
                neighbor_data = graph.nodes[neighbor_key]
                if neighbor_data['region'] != seller:
                    regionNeighborNodes[seller] -= {neighbor_key}
        
        # Add new neighbors
        buyerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[buyer])
        updateNeighbors(mission, buyerRegionSubgraph, regionNeighborNodes)
        sellerRegionSubgraph = graph.subgraph(mission.vehicle_assignments[seller])
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
    if start is None:
        print("No neighbors found for candidate, returning False")
        return False
    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        visited.add(node)
        for neighbor in sellerRegionSubgraph[node]:
            if neighbor not in visited and neighbor != candidate:
                stack.append(neighbor)

    if mission.vehicle_assignments[seller] - {candidate} == visited:
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

def updateTradeList(last2trades, buyer, seller, tradeValue):
    # Update the last 3 trades with the current trade
    print("Updating trade list...")
    if len(last2trades) == 2:
        last2trades.pop(0)
    last2trades.append((buyer, seller, tradeValue))
    print(f"Last 2 trades: {last2trades}")
    return last2trades

def isValidTrade(last2trades, buyer, seller, tradeValue):

    # For trade to be invalid, last trades must include trade with the same buyer and seller, and the other trade must be the seller and buyer swapped
    print(f"Last two trades: {last2trades}")
    if len(last2trades) < 2:
        print("Not enough trades to asses back and fourth trades. Thus, trade is valid")
        return True
    if last2trades[0][0] == buyer and last2trades[0][1] == seller:
        # first trade is same, now other must be swapped
        if last2trades[1][0] == seller and last2trades[1][1] == buyer:
            print("Regions are trading back and fourth, trade is NOT valid")
            return False
    
    if last2trades[1][0] == buyer and last2trades[1][1] == seller:
        # first trade is same, now other must be swapped
        if last2trades[0][0] == seller and last2trades[0][1] == buyer:
            print("Regions are trading back and fourth, trade is NOT valid")
            return False

    print("Regions are NOT trading back and fourth, trade is valid")
    return True
    