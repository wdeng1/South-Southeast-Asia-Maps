%matplotlib inline
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load files
# import electoral division shapefile
geo_df = gpd.read_file("data1/map.shp")
geo_df['coords'] = geo_df['geometry'].apply(lambda x: x.representative_point().coords[:])
geo_df['coords'] = [coords[0] for coords in geo_df['coords']]
geo_df.plot()
geo_df.to_csv("geo.csv")
geo_df.rename(columns = {"polling_di" : "Divisions"}, inplace = True)

# road file
roads_df = gpd.read_file("dataroads/main_roads/main_roads.shp")
roads_df['coords'] = roads_df['geometry'].apply(lambda x: x.representative_point().coords[:])
roads_df['coords'] = [coords[0] for coords in roads_df['coords']]
roads_df.head()

# electoral turnout file
df1 = pd.read_excel("1970turnout.xlsx")
df1.fillna(value=0, inplace=True)
df1.head()

# merge turnout data with electoral division geo-dataframe
geo_merge = geo_df.merge(df1, on='Divisions', how='left')
col_name = geo_merge.columns[0]
geo_merge.fillna(value=0, inplace=True)
geo_merge.head()

# load attacked police stations
import shapely.wkt

police1 = gpd.read_file('srilanka_policestations/controlled.shp')
police1.head()
police1['geometry'] = police1['geometry'].apply(shapely.wkt.loads)

# load not attacked police stations
police2 = gpd.read_file('srilanka_policestations/notcontrolled.shp')
police2.head()
police2['geometry'] = police2['geometry'].apply(shapely.wkt.loads)

# Map
# map choropleth layer
ft = "Turnout"

plate = geo_merge.to_crs(epsg=4269)
ax = plate.plot(column = ft, scheme = "fisher_jenks", k = 9, cmap = "Blues", legend = True,
                 alpha = 0.65, linewidth = 0.9, figsize = (60, 40))

# map police stations
police1.plot(ax=ax, marker='o', color='red', markersize=7)
police2.plot(ax=ax, marker='o', color='gold', markersize=7)

# map roads
roads_df.plot(ax=ax, color='0.30', linewidth = 1)

# add title and label electoral divisions
ax.set_title("Parliamentary Election Turnout (1970)", fontsize = 40)
ax.set_axis_off()
for idx, row in geo_df.iterrows():
    plt.annotate(s=row['Divisions'], xy=row['coords'],
                 horizontalalignment='center')

# Another example
# load SLFP vote share file
df2 = pd.read_excel("1970_SLFP.xlsx")
df2 = df2.dropna(subset = ['share'])
df2.head()

# merge with electoral division geo-dataframe
geo_merge2 = geo_df.merge(df2, on='Divisions', how='left')
col_name = geo_merge2.columns[0]
geo_merge2 = geo_merge2.dropna(subset = ['share'])
geo_merge2.head()

# map
ft = "share"

plate = geo_merge2.to_crs(epsg=4269)
ax = plate.plot(column = ft, scheme = "fisher_jenks", k = 9, cmap = "Oranges", legend = True,
                 alpha = 0.65, linewidth = 0.9, figsize = (60, 40))

police1.plot(ax=ax, marker='o', color='blue', markersize=7)
police2.plot(ax=ax, marker='o', color='green', markersize=7)

roads_df.plot(ax=ax, color='0.3', linewidth = 1)

ax.set_title("SLFP Vote Share (Parliamentary Election, 1970)", fontsize = 40)
ax.set_axis_off()
for idx, row in geo_df.iterrows():
    plt.annotate(s=row['Divisions'], xy=row['coords'],
                 horizontalalignment='center')
