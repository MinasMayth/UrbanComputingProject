import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def choropleth_mapper(month_csv, month_name):
    covid_data = pd.read_csv(month_csv)
    demo_data = pd.read_csv("data/demographic_data/Population_density.csv")

    summed_data = gpd.GeoDataFrame(covid_data.groupby(["Municipality_name"], as_index=False).sum())

    imd = gpd.read_file("data/shape_data/WijkBuurtkaart_2020_v3/gemeente_2020_v3.shp")

    filtered_data = imd.loc[imd['GM_NAAM'].isin(summed_data["Municipality_name"].values)]

    data_merged = filtered_data.merge(summed_data, right_on="Municipality_name", left_on="GM_NAAM")

    data_merged.drop_duplicates(subset=["GM_NAAM"], keep='last', inplace=True)

    fig, ax = plt.subplots(1, 1)

    divider = make_axes_locatable(ax)

    cax = divider.append_axes('right', size='5%', pad=0.05)

    data_merged.plot(column="Total_reported",
                     legend=True,  # Decide to show legend or not
                     figsize=[10, 5],
                     vmin=0,
                     vmax=1500,
                     ax=ax,
                     cax=cax,
                     legend_kwds={'label': "Total reported" + " " + str(month_name)},
                     cmap="cividis"
                     )

    plt.savefig("/graphs/" + month_name + ".png")


if __name__ == "__main__":
    choropleth_mapper("data/cleaned_data/covid_march.csv", "march")
    choropleth_mapper("data/cleaned_data/covid_april.csv", "april")
    choropleth_mapper("data/cleaned_data/covid_may.csv", "may")
    choropleth_mapper("data/cleaned_data/covid_june.csv", "june")
    choropleth_mapper("data/cleaned_data/covid_july.csv", "july")