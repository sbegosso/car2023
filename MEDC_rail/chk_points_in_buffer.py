import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import sys

#params
buffer_miles = int(sys.argv[1])
buffer_meters = buffer_miles * 1609.34
crs = 'EPSG:3857'

#rail shp and converting to buffer
rail_gdf = gpd.read_file('tl_2019_us_rails.shp')
projected_rail_gdf = rail_gdf.to_crs(crs)
buffered_gdf = projected_rail_gdf.copy()
buffered_gdf['geometry'] = projected_rail_gdf['geometry'].buffer(buffer_meters)

#loading in excel data
plant_locations = pd.read_excel('light_vehicle_plant_locations.xlsx')
geometry = [Point(xy) for xy in zip(plant_locations['LONGITUDE'], plant_locations['LATITUDE'])]
geo_df = gpd.GeoDataFrame(plant_locations, geometry=geometry, crs='EPSG:4326')
geo_df_3857 = geo_df.to_crs(crs)

geo_df_3857['Score'] = geo_df_3857['geometry'].apply(
    lambda point: 0 if any(point.within(buffered_gdf) for buffered_gdf in buffered_gdf['geometry']) else -1
)

excel_output_path = 'results.xlsx'
geo_df_3857.to_excel(excel_output_path, index=False)
