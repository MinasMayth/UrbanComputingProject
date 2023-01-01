import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def choropleth_mapper(month_csv, month_name):
    covid_data = pd.read_csv(month_csv)

    summed_data = gpd.GeoDataFrame(covid_data)

    imd = gpd.read_file("data/shape_data/WijkBuurtkaart_2020_v3/gemeente_2020_v3.shp")

    filtered_data = imd.loc[imd['GM_NAAM'].isin(summed_data["Municipality_name"].values)]

    data_merged = filtered_data.merge(summed_data, right_on="Municipality_name", left_on="GM_NAAM")

    data_merged.drop_duplicates(subset=["GM_NAAM"], keep='last', inplace=True)

    fig, ax = plt.subplots(1, 1)

    divider = make_axes_locatable(ax)

    cax = divider.append_axes('right', size='5%', pad=0.05)

    data_merged.plot(column="Positive tests per 100000",
                     legend=True,  # Decide to show legend or not
                     figsize=[10, 5],
                     vmin=0,
                     vmax=10000,
                     ax=ax,
                     cax=cax,
                     legend_kwds={'label': "Positive tests per 100,000" + " " + str(month_name)},
                     cmap="cividis"
                     )

    #plt.show()
    plt.savefig("graphs/" + month_name + ".png")


if __name__ == "__main__":
    choropleth_mapper("data/cleaned_data/SH_monthly_data_dec2020.csv", "Dec_2020")
    choropleth_mapper("data/cleaned_data/SH_monthly_data_july2021.csv", "Jul_2021")
    choropleth_mapper("data/cleaned_data/SH_monthly_data_jan2022.csv", "Jan_2022")
