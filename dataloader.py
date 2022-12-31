import pandas as pd

testing_data = pd.read_csv("data/covid_data/COVID-19_per_municipality_per_day_2022.csv", sep=";")

south_holland_testing_data = (testing_data.loc[testing_data["Province"] == "Zuid-Holland"]).drop(
    labels=["Version", "Date_of_report", "Security_region_code", "Security_region_name",
            "Municipality_code", "ROAZ_region", "Municipal_health_service", "Province"], axis=1)

south_holland_testing_data.dropna(inplace=True)

SH_daily_data = south_holland_testing_data.loc[
    south_holland_testing_data["Date_of_publication"].str.startswith("2022-01")]
SH_daily_data.to_csv("data/cleaned_data/SH_daily_data_jan2022.csv", index=False)

monthly_data = (SH_daily_data.groupby(["Municipality_name"], as_index=False).sum())

age_per_municipality = pd.read_csv("data/demographic_data/Age_per_municipality.csv").drop(
    labels=["Totaal", "Perioden"], axis=1
)
inhabitants_per_municipality = pd.read_csv("data/demographic_data/Inhabitants_per_municipality.csv").drop(
    labels="2020", axis=1
)
population_density = pd.read_csv("data/demographic_data/Population_density.csv").drop(
    labels="2020", axis=1
)
inhabitants_per_municipality.rename(columns={"2022": "Total"}, inplace=True)
population_density.rename(columns={"2022": "pop_density"}, inplace=True)

monthly_data = monthly_data.merge(age_per_municipality, how="inner", left_on="Municipality_name"
                                  , right_on="Regio's").drop("Regio's", axis=1)
monthly_data = monthly_data.merge(inhabitants_per_municipality, how="inner", left_on="Municipality_name"
                                  , right_on="Municipality").drop("Municipality", axis=1)
monthly_data = monthly_data.merge(population_density, how="inner", left_on="Municipality_name"
                                  , right_on="Municipality").drop("Municipality", axis=1)

continent_of_origin = pd.read_csv("data/demographic_data/Continent_Of_Origin.csv")

continent_of_origin.dropna(inplace=True)

frames = []
for municipality in monthly_data["Municipality_name"].unique():
    data_slice = (continent_of_origin.loc[continent_of_origin["Municipality"] == municipality])

    data_slice = data_slice.drop(labels=["Municipality", "2020"], axis=1).T

    new_header = data_slice.iloc[0]  # grab the first row for the header
    data_slice = data_slice[1:]  # take the data less the header row
    data_slice.columns = new_header  # set the header row as the df header
    data_slice["Region"] = municipality

    frames.append(data_slice)

result = pd.concat(frames)
monthly_data = monthly_data.merge(result, how="inner", left_on="Municipality_name"
                                  , right_on="Region").drop(["Region", "Totaal"], axis=1)

income = pd.read_csv("data/demographic_data/Income.csv").drop("Unnamed: 0", axis=1)

frames = []
for municipality in monthly_data["Municipality_name"].unique():
    data_slice = (income.loc[income["Regionaam"] == municipality])
    frames.append(data_slice)

result = pd.concat(frames)
monthly_data = monthly_data.merge(result, how="inner", left_on="Municipality_name"
                                  , right_on="Regionaam").drop(["Regionaam"], axis=1)


monthly_data["Positive tests per 100000"] = \
    (monthly_data["Total_reported"] / monthly_data["Total"]) * 100000

occupation_data = pd.read_csv("data/demographic_data/Occupation.csv").drop("Perioden", axis=1)

monthly_data = monthly_data.merge(occupation_data, how="inner", left_on="Municipality_name"
                                  , right_on="Gemeente").drop("Gemeente", axis=1)

monthly_data.to_csv("data/cleaned_data/SH_monthly_data_jan2022.csv", index=False)
