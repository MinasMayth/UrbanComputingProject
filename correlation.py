from scipy import stats
import pandas as pd

monthly_data = pd.read_csv("data/cleaned_data/SH_monthly_data_dec2020.csv")

#######Country of Origin
# monthly_data["pop_percentage"] = ((monthly_data["Total"] - monthly_data["Totaal niet-Nederlandse nationaliteit"])
#                                   / monthly_data["Total"]) * 100
# monthly_data["pop_percentage"] = ((monthly_data["Azië"]) / monthly_data["Total"]) * 100

#######POP Density
# monthly_data["pop_percentage"] = monthly_data["pop_density"]

#######Income
monthly_data["pop_percentage"] = monthly_data["Avg personal income per inhabitant"]

#######Occupation
monthly_data["pop_percentage"] = (monthly_data["Non-commercial service"] * 1000) / monthly_data["Total"]


corr, p_value = stats.pearsonr(monthly_data["pop_percentage"],
                               monthly_data["Positive tests per 100000"])

print("corr:", corr)
print("\nP value:", p_value)
