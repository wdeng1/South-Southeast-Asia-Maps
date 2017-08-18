%matplotlib inline
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load files
# electoral divisions shapefile
geo_df = gpd.read_file("data1/map.shp")
geo_df['coords'] = geo_df['geometry'].apply(lambda x: x.representative_point().coords[:])
geo_df['coords'] = [coords[0] for coords in geo_df['coords']]
geo_df.plot()
geo_df.rename(columns = {"polling_di" : "Divisions"}, inplace = True)

# roads shapefile
roads_df = gpd.read_file("dataroads/roads.shp")
roads_df['coords'] = roads_df['geometry'].apply(lambda x: x.representative_point().coords[:])
roads_df['coords'] = [coords[0] for coords in roads_df['coords']]

# SLFP vote share file
df1 = pd.read_excel("1970_SLFP.xlsx")
df1 = df1.dropna(subset = ['share'])
df1.head()

# merge geo dataframe with SLFP vote share file
geo_merge = geo_df.merge(df1, on='Divisions', how='left')
geo_merge
col_name = geo_merge.columns[0]
geo_merge = geo_merge.dropna(subset = ['share'])
geo_merge.head()

# load police data files
police = pd.read_excel('controlled.xlsx')
police2 = pd.read_excel('notcontrolled.xlsx')

# Mapping
import folium
from folium.element import IFrame
from geopy.geocoders import Nominatim

# get base map
m = folium.Map([8, 79.8],
 zoom_start=8)

folium.TileLayer('cartodbpositron').add_to(m)

# specify choropleth layer options
ft = "share"
cmap = folium.colormap.linear.YlOrBr.scale(geo_merge[ft].min(), geo_merge[ft].max())

folium.GeoJson(geo_merge,
 style_function=lambda feature: {
 'fillColor': cmap(feature['properties'][ft]),
 'fillOpacity' : 0.9,
 'weight' : 1, 'color' : 'black'
 }).add_to(m)

# gradient legend
cmap.caption = 'SLFP Coalition Vote Share (Parliamentary Election, 1970)'
cmap.add_to(m)

# specify roads layer options

folium.GeoJson(roads_df,
 style_function=lambda feature: {
 'fillOpacity' : 0.5,
 'weight' : 1.5, 'color' : 'gray'
 }).add_to(m)

# add police stations as scatter points.
# first line indicates marker cluster
my_marker_cluster = folium.MarkerCluster().add_to(m)
for ix, row in police.iterrows():
 folium.CircleMarker(location = [row['Latitude'],row['Longitude']], radius=500, popup="Station: " + row['stations'], color='#0000FF', fill_color='#0000FF').add_to(m)
for ix, row in police2.iterrows():
 folium.CircleMarker(location = [row['Latitude'],row['Longitude']], radius=500, popup="Station: " + row['stations'], color='#00FF33', fill_color="#00FF33").add_to(m)
