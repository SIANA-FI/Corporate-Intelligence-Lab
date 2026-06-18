import pandas as pd

ownership_df = pd.read_csv("data/ownership.csv")

ownership_map = {}

for _, row in ownership_df.iterrows():

    parent = row["Parent"]
    child = row["Subsidiary"]
    pct = row["Ownership"]

    ownership_map.setdefault(parent, [])
    ownership_map[parent].append(
        (child, pct)
    )

all_parents = set(ownership_df["Parent"])
all_children = set(ownership_df["Subsidiary"])

ultimate_parents = all_parents - all_children


def print_tree(company, level=0):

    if company not in ownership_map:
        return

    for child, pct in ownership_map[company]:

        print(
            "    " * level
            + f"├── {child} ({pct}%)"
        )

        print_tree(
            child,
            level + 1
        )


print("\n")
print("=" * 60)
print("OWNERSHIP TREE")
print("=" * 60)

for parent in ultimate_parents:

    print(f"\n{parent}")

    print_tree(parent)