import pandas as pd

# ==========================
# Chargement des données
# ==========================

ownership_df = pd.read_csv(
    "data/ownership.csv"
)

# ==========================
# Construction du graphe inverse
# ==========================

parent_map = {}

for _, row in ownership_df.iterrows():

    parent_map[row["Subsidiary"]] = (
        row["Parent"],
        row["Ownership"]
    )

# ==========================
# Recherche UBO
# ==========================

def find_ubo(entity):

    chain = [entity]

    current_entity = entity

    economic_interest = 100

    while current_entity in parent_map:

        parent, ownership = parent_map[current_entity]

        chain.append(parent)

        economic_interest = (
            economic_interest
            * ownership
            / 100
        )

        current_entity = parent

    chain.reverse()

    return (
        current_entity,
        chain,
        economic_interest
    )

# ==========================
# Interface utilisateur
# ==========================

print("\n")
print("=" * 60)
print("UBO DETECTOR")
print("=" * 60)

entity = input(
    "\nEnter company name : "
)

print("\n")

if entity not in set(
    ownership_df["Subsidiary"]
):

    print(
        f"{entity} not found "
        f"in ownership database."
    )

else:

    ubo, chain, interest = find_ubo(
        entity
    )

    print("=" * 60)
    print("ULTIMATE BENEFICIAL OWNER")
    print("=" * 60)

    print(
        f"\nEntity : {entity}"
    )

    print(
        f"\nUltimate Owner : {ubo}"
    )

    print(
        f"\nEconomic Interest : "
        f"{interest:.2f}%"
    )

    print(
        "\nControl Chain :"
    )

    for company in chain:

        print(company)

        if company != chain[-1]:
            print("↓")