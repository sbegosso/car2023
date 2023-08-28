import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

#importing rail lines
crs = 'EPSG:3857'
gdf = gpd.read_file('tl_2019_us_rails.shp')
projected_gdf = gdf.to_crs(crs)

#importing coordinate points
locations_df = pd.read_excel('light_vehicle_plant_locations.xlsx')
geometry = [Point(xy) for xy in zip(locations_df['LONGITUDE'], locations_df['LATITUDE'])]
geo_df = gpd.GeoDataFrame(locations_df, geometry=geometry, crs='EPSG:4326')
geo_df_3857 = geo_df.to_crs(crs)

#checking point
point = Point(-79.36046, 43.85449)
point_geometry = gpd.GeoSeries([point], crs='EPSG:4326')
point_geo_df = gpd.GeoDataFrame(geometry=point_geometry)
point_geo_df_3857 = point_geo_df.to_crs(crs)


#importing us border
boundaries = gpd.read_file('cb_2018_us_state_500k.shp')
projected_boundaries = boundaries.to_crs(crs)

#creating the buffer
buffer_distance_miles = 2 # in miles
buffer_distance_meters = buffer_distance_miles * 1609.34

buffered_gdf = projected_gdf.copy()
buffered_gdf['geometry'] = projected_gdf['geometry'].buffer(buffer_distance_meters)

#plotting
fig, ax = plt.subplots(figsize=(10, 10))
projected_boundaries.plot(ax=ax, edgecolor='black', alpha = 0.5)
buffered_gdf.plot(ax=ax, color='red', alpha=0.5, label='Buffered')
projected_gdf.plot(ax=ax, color='blue', alpha=0.5, label='Rail Lines')
geo_df_3857.plot(ax=ax, color='green', markersize=50, edgecolor='black')
point_geo_df_3857.plot(ax=ax, color='orange', markersize=80, edgecolor='blue')
ax.set_title('Supplier Locations with Major Railroads')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend()
plt.show()