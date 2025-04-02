import matplotlib.pyplot as plt

import missionLayouts
from MissionArea import MissionArea, calculate_sensor_range_gcd
from gridArrayGenerator import genConnectedGrid
from UxV import UxV
from cyclicRegionGrowth import cyclic_region_growth, calculate_optimal_tasks
from regionFineTuning import findNeighborNodes
from cellDecomposition import cell_decomposition
from networkx.algorithms.approximation import traveling_salesman_problem
from sensorRangeDecomposition import sensor_range_decomposition
from pathPlanning import calculate_vehicle_paths
from missionLayouts import *

# Create a list of UxV objects to be added as nodes
uxvs = []
uxvs.append(UxV(name="alpha", position=(0,15), speed=(5), sensorRange=(10), type="UUV", endurance=200))
uxvs.append(UxV(name="bravo", position=(300,30), speed=(5), sensorRange=(10), type="UUV", endurance=100))
uxvs.append(UxV(name="charlie", position=(600,75), speed=(10), sensorRange=(5), type="UUV", endurance=100))
uxvs.append(UxV(name="delta", position=(900, 55), speed=(20), sensorRange=(20), type="UUV", endurance=100))

# Generate a random 2D numpy array to represent mission area
# grid_data = genConnectedGrid(75, 50, .2, 5)
grid_data = missionLayouts.mission_area_1_upscaled


# Create a MissionArea object to manage mission info
cellDimension = calculate_sensor_range_gcd(uxvs) * 2
mission_3 = MissionArea("Mission", grid_data, cellDimension)


# Add each vehicle to mission
mission_3.add_vehicles_to_graph(uxvs)

# Apply algorithms to mission to determine task allocation

cell_decomposition(mission_3)

cyclic_region_growth(mission_3)
# mission_3.neighbors = findNeighborNodes(mission_3)
print(mission_3.neighbors)


# Path finding
# tsp = traveling_salesman_problem
# print(tsp(mission_3.grid_graph.graph, nodes=[uxv1.position, uxv2.position]))

mission_3.redraw_grid_colormesh()


sensor_range_decomposition(mission_3)
vehicle_paths = calculate_vehicle_paths(mission_3)

# Display result

mission_3.draw(show_neighbors=False, node_color="blue", edge_color="white", vehicle_paths=vehicle_paths)
plt.show()





