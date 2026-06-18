import pandas as pd

income_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Income_Statement"
)

for company in income_df["Company"].unique():

    company_data = (
        income_df[
            income_df["Company"] == company
        ]
        .sort_values("Year")
    )

    first_revenue = company_data.iloc[0]["Revenue"]
    last_revenue = company_data.iloc[-1]["Revenue"]

    years = len(company_data) - 1

    cagr = (
        (last_revenue / first_revenue)
        ** (1 / years)
        - 1
    ) * 100

    print("\n")
    print("=" * 50)
    print(company)
    print("=" * 50)

    print(
        f"CAGR Revenue : {cagr:.2f}%"
    )