%matplotlib inline
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the geo-dataframe and rename the column so it makes sense at a glance

geo_df = gpd.read_file("data1/LKA_adm1.shp")
geo_df.rename(columns = {"NAME_1" : "Districts"}, inplace = True)
geo_df.head()

# Load the deaths dataframe created last time from the spatial join function

deaths_geo_count = pd.read_excel("deaths_geo_count.xlsx")

# Merge the deaths dataframe and the geo-dataframe by districts

geo_merge = geo_df.merge(deaths_geo_count, on='Districts', how='left')
geo_merge
col_name =geo_merge.columns[0]
geo_merge.head()

# Mapping

import folium
from folium.element import IFrame
from geopy.geocoders import Nominatim

# Get the folium base map and set zoom position, then start mapping

m = folium.Map([8, 79.8],
               tiles='cartodbpositron',
               zoom_start=8)

ft = "deaths_per_district"
cmap = folium.colormap.linear.YlOrRd.scale(geo_merge[ft].min(), geo_merge[ft].max())

folium.GeoJson(geo_merge,
               style_function=lambda feature: {
                'fillColor': cmap(feature['properties'][ft]),
                'threshold_scale': [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400],
                'fillOpacity' : 0.7,
                'weight' : 1, 'color' : 'black'
               }).add_to(m)

cmap.caption = 'Deaths by district'
cmap.add_to(m)

# Add pop-ups

deaths = pd.read_excel('SLA_RoH_Deng.xlsx')
deaths["DATE"] = deaths["DATE"].astype(str)
deaths["NAME"] = deaths["NAME"].astype(str)
deaths["PLACE"] = deaths["PLACE"].astype(str)

my_marker_cluster = folium.MarkerCluster().add_to(m)
for ix, row in deaths.iterrows():
	text = "Name: " + row['NAME'] + "<br>" + "Location: " + str(row['PLACE']) + "<br>" + "Date: " + str(row['DATE'])
	popup = folium.Popup(IFrame(text, width=300, height=100))
	folium.Marker(location = [row['Latitude'],row['Longitude']], popup=popup).add_to(my_marker_cluster)

# Save map

m.save("HeatMap.html")
m
