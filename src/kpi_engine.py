import pandas as pd

# Lecture Excel
income_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Income_Statement"
)

balance_df = pd.read_excel(
    "data/financial_data.xlsx",
    sheet_name="Balance_Sheet"
)

# Fusion
df = pd.merge(
    income_df,
    balance_df,
    on=["Company", "Year"]
)

results = []

for _, company in df.iterrows():

    revenue = company["Revenue"]
    net_income = company["Net_Income"]
    equity = company["Equity"]
    assets = company["Assets"]
    debt = company["Debt"]

    roe = (net_income / equity) * 100
    roa = (net_income / assets) * 100
    net_margin = (net_income / revenue) * 100
    debt_to_equity = debt / equity

    score = 0

    # ROE
    if roe > 20:
        score += 25
    elif roe > 15:
        score += 20
    elif roe > 10:
        score += 15

    # ROA
    if roa > 10:
        score += 25
    elif roa > 5:
        score += 20
    elif roa > 2:
        score += 15

    # Marge nette
    if net_margin > 15:
        score += 25
    elif net_margin > 10:
        score += 20
    elif net_margin > 5:
        score += 15

    # Dette
    if debt_to_equity < 0.5:
        score += 25
    elif debt_to_equity < 1:
        score += 20
    elif debt_to_equity < 2:
        score += 15

    results.append({
        "Company": company["Company"],
        "ROE": round(roe, 2),
        "ROA": round(roa, 2),
        "Net Margin": round(net_margin, 2),
        "Debt/Equity": round(debt_to_equity, 2),
        "Score": score
    })

# Création DataFrame
results_df = pd.DataFrame(results)

# Classement
results_df = results_df.sort_values(
    by="Score",
    ascending=False
)

# Export Excel
results_df.to_excel(
    "outputs/financial_score.xlsx",
    index=False
)

print("\n===== CLASSEMENT FINANCIER =====\n")
print(results_df)

print(
    "\nRapport exporté dans : outputs/financial_score.xlsx"
)