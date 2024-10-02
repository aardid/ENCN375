import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import HBox
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import numpy as np

def create_sea_level_mask(contour, sea_level):
    """
    Create a mask that represents areas that would be flooded given a sea level rise.
    """
    elevation_field = 'Contour'
    flooded_areas = contour[contour[elevation_field] <= sea_level]
    flooded_geom = flooded_areas.unary_union  # Combine all polygons
    flooded_gdf = gpd.GeoDataFrame(geometry=[flooded_geom], crs=contour.crs)
    return flooded_gdf

def plot_map_full_sea_level(contour, coastline, roads, marae, sea_level, zoom=False):
    """
    Plot the map showing sea level rise and its effect on the coastline.
    """
    # Generate flooded areas based on the sea level rise
    flooded_gdf = create_sea_level_mask(contour, sea_level)

    # Visualize the map with the risks and new coastline
    fig, ax = plt.subplots(figsize=(6, 6) if zoom else (10, 10))
    
    # Set background sea area color
    ax.set_facecolor('lightblue')

    # Plot original coastline
    coastline.plot(ax=ax, edgecolor='blue', facecolor='lightgreen', alpha=1.0, linewidth=1.5, label='Original Coastline')

    # Plot roads
    roads.plot(ax=ax, color="gray", label="Roads")

    # Plot flooded areas representing new coastline due to sea level rise
    flooded_gdf.plot(ax=ax, color='red', linewidth=2.5, alpha=.9, label=f'New Coastline with {sea_level}m SLR')
    coastline.plot(ax=ax, edgecolor='blue', alpha=1.0, linewidth=1.5, )#label='Original Coastline')

    # Plot marae
    marae.plot(ax=ax, color='m', markersize=15, label='Marae', zorder=5)
    
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

    plt.title(f"Sea Level Rise Scenario ({sea_level}m) with New Coastline")
    plt.legend()
    plt.show()

def load_int():
    '''
    '''
    # Load shapefiles (adjust file paths as needed)
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
    
    return contour, coastline, roads, marae

def plot_map_full_sea_level_int(contour, coastline, roads, marae):
    """
    Creates an interactive slider to modify sea level rise and plot map dynamically.
    """
    # Create an interactive slider for sea level rise
    slider = widgets.FloatSlider(
        value=1,   # Initial sea level rise
        min=0,     # Minimum sea level rise
        max=4,    # Maximum sea level rise
        step=1,  # Step size for slider
        description='Sea Level + tides (m):',
        continuous_update=False
    )

    # Interactive plotting function
    def update_plot(sea_level):
        plot_map_full_sea_level(contour, coastline, roads, marae, sea_level, zoom=True)

    # Return the interactive widget
    return widgets.interactive(update_plot, sea_level=slider)

# Existing functions to estimate flooded area, roads, and houses
def estimate_flooded_area(sea_level):
    # Known points from the linear relationship
    x = np.array([1, 2, 3])  # Sea levels in meters
    y = np.array([0.06, 2.39121, 3.3279868])  # Corresponding flooded areas in km²

    # Fit a linear model and estimate the area for the given sea level
    coefficients = np.polyfit(x, y, 1)
    estimated_area = np.polyval(coefficients, sea_level)
    
    return estimated_area

def estimate_flooded_roads(estimated_area):
    roads_per_km2 = 10
    flooded_roads = estimated_area * roads_per_km2
    return flooded_roads

def estimate_flooded_houses(flooded_area):
    houses_per_km2 = 150
    flooded_houses = flooded_area * houses_per_km2
    return int(flooded_houses)

# Main interactive plot function with buttons for estimation
def plot_map_full_sea_level_int_button(contour, coastline, roads, marae):
    """
    Creates an interactive slider to modify sea level rise and plot map dynamically,
    along with buttons to compute flooded area, roads, and houses.
    """
    # Create an interactive slider for sea level rise
    slider = widgets.FloatSlider(
        value=1,   # Initial sea level rise
        min=0,     # Minimum sea level rise
        max=4,     # Maximum sea level rise
        step=1,    # Step size for slider
        description='Sea Level + tides (m):',
        continuous_update=False
    )

    # Create buttons with fixed width for better display
    button_area = widgets.Button(description="Compute Flooded Area", layout=widgets.Layout(width='200px'))
    button_roads = widgets.Button(description="Compute Flooded Roads", layout=widgets.Layout(width='200px'))
    button_houses = widgets.Button(description="Compute Flooded Houses", layout=widgets.Layout(width='200px'))
    
    # Output areas for the results
    output_area = widgets.Output()
    output_roads = widgets.Output()
    output_houses = widgets.Output()

    # Interactive plotting function
    def update_plot(sea_level):
        plot_map_full_sea_level(contour, coastline, roads, marae, sea_level, zoom=True)

    # Button callback functions
    def compute_area(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        with output_area:
            output_area.clear_output()
            print(f"Flooded area for {sea_level}m sea level rise (+ tide): {flooded_area:.2f} km²")

    def compute_roads(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        flooded_roads = estimate_flooded_roads(flooded_area)
        with output_roads:
            output_roads.clear_output()
            print(f"Flooded roads for {sea_level}m sea level rise (+ tide): {flooded_roads:.2f} km")

    def compute_houses(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        flooded_houses = estimate_flooded_houses(flooded_area)
        with output_houses:
            output_houses.clear_output()
            print(f"Flooded houses for {sea_level}m sea level rise (+ tide): {flooded_houses} houses")

    # Link buttons to their callback functions
    button_area.on_click(compute_area)
    button_roads.on_click(compute_roads)
    button_houses.on_click(compute_houses)
    
    # Arrange buttons in a horizontal box (HBox) and display
    buttons_box = HBox([button_area, button_roads, button_houses])

    # Display the interactive slider, plot, buttons, and outputs
    display(widgets.interactive(update_plot, sea_level=slider), 
            button_area, output_area, 
            button_roads, output_roads, 
            button_houses, output_houses)
    
# Assumption-based function for economic loss estimation
def estimate_economic_loss(flooded_houses, flooded_roads):
    """
    Estimate the economic loss due to flooded houses and roads.

    Assumptions:
    - 600k NZD per house
    - 1.5m NZD per km of road
    """
    house_price = 600000  # NZD
    road_price_per_km = 1500000  # NZD
    
    house_loss = flooded_houses * house_price
    road_loss = flooded_roads * road_price_per_km
    total_loss = house_loss + road_loss
    
    return house_loss, road_loss, total_loss

# Main interactive plot function with buttons for estimation
def plot_map_full_sea_level_int_button_eco_loss(contour, coastline, roads, marae):
    """
    Creates an interactive slider to modify sea level rise and plot map dynamically,
    along with buttons to compute flooded area, roads, houses, and economic losses.
    """
    # Create an interactive slider for sea level rise
    slider = widgets.FloatSlider(
        value=1,   # Initial sea level rise
        min=0,     # Minimum sea level rise
        max=4,     # Maximum sea level rise
        step=1,    # Step size for slider
        description='Sea Level + tides (m):',
        continuous_update=False
    )

    # Create buttons with fixed width for better display
    button_area = widgets.Button(description="Compute Flooded Area", layout=widgets.Layout(width='200px'))
    button_roads = widgets.Button(description="Compute Flooded Roads", layout=widgets.Layout(width='200px'))
    button_houses = widgets.Button(description="Compute Flooded Houses", layout=widgets.Layout(width='200px'))
    button_loss = widgets.Button(description="Compute Economic Loss", layout=widgets.Layout(width='200px'))
    
    # Output areas for the results
    output_area = widgets.Output()
    output_roads = widgets.Output()
    output_houses = widgets.Output()
    output_loss = widgets.Output()

    # Interactive plotting function
    def update_plot(sea_level):
        plot_map_full_sea_level(contour, coastline, roads, marae, sea_level, zoom=True)

    # Button callback functions
    def compute_area(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        with output_area:
            output_area.clear_output()
            display(HTML(f"<p style='font-size:16px;'>Flooded area for {sea_level}m sea level rise (+ tide): {flooded_area:.2f} km²</p>"))

    def compute_roads(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        flooded_roads = estimate_flooded_roads(flooded_area)
        with output_roads:
            output_roads.clear_output()
            display(HTML(f"<p style='font-size:16px;'>Flooded roads for {sea_level}m sea level rise (+ tide): {flooded_roads:.2f} km</p>"))

    def compute_houses(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        flooded_houses = estimate_flooded_houses(flooded_area)
        with output_houses:
            output_houses.clear_output()
            display(HTML(f"<p style='font-size:16px;'>Flooded houses for {sea_level}m sea level rise (+ tide): {flooded_houses} houses</p>"))

    def compute_loss(b):
        sea_level = slider.value
        flooded_area = estimate_flooded_area(sea_level)
        flooded_roads = estimate_flooded_roads(flooded_area)
        flooded_houses = estimate_flooded_houses(flooded_area)
        house_loss, road_loss, total_loss = estimate_economic_loss(flooded_houses, flooded_roads)
        with output_loss:
            output_loss.clear_output()
            display(HTML(f"""
            <p style='font-size:16px;'>Estimated economic loss for {sea_level}m sea level rise (+ tide):</p>
            <p style='font-size:16px;'>  - House loss: ${house_loss:,.2f} NZD</p>
            <p style='font-size:16px;'>  - Road loss: ${road_loss:,.2f} NZD</p>
            <p style='font-size:16px;'>  - Total loss: ${total_loss:,.2f} NZD</p>
            <p style='font-size:14px; color:gray;'>Assumptions: NZD 600k per house and NZD 1.5m per km of road</p>
            """))

    # Link buttons to their callback functions
    button_area.on_click(compute_area)
    button_roads.on_click(compute_roads)
    button_houses.on_click(compute_houses)
    button_loss.on_click(compute_loss)
    
    # Arrange buttons in a horizontal box (HBox) and display
    buttons_box = HBox([button_area, button_roads, button_houses, button_loss])

    # Display the interactive slider, plot, buttons, and outputs
    display(widgets.interactive(update_plot, sea_level=slider), 
            buttons_box, output_area, output_roads, output_houses, output_loss)
   
# Compute the cost of constructing barriers
def compute_barrier_cost(sea_level):
    # Base price for 1-2 meters of sea level rise is 50m NZD per km
    barrier_length_km = 12  # 12 km of barrier
    base_cost_per_km = 50000000  # 50m NZD per km
    
    # If sea level is greater than 2m, increase the cost
    if sea_level > 2:
        additional_cost = (sea_level - 2) * 10000000  # Increase 10m per km for each meter above 2m
    else:
        additional_cost = 0  # No additional cost for 1-2m

    total_cost = barrier_length_km * (base_cost_per_km + additional_cost)
    return total_cost

# Compute the cost of relocating people from flooded houses
def compute_relocation_cost(flooded_houses):
    # Assume 4 people per house and 264,450 NZD per person relocation cost
    people_per_house = 4
    relocation_cost_per_person = 264450  # NZD
    
    total_people = flooded_houses * people_per_house
    total_relocation_cost = total_people * relocation_cost_per_person
    return total_relocation_cost

# Function to estimate the flooded area and houses
def estimate_flooded_area(sea_level):
    x = np.array([1, 2, 3])
    y = np.array([0.06, 2.39121, 3.3279868])
    coefficients = np.polyfit(x, y, 1)
    estimated_area = np.polyval(coefficients, sea_level)
    return estimated_area

def estimate_flooded_houses(flooded_area):
    houses_per_km2 = 150
    flooded_houses = flooded_area * houses_per_km2
    return int(flooded_houses)

# Interactive function for the mitigation sidebar
def mitigation_strategy_sidebar():
    """
    Creates an interactive sidebar with a slider for sea level rise and computes mitigation strategy costs:
    - Barrier construction cost
    - Relocation cost based on the number of houses affected
    """

    # Create an interactive slider for sea level rise
    sea_level_slider = widgets.FloatSlider(
        value=1,   # Initial sea level rise
        min=1,     # Minimum sea level rise
        max=3,     # Maximum sea level rise
        step=0.5,  # Step size for slider
        description='Sea Level + tides (m):',
        continuous_update=False
    )

    # Output area for the mitigation strategy costs
    output = widgets.Output()

    # Function to update the mitigation cost based on sea level
    def update_mitigation_cost(change):
        sea_level = sea_level_slider.value
        flooded_area = estimate_flooded_area(sea_level)
        flooded_houses = estimate_flooded_houses(flooded_area)

        # Compute costs
        barrier_cost = compute_barrier_cost(sea_level)
        relocation_cost = compute_relocation_cost(flooded_houses)

        with output:
            output.clear_output()
            display(HTML(f"""
            <p style='font-size:16px;'>Sea Level Rise (+ tide): {sea_level}m</p>
            <p style='font-size:16px;'>Flooded Area: {flooded_area:.2f} km²</p>
            <p style='font-size:16px;'>Flooded Houses: {flooded_houses}</p>
            <br>
            <p style='font-size:18px;'><b>Mitigation Costs:</b></p>
            <p style='font-size:16px;'>Barrier construction cost for 12 km: ${barrier_cost:,.2f} NZD</p>
            <p style='font-size:16px;'>Relocation cost: ${relocation_cost:,.2f} NZD</p>
            <br>
            <p style='font-size:18px;'><b>Assumptions:</b></p>
            <p style='font-size:14px; color:gray;'>- Barrier cost is 50m NZD per km for 1-2m sea level rise.</p>
            <p style='font-size:14px; color:gray;'>- An additional 10m NZD per km for every meter above 2m sea level rise.</p>
            <p style='font-size:14px; color:gray;'>- Relocation cost per person is 264,450 NZD.</p>
            """))

    # Link the slider to the update function
    sea_level_slider.observe(update_mitigation_cost, names='value')

    # Display the slider and output
    display(sea_level_slider, output)



