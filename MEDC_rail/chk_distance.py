import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import matplotlib.pyplot as plt

#params
buffer_distance_miles = 1
buffer_distance_meters = buffer_distance_miles * 1609.34
projected_crs = 'EPSG:3857'

#import shps
gdf_rail = gpd.read_file('tl_2019_us_rails.shp')
us_boundaries = gpd.read_file('cb_2018_us_state_500k.shp')

#adjust shp
gdf_rail_buffer = gdf_rail.copy()
gdf_rail_buffer = gdf_rail_buffer.to_crs(projected_crs)
gdf_rail_buffer['geometry'] = gdf_rail_buffer['geometry'].buffer(buffer_distance_meters)

#compiling points
locations_df = pd.read_excel('light_vehicle_plant_locations.xlsx')

#check if points inside buffer
points_within_buffer = []

points_within_buffer_df = pd.DataFrame(columns=locations_df.columns)

for index, row in locations_df.iterrows():
    longitude = row['VP: Longitude']
    latitude = row['VP: Latitude']

    if pd.notna(longitude) and pd.notna(latitude):
        point = Point(longitude, latitude)

        for index, rail_row in gdf_rail_buffer.iterrows():
            if point.within(rail_row['geometry']):
                points_within_buffer_df = pd.concat([points_within_buffer_df, row.to_frame().T], ignore_index=True)
                break

points_within_buffer_df.to_excel('points_within_buffer.xlsx', index=False)