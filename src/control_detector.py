import pandas as pd

ownership_df = pd.read_csv("data/ownership.csv")

ownership_map = {}

for _, row in ownership_df.iterrows():

    parent = row["Parent"]
    child = row["Subsidiary"]

    ownership_map.setdefault(parent, [])
    ownership_map[parent].append(child)


def find_control_chain(company, path=None):

    if path is None:
        path = []

    path.append(company)

    if company not in ownership_map:
        return path

    for child in ownership_map[company]:
        return find_control_chain(child, path)

    return path


print("\n")
print("=" * 50)
print("CONTROL CHAINS")
print("=" * 50)

all_parents = set(ownership_df["Parent"])
all_children = set(ownership_df["Subsidiary"])

ultimate_parents = all_parents - all_children

print("\nUltimate Parents:")
print(ultimate_parents)

for parent in ultimate_parents:

    chain = find_control_chain(parent)

    print(
        " -> ".join(chain)
    )