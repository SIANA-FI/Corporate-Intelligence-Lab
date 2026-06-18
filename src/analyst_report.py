import pandas as pd

# Chargement du score

df = pd.read_excel(
    "outputs/corporate_score.xlsx"
)

print("\n")
print("=" * 60)
print("AUTOMATED ANALYST REPORT")
print("=" * 60)

for _, company in df.iterrows():

    print("\n")
    print("=" * 60)
    print(f"COMPANY : {company['Company']}")
    print("=" * 60)

    print(f"ROE : {company['ROE']}%")
    print(f"Net Margin : {company['Net Margin']}%")
    print(f"Debt/Equity : {company['Debt/Equity']}")
    print(f"CAGR Revenue : {company['CAGR Revenue']}%")

    print("\nAssessment :")

    # Rentabilité

    if company["ROE"] > 20:
        print("- Excellent profitability")
    elif company["ROE"] > 10:
        print("- Good profitability")
    else:
        print("- Weak profitability")

    # Croissance

    if company["CAGR Revenue"] > 8:
        print("- Strong growth profile")
    elif company["CAGR Revenue"] > 5:
        print("- Stable growth profile")
    else:
        print("- Low growth profile")

    # Risque

    if company["Debt/Equity"] < 0.6:
        print("- Low financial risk")
    elif company["Debt/Equity"] < 1:
        print("- Moderate financial risk")
    else:
        print("- Elevated financial risk")

    print(
        f"\nCorporate Score : {company['Corporate Score']}"
    )