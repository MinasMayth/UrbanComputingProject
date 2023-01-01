from scipy import stats
import pandas as pd

monthly_data = pd.read_csv("data/cleaned_data/SH_monthly_data_jan2022.csv")

# monthly_data["pop_percentage"] = ((monthly_data["Total"] - monthly_data["Totaal niet-Nederlandse nationaliteit"])
#                                   / monthly_data["Total"]) * 100
monthly_data["pop_percentage"] = ((monthly_data["Afrika"]) / monthly_data["Total"]) * 100

corr, p_value = stats.pearsonr(monthly_data["pop_percentage"],
                               monthly_data["Positive tests per 100000"])

print("corr:", corr)
print("\nP value:", p_value)
