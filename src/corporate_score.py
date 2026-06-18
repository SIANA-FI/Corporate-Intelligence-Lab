import pandas as pd

# ==========================
# Chargement des données
# ==========================

income_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Income_Statement"
)

balance_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Balance_Sheet"
)

# ==========================
# Fusion des données
# ==========================

df = pd.merge(
    income_df,
    balance_df,
    on=["Company", "Year"]
)

# ==========================
# Dernière année disponible
# ==========================

latest_year = df["Year"].max()

df = df[df["Year"] == latest_year]

results = []

# ==========================
# Analyse par entreprise
# ==========================

for _, company in df.iterrows():

    revenue = company["Revenue"]
    net_income = company["Net_Income"]
    equity = company["Equity"]
    debt = company["Debt"]

       # KPI

    roe = (net_income / equity) * 100
    net_margin = (net_income / revenue) * 100
    debt_to_equity = debt / equity

    # CAGR Revenue

    company_history = income_df[
        income_df["Company"] == company["Company"]
    ].sort_values("Year")

    cagr = 0

    if len(company_history) >= 2:

        first_year = company_history.iloc[0]
        last_year = company_history.iloc[-1]

        years = last_year["Year"] - first_year["Year"]

        if years > 0:

            cagr = (
                (
                    last_year["Revenue"]
                    / first_year["Revenue"]
                ) ** (1 / years)
                - 1
            ) * 100

    # ROE
    score_roe = min(max(roe, 0), 30)

    # Marge
    score_margin = min(max(net_margin, 0), 30)

    # Risque
    score_risk = max(
        0,
        40 - (debt_to_equity * 20)
    )

    # Croissance
    score_growth = min(cagr * 2, 20)

    corporate_score = (
        score_roe
        + score_margin
        + score_risk
        + score_growth
    )

    results.append(
        {
            "Company": company["Company"],
            "ROE": round(roe, 2),
            "Net Margin": round(net_margin, 2),
            "Debt/Equity": round(debt_to_equity, 2),
            "CAGR Revenue": round(cagr, 2),
            "Corporate Score": round(corporate_score, 2)
        }
    )

# ==========================
# Classement
# ==========================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Corporate Score",
    ascending=False
)

# ==========================
# Affichage
# ==========================

print("\n")
print("=" * 60)
print("CORPORATE INTELLIGENCE SCORE")
print("=" * 60)

print(results_df)

# ==========================
# Export Excel
# ==========================

results_df.to_excel(
    "outputs/corporate_score.xlsx",
    index=False
)

print("\nRapport exporté dans : outputs/corporate_score.xlsx")