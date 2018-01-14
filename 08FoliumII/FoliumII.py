# import

%matplotlib inline
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read shapefiles

Bangladesh_geodf = gpd.read_file("BGD_adm_shp/BGD_adm1.shp")
Bangladesh_geodf['coords'] = Bangladesh_geodf['geometry'].apply(lambda x: x.representative_point().coords[:])
Bangladesh_geodf['coords'] = [coords[0] for coords in Bangladesh_geodf['coords']]
Bangladesh_geodf.head()

India_geodf = gpd.read_file("IND_adm_shp/IND_adm1.shp")
India_geodf['coords'] = India_geodf['geometry'].apply(lambda x: x.representative_point().coords[:])
India_geodf['coords'] = [coords[0] for coords in India_geodf['coords']]
India_geodf.head()

Myanmar_geodf = gpd.read_file("MMR_adm_shp/MMR_adm1.shp")
Myanmar_geodf['coords'] = Myanmar_geodf['geometry'].apply(lambda x: x.representative_point().coords[:])
Myanmar_geodf['coords'] = [coords[0] for coords in Myanmar_geodf['coords']]
Myanmar_geodf.head()

Pakistan_geodf = gpd.read_file("PAK_adm_shp/PAK_adm1.shp")
Pakistan_geodf['coords'] = Pakistan_geodf['geometry'].apply(lambda x: x.representative_point().coords[:])
Pakistan_geodf['coords'] = [coords[0] for coords in Pakistan_geodf['coords']]
Pakistan_geodf.head()

# Concatenate

frames = [Bangladesh_geodf, India_geodf, Myanmar_geodf, Pakistan_geodf]
result = pd.concat(frames)
result.plot()

# Read shapefiles for countries

Bangladesh_country = gpd.read_file("BGD_adm_shp/BGD_adm0.shp")
Bangladesh_country['coords'] = Bangladesh_country['geometry'].apply(lambda x: x.representative_point().coords[:])
Bangladesh_country['coords'] = [coords[0] for coords in Bangladesh_country['coords']]
Bangladesh_country.head()

India_country = gpd.read_file("IND_adm_shp/IND_adm0.shp")
India_country['coords'] = India_country['geometry'].apply(lambda x: x.representative_point().coords[:])
India_country['coords'] = [coords[0] for coords in India_country['coords']]
India_country.head()

Myanmar_country = gpd.read_file("MMR_adm_shp/MMR_adm0.shp")
Myanmar_country['coords'] = Myanmar_country['geometry'].apply(lambda x: x.representative_point().coords[:])
Myanmar_country['coords'] = [coords[0] for coords in Myanmar_country['coords']]
Myanmar_country.head()

Pakistan_country = gpd.read_file("PAK_adm_shp/PAK_adm0.shp")
Pakistan_country['coords'] = Pakistan_country['geometry'].apply(lambda x: x.representative_point().coords[:])
Pakistan_country['coords'] = [coords[0] for coords in Pakistan_country['coords']]
Pakistan_country.head()

# Concatenate

frames_country = [Bangladesh_country, India_country, Myanmar_country, Pakistan_country]
result_country = pd.concat(frames_country)
result_country.plot()

# Read dataframe for polity score

df1 = pd.read_excel("polity.xlsx")
df1

# Merge with the state/provinces shapefile we just concatenated

polity_merge = result.merge(df1, on='NAME_0', how='left')
polity_merge.head()

# Read dataframes for armed groups

terminated = pd.read_excel("Terminated.xlsx", usecols = [3, 4, 5, 7, 9, 10, 12, 13, 22, 25])
terminated.head()

not_terminated = pd.read_excel("Not_terminated.xlsx", usecols = [3, 4, 5, 7, 9, 11, 13, 16, 18, 22, 25])
not_terminated.head()

# Mapping

# First method, using a predefined color scheme

import folium
from folium.element import IFrame
from geopy.geocoders import Nominatim

m = folium.Map([24, 84],
               zoom_start=5)

folium.TileLayer('Mapbox Bright').add_to(m)

ft = "Polity_score"
cmap = folium.colormap.linear.YlGn.to_step(9).scale(polity_merge[ft].min(), polity_merge[ft].max())

folium.GeoJson(polity_merge,
               style_function=lambda feature: {
                'fillColor': cmap(feature['properties'][ft]),
                'fillOpacity' : 0.95,
                'weight' : 1, 'color' : 'black'
               }).add_to(m)

cmap.caption = 'Polity Score Scale'
cmap.add_to(m)

folium.GeoJson(result_country,
               style_function=lambda feature: {'weight': 2, 'color':'black'}).add_to(m)

terminated_groups = terminated
terminated_groups["fullname"] = terminated_groups["fullname"].astype(str)

not_terminated_groups = not_terminated
not_terminated_groups["fullname"] = not_terminated_groups["fullname"].astype(str)

#my_marker_cluster = folium.MarkerCluster().add_to(m)
for ix, row in terminated_groups.iterrows():
    folium.CircleMarker(location = [row['Latitude'],row['Longitude']], radius=5000, popup=row['fullname']
                        + ", formed in " + str(row['startdate'])
                        + ", terminated in " + str(row['obsyear'])
                        + " with " + str(row['terminateform'])
                        + ". Armed order was " + str(row['armedorder'])
                        + ". Group goal was " + str(row['aggoals'])
                        + ". Political participation status was " + str(row['polpar']) + ".", color='#FF0000', fill_color='#FF0000').add_to(m)

for ix, row in not_terminated_groups.iterrows():
    folium.CircleMarker(location = [row['Latitude'],row['Longitude']], radius=5000, popup=row['fullname']
                        + ", formation year " + str(row['startdate'])
                        + ". " + str(row['terminate']) + ". There is " + str(row['ceasefireongoing']) + " ongoing ceasefire, "
                        + "and " + str(row['peacedealongoing']) + " ongoing peacedeal"
                        + ". Armed order is " + str(row['armedorder'])
                        + ". Group goal is " + str(row['aggoals'])
                        + ". Political participation status is " + str(row['polpar']) + ".", color='#00FF00', fill_color='#00FF00').add_to(m)


m.save("HeatMap.html")
m

# Second method, defining your own color scheme

import folium
from folium.element import IFrame
from geopy.geocoders import Nominatim
import folium.colormap as cm

step = cm.StepColormap(['#AED6F1', '#3498DB', '#2874A6', '#1B4F72'], vmin=0., vmax=9., index=[0,6,7,8,9], caption='Polity Score')
step

m = folium.Map([24, 84], tiles='cartodbpositron', zoom_start=5)

ft='Polity_score'

folium.GeoJson(polity_merge,
               style_function=lambda feature: {
                'fillColor': step(feature['properties'][ft]),
                'fillOpacity' : 0.95,
                'weight' : 1, 'color' : 'white'
               }).add_to(m)

step.add_to(m)

folium.GeoJson(result_country,
               style_function=lambda feature: {'weight': 3, 'color':'black'}).add_to(m)

terminated_groups = terminated
terminated_groups["fullname"] = terminated_groups["fullname"].astype(str)

not_terminated_groups = not_terminated
not_terminated_groups["fullname"] = not_terminated_groups["fullname"].astype(str)

#my_marker_cluster = folium.MarkerCluster().add_to(m)
for ix, row in terminated_groups.iterrows():
    folium.CircleMarker(location = [row['Latitude'],row['Longitude']], radius=5000, popup=row['fullname']
                        + ", formed in " + str(row['startdate'])
                        + ", terminated in " + str(row['obsyear'])
                        + " with " + str(row['terminateform'])
                        + ". Armed order was " + str(row['armedorder'])
                        + ". Group goal was " + str(row['aggoals'])
                        + ". Political participation status was " + str(row['polpar']) + ".", color='#FF0000', fill_color='#FF0000').add_to(m)

for ix, row in not_terminated_groups.iterrows():
    folium.CircleMarker(location = [row['Latitude'],row['Longitude']], radius=5000, popup=row['fullname']
                        + ", formation year " + str(row['startdate'])
                        + ". " + str(row['terminate']) + ". There is " + str(row['ceasefireongoing']) + " ongoing ceasefire, "
                        + "and " + str(row['peacedealongoing']) + " ongoing peacedeal"
                        + ". Armed order is " + str(row['armedorder'])
                        + ". Group goal is " + str(row['aggoals'])
                        + ". Political participation status is " + str(row['polpar']) + ".", color='#00FF00', fill_color='#00FF00').add_to(m)


m.save("HeatMap2.html")
m
