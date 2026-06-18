import pandas as pd
import matplotlib.pyplot as plt

income_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Income_Statement"
)

for company in income_df["Company"].unique():

    company_data = income_df[
        income_df["Company"] == company
    ].sort_values("Year")

    plt.figure(figsize=(8,4))

    plt.plot(
        company_data["Year"],
        company_data["Revenue"],
        marker="o",
        label="Revenue"
    )

    plt.title(f"Evolution du CA - {company}")
    plt.xlabel("Année")
    plt.ylabel("Chiffre d'affaires")
    plt.legend()

    plt.savefig(
        f"outputs/{company}_revenue.png"
    )

    plt.close()