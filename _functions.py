# Import required libraries
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
#
def plot_map_full(zoom=False,coords = None):
    #contour_file = r'C:\Temp\UC_teaching_notebook\data_test2\NB_shapes\NB_Contour_NB.shp'
    #coastline_file = r'C:\Temp\UC_teaching_notebook\data_test2\NB_shapes\NB_Coastline_LINZ.shp'
    #roads_file = r'C:\Temp\UC_teaching_notebook\data_test2\NB_shapes\NB_nz_road_centrelines_topo_150k.shp'
    #marae_file = r'C:\Temp\UC_teaching_notebook\data_test2\NB_shapes\NB_Marae_NB_UTM.shp'
    #contour_file = r'.\data_test2\NB_shapes\NB_Contour_NB.shp'
    #coastline_file = r'.\data_test2\NB_shapes\NB_Coastline_LINZ.shp'
    #roads_file = r'.\data_test2\NB_shapes\NB_nz_road_centrelines_topo_150k.shp'
    #marae_file = r'.\data_test2\NB_shapes\NB_Marae_NB_UTM.shp'
    contour_file = r'NB_Contour_NB.shp'
    coastline_file = r'NB_Coastline_LINZ.shp'
    roads_file = r'NB_nz_road_centrelines_topo_150k.shp'
    marae_file = r'NB_Marae_NB_UTM.shp'

    contour = gpd.read_file(contour_file)
    roads = gpd.read_file(roads_file)
    coastline = gpd.read_file(coastline_file)
    marae = gpd.read_file(marae_file)

    # Visualize the map with the risks
    def plot_map(zoom=zoom):
        if zoom:
            fig, ax = plt.subplots(figsize=(4, 4))
        else:
            fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_facecolor('lightblue')
        coastline.plot(ax=ax, edgecolor='blue', facecolor='lightgreen', alpha=0.6, linewidth=0.5, label='Coastline')
        marae.plot(ax=ax, color='m', markersize=15, label='Marae', zorder=5)
        roads.plot(ax=ax, color="gray", label="Roads")
        ax.set_xlim([1.565e6, 1.585e6])  # Adjust these values to match the rectangle you want
        ax.set_ylim([5.17e6, 5.21e6])

        # Add axis labels for UTM (NZTM projection)
        ax.set_xlabel('Easting (km)', fontsize=12)
        ax.set_ylabel('Northing (km)', fontsize=12)

        # Convert axis ticks to kilometers
        ax.set_xticklabels(np.round(ax.get_xticks() / 1000, 2))
        ax.set_yticklabels(np.round(ax.get_yticks() / 1000, 2))
        
        if zoom: 
           # Zoom in to the most affected coastal area
            ax.set_xlim([1.575e6, 1.585e6])  # Easting range
            ax.set_ylim([5.175e6, 5.185e6])  # Northing range

            # Add axis labels for UTM (NZTM projection)
            ax.set_xlabel('Easting (km)', fontsize=12)
            ax.set_ylabel('Northing (km)', fontsize=12)

            # Convert axis ticks to kilometers
            ax.set_xticklabels(np.round(ax.get_xticks() / 1000, 2))
            ax.set_yticklabels(np.round(ax.get_yticks() / 1000, 2))
                                        
        plt.title("Risk Identification: Case Study Area")
        plt.legend()
        plt.show()

    plot_map(zoom=zoom)
    
def estimate_flooded_area(sea_level):
    """
    Estimate the flooded area (km²) based on a linear relationship.
    
    Parameters:
    sea_level (float): The sea level rise in meters.
    
    Returns:
    float: Estimated flooded area in km².
    """
    # Known points from the linear relationship
    x = np.array([1, 2, 3])  # Sea levels in meters
    y = np.array([0.06, 2.39121, 3.3279868])  # Corresponding flooded areas in km²

    # Fit a linear model and estimate the area for the given sea level
    coefficients = np.polyfit(x, y, 1)
    estimated_area = np.polyval(coefficients, sea_level)
    
    return estimated_area

def estimate_flooded_roads(estimated_area):
    """
    Estimate the length of roads flooded (km) based on the flooded area.
    
    Parameters:
    estimated_area (float): The estimated flooded area in km².
    
    Returns:
    float: Estimated length of roads flooded in km.
    """
    # Assume 10 km of roads per 1 km² of flooded area
    roads_per_km2 = 10
    
    # Calculate the estimated length of roads flooded
    flooded_roads = estimated_area * roads_per_km2
    
    return flooded_roads

def estimate_flooded_houses(flooded_area):
    """
    Estimate the number of houses flooded based on the flooded area.
    
    Parameters:
    flooded_area (float): The estimated flooded area in km².
    
    Returns:
    int: Estimated number of houses flooded.
    """
    # Assume 150 houses per 1 km² of flooded area
    houses_per_km2 = 150
    
    # Calculate the estimated number of houses flooded
    flooded_houses = flooded_area * houses_per_km2
    
    return int(flooded_houses)  # Return as an integer

def create_sea_level_mask(contour, sea_level):
    """
    Create a mask that represents areas that would be flooded given a sea level rise.
    """
    elevation_field = 'Contour'  # Adjust based on your contour field name
    flooded_areas = contour[contour[elevation_field] <= sea_level]
    flooded_geom = flooded_areas.unary_union  # Combine all polygons
    flooded_gdf = gpd.GeoDataFrame(geometry=[flooded_geom], crs=contour.crs)
    return flooded_gdf

def plot_map_full_sea_level(sea_level, zoom=False):
    # File paths (update these based on your environment)
    #contour_file = r'C:\Temp\UC_interv_teaching_seminar\data_test2\NB_shapes\NB_Contour_NB.shp'
    #coastline_file = r'C:\Temp\UC_interv_teaching_seminar\data_test2\NB_shapes\NB_Coastline_LINZ.shp'
    #roads_file = r'C:\Temp\UC_interv_teaching_seminar\data_test2\NB_shapes\NB_nz_road_centrelines_topo_150k.shp'
    #marae_file = r'C:\Temp\UC_interv_teaching_seminar\data_test2\NB_shapes\NB_Marae_NB_UTM.shp'
    contour_file = r'NB_Contour_NB.shp'
    coastline_file = r'NB_Coastline_LINZ.shp'
    roads_file = r'NB_nz_road_centrelines_topo_150k.shp'
    marae_file = r'NB_Marae_NB_UTM.shp'

    # Load the shapefiles
    contour = gpd.read_file(contour_file)
    roads = gpd.read_file(roads_file)
    coastline = gpd.read_file(coastline_file)
    marae = gpd.read_file(marae_file)

    # Generate flooded areas based on the sea level rise
    flooded_gdf = create_sea_level_mask(contour, sea_level)

    # Visualize the map with the risks and new coastline
    def plot_map(zoom=zoom):
        if zoom:
            fig, ax = plt.subplots(figsize=(4, 4))
        else:
            fig, ax = plt.subplots(figsize=(8, 8))

        # Set background sea area color
        ax.set_facecolor('lightblue')

        coastline.plot(ax=ax, edgecolor='blue', facecolor='lightgreen', alpha=0.8, linewidth=1.5, label='Original Coastline')

        # Plot marae
        marae.plot(ax=ax, color='m', markersize=15, label='Marae', zorder=5)

        # Plot roads
        roads.plot(ax=ax, color="gray", label="Roads")

        # Plot flooded areas representing new coastline due to sea level rise
        flooded_gdf.plot(ax=ax, color='red', linewidth=2.5, alpha=.9, label=f'New Coastline with {sea_level}m SLR')
        
        # Plot original coastline
        coastline.plot(ax=ax, edgecolor='blue', alpha=0.8, linewidth=1.5)


        # Set x and y limits to the coastline area bounds
        ax.set_xlim([1.565e6, 1.585e6])  
        ax.set_ylim([5.17e6, 5.21e6])

        # Add axis labels for UTM (NZTM projection)
        ax.set_xlabel('Easting (km)', fontsize=12)
        ax.set_ylabel('Northing (km)', fontsize=12)

        # Convert axis ticks to kilometers
        ax.set_xticklabels(np.round(ax.get_xticks() / 1000, 2))
        ax.set_yticklabels(np.round(ax.get_yticks() / 1000, 2))

        if zoom:
            # Zoom in to the most affected coastal area
            ax.set_xlim([1.575e6, 1.585e6])  # Easting range
            ax.set_ylim([5.175e6, 5.185e6])  # Northing range

            # Add axis labels for UTM (NZTM projection)
            ax.set_xlabel('Easting (km)', fontsize=12)
            ax.set_ylabel('Northing (km)', fontsize=12)

            # Convert axis ticks to kilometers
            ax.set_xticklabels(np.round(ax.get_xticks() / 1000, 2))
            ax.set_yticklabels(np.round(ax.get_yticks() / 1000, 2))

        plt.title(f"Sea Level (+ tide) Rise Scenario ({sea_level}m) with New Coastline")
        plt.legend()
        plt.show()

    # Call the plot function with the zoom parameter
    plot_map(zoom=zoom)

def plot_map_full_sea_level_int(contour, coastline, roads, marae):
    """
    Creates an interactive slider to modify sea level rise and plot map dynamically.
    """
    # Create an interactive slider for sea level rise
    slider = widgets.FloatSlider(
        value=3,   # Initial sea level rise
        min=0,     # Minimum sea level rise
        max=10,    # Maximum sea level rise
        step=0.1,  # Step size for slider
        description='Sea Level (+ tide) (m):',
        continuous_update=False
    )

    # Interactive plotting function
    def update_plot(sea_level):
        plot_map_full_sea_level(contour, coastline, roads, marae, sea_level, zoom=False)

    # Return the interactive widget
    return widgets.interactive(update_plot, sea_level=slider)