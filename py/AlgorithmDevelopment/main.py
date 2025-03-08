import matplotlib.pyplot as plt
from MissionArea import MissionArea
from gridArrayGenerator import genConnectedGrid
from UxV import UxV
from cyclicRegionGrowth import cyclic_region_growth, calculate_optimal_tasks
from regionFineTuning import findNeighborNodes
from cellDecomposition import cell_decomposition
from networkx.algorithms.approximation import traveling_salesman_problem


# Create UxV objects to be added as nodes
uxv1 = UxV(name="alpha", position=(5,15), speed=(10), sensorRange=(10), type="UUV", endurance=200)
uxv2 = UxV(name="bravo", position=(45,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv3 = UxV(name="charlie", position=(155,275), speed=(5), sensorRange=(15), type="UUV", endurance=100)
uxv4 = UxV(name="delta", position=(315, 345), speed=(20), sensorRange=(15), type="UUV", endurance=100)

# Generate a random 2D numpy array to represent mission area
grid_data = genConnectedGrid(75, 50, .2, 5)

# Create a MissionArea object to manage mission info
mission_3 = MissionArea("Mission", grid_data, 10)





# Add each vehicle to mission
mission_3.add_vehicle_to_graph(uxv1)
mission_3.add_vehicle_to_graph(uxv2)
mission_3.add_vehicle_to_graph(uxv3)
mission_3.add_vehicle_to_graph(uxv4)

# Apply algorithms to mission to determine task allocation

cell_decomposition(mission_3)

cyclic_region_growth(mission_3)
mission_3.neighbors = findNeighborNodes(mission_3)
print(mission_3.neighbors)

# Path finding
tsp = traveling_salesman_problem



# Display result
mission_3.draw(show_neighbors=False)

plt.show()





