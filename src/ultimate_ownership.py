import pandas as pd

ownership_df = pd.read_csv(
    "data/ownership.csv"
)

ownership_map = {}

for _, row in ownership_df.iterrows():

    parent = row["Parent"]

    ownership_map.setdefault(
        parent,
        []
    )

    ownership_map[parent].append(
        (
            row["Subsidiary"],
            row["Ownership"]
        )
    )

all_parents = set(
    ownership_df["Parent"]
)

all_children = set(
    ownership_df["Subsidiary"]
)

ultimate_parents = (
    all_parents - all_children
)


def explore(
    company,
    current_pct=100,
    root=None
):

    if root is None:
        root = company

    if company not in ownership_map:

        print(
            f"{root} owns "
            f"{current_pct:.2f}% "
            f"of {company}"
        )

        return

    for child, pct in ownership_map[company]:

        new_pct = (
            current_pct
            * pct
            / 100
        )

        explore(
            child,
            new_pct,
            root
        )


print("\n")
print("=" * 60)
print("ULTIMATE OWNERSHIP")
print("=" * 60)

for parent in ultimate_parents:

    explore(parent)