import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

covid_data = pd.read_csv("data/cleaned_data/covid_march.csv")
demo_data = pd.read_csv("data/demographic_data/Population_density.csv")

averaged_data = gpd.GeoDataFrame(covid_data.groupby(["Municipality_name"], as_index=False).mean())

# print(demo_data)

# imd = gpd.read_file("data/shape_data/shapefiles/cbsgebiedsindelingen2020.gpkg")
# print(imd["statnaam"])


print(covid_data)

imd = gpd.read_file("data/shape_data/data/NLD_adm2.shp")
new_imd = (imd.loc[imd["NAME_1"] == "Zuid-Holland"])

filtered_data = new_imd.loc[new_imd['NAME_2'].isin(averaged_data["Municipality_name"].values)]

for i in filtered_data["NAME_2"].values:
    print(i)

filtered_data.plot( figsize = [10,5])
plt.show()
