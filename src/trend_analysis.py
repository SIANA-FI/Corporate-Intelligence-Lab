import pandas as pd

income_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Income_Statement"
)

for company in income_df["Company"].unique():

    company_data = income_df[
        income_df["Company"] == company
    ].sort_values("Year")

    revenue_growth = (
        company_data["Revenue"].pct_change() * 100
    )

    income_growth = (
        company_data["Net_Income"].pct_change() * 100
    )

    print("\n")
    print("=" * 40)
    print(company)
    print("=" * 40)

    print(
        f"Croissance CA : {revenue_growth.iloc[-1]:.2f}%"
    )

    print(
        f"Croissance Résultat Net : {income_growth.iloc[-1]:.2f}%"
    )