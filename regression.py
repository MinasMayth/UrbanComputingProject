import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


def coefficient_extractor(feature, month):
    if month == "dec":
        monthly_data = pd.read_csv("data/cleaned_data/SH_monthly_data_dec2020.csv").sort_values(
            by=["Municipality_name"])
        daily_data = pd.read_csv("data/cleaned_data/SH_daily_data_dec2020.csv")
        month_string = "2020-12"
    elif month == "jan":
        monthly_data = pd.read_csv("data/cleaned_data/SH_monthly_data_jan2022.csv").sort_values(
            by=["Municipality_name"])
        daily_data = pd.read_csv("data/cleaned_data/SH_daily_data_jan2022.csv")
        month_string = "2022-01"
    elif month == "jul":
        monthly_data = pd.read_csv("data/cleaned_data/SH_monthly_data_july2021.csv").sort_values(
            by=["Municipality_name"])
        daily_data = pd.read_csv("data/cleaned_data/SH_daily_data_july2021.csv")
        month_string = "2021-07"
    else:
        print("INVALID MONTH")
        quit()

    feature_coefficients = []
    # for all days in the month
    for day in range(1, 32):
        # reformatting
        if day < 10:
            day_string = "0" + str(day)
        else:
            day_string = str(day)

        # obtain data for this day
        day_data = (daily_data.loc[daily_data["Date_of_publication"] == month_string + "-" + day_string]).sort_values(
            by=["Municipality_name"])
        y = day_data["Total_reported"]
        y = y.reset_index().drop("index", axis=1)

        # obtain X data
        X = monthly_data["Positive tests per 100000"]
        X = X.rename("X")
        X = X.reset_index().drop("index", axis=1)

        # obtain feature data
        control = monthly_data[feature]
        control = control.rename("control")
        control = control.reset_index().drop("index", axis=1)

        df = pd.concat([y, X, control], axis=1)
        model = smf.ols("Total_reported ~ X + control", data=df)
        results = model.fit()
        feature_coefficients.append(results.params[2])

    return feature_coefficients


month = "dec"
coef1 = coefficient_extractor("Farming Forestry and Fishery", month)
coef2 = coefficient_extractor("Industry and energy", month)
coef3 = coefficient_extractor("Commercial service", month)
coef4 = coefficient_extractor("Non-commercial service", month)
plt.plot(coef1, label="Farming Forestry and Fishery")
plt.plot(coef2, label="5-10 Years")
plt.plot(coef3, label="10-15 Years")
plt.plot(coef4, label="15-20 Years")
plt.legend()
plt.ylim(0, 2)
plt.xlabel("Day - December 2020")
plt.ylabel("Correlation Coefficient")
plt.title("Correlation Coefficients for Ages 0-20")
plt.show()
#plt.savefig("graphs/corr_jan2022.png")
