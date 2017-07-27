%matplotlib inline
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Read your shapefile into a geo-dataframe

geo_df = gpd.read_file("data1/LKA_adm1.shp")
geo_df.head()

geo_df.set_index(geo_df["ID_1"].astype(int), inplace = True)

# Plot it

geo_df.plot()

# Make a new column called coordinates, which is based on the “geometry” column

geo_df['coords'] = geo_df['geometry'].apply(lambda x: x.representative_point().coords[:])
geo_df['coords'] = [coords[0] for coords in geo_df['coords']]

# Label the districts

print(geo_df.crs)

# try 2163 (albers), 3857 (web), 4269 (plate)
ax = geo_df.to_crs(epsg=4269).plot()
ax.set_axis_off()
for idx, row in geo_df.iterrows():
    plt.annotate(s=row['NAME_1'], xy=row['coords'],
                 horizontalalignment='center')

geo_df.head()

# Spatial join

from shapely.geometry import Point

deaths_df = pd.read_excel("SLA_RoH_Deng.xlsx", usecols = [8, 9])
deaths_df.dropna(inplace = True)

geometry = [Point(xy) for xy in zip(deaths_df.Longitude, deaths_df.Latitude)]
deaths_coords = gpd.GeoDataFrame(deaths_df, crs = geo_df.crs, geometry=geometry)

located_deaths = gpd.sjoin(deaths_coords, geo_df, how = 'left', op = 'within')
located_deaths = located_deaths.dropna(axis=1, how='all')

# Plot it

located_deaths.plot()

# Rename the spatially joined table
# count and sum up the deaths in each district
# save as an Excel file and check for errors and NaNs


located_deaths.rename(columns = {"NAME_1" : "Districts", "index_right" : "deaths_per_district"}, inplace = True)

deaths_geo_count = located_deaths.groupby("Districts").count()[["deaths_per_district"]]
deaths_geo_count.to_excel("deaths_geo_count.xlsx")

# Import the Excel sheet and draw a bar graph with Pandas

deaths_geo_count = pd.read_excel("deaths_geo_count.xlsx")
deaths_geo_count.set_index("Districts")["deaths_per_district"].sort_values(ascending = False).plot(kind = "bar", figsize = (15, 3))

geo_df.rename(columns = {"NAME_1" : "Districts"}, inplace = True)

# Merge the geo-dataframe with the deaths dataframe

geo_merge = geo_df.merge(deaths_geo_count, on='Districts', how='left')
geo_merge
col_name =geo_merge.columns[0]
geo_merge.head()

# Plot the map

ft = "deaths_per_district"

plate = geo_merge.to_crs(epsg=4269)
ax = plate.plot(column = ft, scheme = "quantiles", k = 9, cmap = "Reds", legend = True,
                 alpha = 0.7, linewidth = 0.5, figsize = (50, 25))

ax.set_title("Sri Lankan Army Fatalities by District", fontsize = 30)
ax.set_axis_off()
for idx, row in geo_df.iterrows():
    plt.annotate(s=row['Districts'], xy=row['coords'],
                 horizontalalignment='center')
