import pandas as pd

covid_data = pd.read_csv("data/covid_data/COVID-19_aantallen_gemeente_per_dag_tm_03102021.csv", sep=";")
covid_month_march = covid_data.loc[covid_data["Date_of_publication"].str.startswith("2020-08")]
covid_month_march = covid_month_march[["Date_of_publication", "Municipality_name",
                                       "Total_reported", "Deceased"]]

pop_density_data = pd.read_csv("data/demographic_data/Population_density.csv", sep=",")

covid_sorted = covid_month_march.sort_values(by=["Municipality_name"])

filtered_data = covid_sorted.loc[covid_sorted['Municipality_name'].isin(pop_density_data["Municipality"].values)]

sorted_data = (filtered_data.sort_values(by=["Municipality_name", "Date_of_publication"]))

sorted_data.to_csv("data/cleaned_data/covid_august.csv", index=False)
