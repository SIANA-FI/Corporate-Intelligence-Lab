import pandas as pd

ownership_df = pd.read_csv(
    "data/ownership.csv"
)

print("\n")
print("=" * 60)
print("OWNERSHIP STRUCTURE")
print("=" * 60)

for parent in ownership_df["Parent"].unique():

    print("\n")
    print(parent)

    subsidiaries = ownership_df[
        ownership_df["Parent"] == parent
    ]

    for _, row in subsidiaries.iterrows():

        print(
            f"├── {row['Subsidiary']} "
            f"({row['Ownership']}%)"
        )