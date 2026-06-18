import pandas as pd

ownership_df = pd.read_csv("data/ownership.csv")

print("\n")
print("=" * 60)
print("OWNERSHIP RISK SCANNER")
print("=" * 60)

for _, row in ownership_df.iterrows():

    parent = row["Parent"]
    child = row["Subsidiary"]
    ownership = row["Ownership"]
    country = row["Country"]
    sector = row["Sector"]

    risk_flags = []

    # Contrôle faible

    if ownership < 50:
        risk_flags.append(
            "Minority Ownership"
        )

    # Contrôle partiel

    if ownership >= 50 and ownership < 100:
        risk_flags.append(
            "Partial Control"
        )

    # Contrôle total

    if ownership == 100:
        risk_flags.append(
            "Full Control"
        )

    print("\n")
    print(f"{parent} -> {child}")
    print(f"Ownership : {ownership}%")
    print(f"Country   : {country}")
    print(f"Sector    : {sector}")

    print("Risk Flags :")

    for flag in risk_flags:
        print(f" - {flag}")