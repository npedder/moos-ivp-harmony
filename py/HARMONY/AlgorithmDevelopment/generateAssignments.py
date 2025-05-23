import matplotlib.pyplot as plt

from AlgorithmDevelopment.MissionArea import MissionArea, calculate_sensor_range_gcd

from AlgorithmDevelopment.cyclicRegionGrowth import cyclic_region_growth, calculate_optimal_tasks
# from region_fine_tuning
from AlgorithmDevelopment.cellDecomposition import cell_decomposition
from AlgorithmDevelopment.regionFineTuning import region_fine_tuning
from AlgorithmDevelopment.sensorRangeDecomposition import sensor_range_decomposition
from AlgorithmDevelopment.pathPlanning import calculate_vehicle_paths
from AlgorithmDevelopment.missionLayouts import *

# All the portions of the algorithm, condensed into a single method
# Input: list of UxV objects, binary grid data, 0 is dead space, 1 is uncovered
# Output: Dictionary representing vehicle assignments (name : list of waypoints)
def generate_assignments(UxVs, grid_data, show_graph=False, mission_name="Mission", iterations=200):

    # Create mission object containing graph information to be manipulated
    cellDimension = int(calculate_sensor_range_gcd(UxVs))
    mission = MissionArea(mission_name, grid_data, cellDimension)

    cell_decomposition(mission)

    mission.add_vehicles_to_graph(UxVs)

    if len(mission.vehicles) > 1:
        bals = cyclic_region_growth(mission)

    if len(mission.vehicles) > 1:
        region_fine_tuning(mission, iterations, bals)

    if show_graph:
        mission.redraw_grid_colormesh()

    sensor_range_decomposition(mission)

    vehicle_paths = calculate_vehicle_paths(mission)

    # Display result
    if show_graph:
        mission.draw(show_neighbors=False, node_color="blue", edge_color="white", vehicle_paths=vehicle_paths)
        plt.show()

    return vehicle_paths


if __name__ == "__main__":
    try:
        from missionLayouts import *
        from UxV import UxV
    except:
        print("error importing mission layouts")

    # Usage
    uxvs = []
    uxvs.append(UxV(name="alpha", position=(0, 15), speed=(5), sensorRange=(10), type="UUV", endurance=200))
    uxvs.append(UxV(name="bravo", position=(300, 30), speed=(5), sensorRange=(10), type="UUV", endurance=100))
    uxvs.append(UxV(name="charlie", position=(600, 75), speed=(10), sensorRange=(5), type="UUV", endurance=100))
    uxvs.append(UxV(name="delta", position=(900, 55), speed=(20), sensorRange=(20), type="UUV", endurance=100))


    grid = mission_area_1_upscaled

    print(generate_assignments(uxvs, grid, show_graph=True, mission_name="Mission Test"))
