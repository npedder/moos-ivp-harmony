import MissionArea

def findNeighborNodes(mission: MissionArea):
    print("Entering findNeighborNodes")
    # Initialize a dictionary of empty sets for holding the neighbors of each region
    regionNeighborNodes = {key: set() for key in range(len(mission.vehicles))}
    
    # Iterate through the keys of each node and then the keys of that node's neighbors
    for node_key in dict(mission.grid_graph.graph.nodes).keys():
        node_data = mission.grid_graph.graph.nodes[node_key]
        for neighbor_key in dict(mission.grid_graph.graph[node_key]).keys():
            neighbor_data = mission.grid_graph.graph.nodes[neighbor_key]
            if neighbor_data['region'] != node_data['region']:
                regionNeighborNodes[node_data['region']].add(neighbor_key)
    
    return regionNeighborNodes


def region_fine_tuning(mission_3: MissionArea, f_prime, V, max_Inum):
    # Step 1: Initialize variables
    
    N_two_prime = dict(mission_3.grid_graph.graph.nodes)
    
    max_f = max(abs(x) for x in f_prime)
    iter_number = 0
    
    # Step 2: Generate the set of connected cells of K partitions
    BV = V  # BV_k for each vehicle, where V contains sets of tuples
    
    # Step 3: Iteratively balance task assignments
    while max_f != 0 and iter_number <= max_Inum:
        # Step 4: Identify the partitions with max and min tasks
        start = f_prime.index(max(f_prime))  # Partition with max tasks
        dest = f_prime.index(min(f_prime))  # Partition with min tasks
        
        # Step 6: Generate a path for task exchange using DFS
        path = [start]
        visited = set()
        stack = [start] 
        
        while stack:
            node = stack.pop()
            if node == dest:
                break
            visited.add(node)

            # If BV[node] is a set of tuples, extract the first element of the tuple (cell)
            if node in BV:
                neighbors = {t[0] for t in BV[node]} - visited  # Extract the first element of each tuple
            else:
                continue  # Skip this node or handle accordingly
            
            stack.extend(neighbors)
            path.append(node)
        
        path.append(dest)

        # Step 7: Task exchange along the path
        for i in range(1, len(path) - 1):
            # Get the next cell from the previous partition (which might be a tuple)
            cell = next(iter(BV[path[i - 1]]), None)  # Select a cell to move
            if cell is None:
                continue
            
            # Step 9: Assign cell to new partition
            N_two_prime[cell] = path[i]  
            
            # Step 10-11: Update BV sets
            BV[path[i - 1]].remove(cell)
            BV[path[i]].add(cell)
        
        # Step 13-14: Update function values
        f_prime[start] -= 1
        f_prime[dest] += 1
        
        # Step 15-16: Update max_f and iteration count
        max_f = max(abs(x) for x in f_prime)
        iter_number += 1
    
    # Step 18: Return the adjusted partitions
    return N_two_prime
