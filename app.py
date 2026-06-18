import streamlit as st
import pandas as pd

# ============================================================
# Configuration
# ============================================================

st.set_page_config(
    page_title="Corporate Intelligence Lab",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# Data Loading
# ============================================================

score_df = pd.read_excel(
    "outputs/corporate_score.xlsx"
)

ownership_df = pd.read_csv(
    "data/ownership.csv"
)

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("Corporate Intelligence Lab")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Financial Analysis",
        "Ownership Analysis",
        "Ownership Graph",
        "UBO Search",
        "Risk Scanner"
    ]
)

# ============================================================
# Financial Analysis
# ============================================================

if page == "Financial Analysis":

    st.title("📈 Financial Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Companies",
        len(score_df)
    )

    col2.metric(
        "Best Score",
        round(score_df["Corporate Score"].max(), 2)
    )

    col3.metric(
        "Average Score",
        round(score_df["Corporate Score"].mean(), 2)
    )

    st.dataframe(
        score_df,
        width="stretch"
    )

    st.subheader("Revenue Trend")

    selected_company = st.selectbox(
        "Choose a company",
        ["LVMH", "Bollore", "AirLiquide"]
    )

    image_path = f"outputs/{selected_company}_revenue.png"

    try:
        st.image(
            image_path,
            width="stretch"
        )
    except Exception:
        st.warning(
            f"Graph not found: {image_path}"
        )

# ============================================================
# Ownership Analysis
# ============================================================

elif page == "Ownership Analysis":

    st.title("🏢 Ownership Analysis")

    st.dataframe(
        ownership_df,
        width="stretch"
    )

# ============================================================
# Ownership Graph
# ============================================================

elif page == "Ownership Graph":

    st.title("🕸️ Ownership Graph")

    st.image(
        "outputs/ownership_graph.png",
        width="stretch"
    )

# ============================================================
# UBO Search
# ============================================================

elif page == "UBO Search":

    st.title("🔎 UBO Search")

    company = st.text_input(
        "Search company"
    )

    if company:

        parent_map = {}

        for _, row in ownership_df.iterrows():
            parent_map[row["Subsidiary"]] = (
                row["Parent"],
                row["Ownership"]
            )

        if company not in parent_map:

            st.error(
                f"{company} not found."
            )

        else:

            chain = [company]
            current = company
            economic_interest = 100

            while current in parent_map:

                parent, ownership = parent_map[current]

                chain.append(parent)

                economic_interest = (
                    economic_interest * ownership / 100
                )

                current = parent

            chain.reverse()

            st.success(
                f"Ultimate Owner : {chain[0]}"
            )

            st.metric(
                "Economic Interest",
                f"{economic_interest:.2f}%"
            )

            st.subheader("Control Chain")

            for entity in chain:
                st.write(entity)

                if entity != chain[-1]:
                    st.write("⬇️")

# ============================================================
# Risk Scanner
# ============================================================

elif page == "Risk Scanner":

    st.title("⚠️ Ownership Risk Scanner")

    for _, row in ownership_df.iterrows():

        st.markdown("---")

        st.subheader(
            f"{row['Parent']} → {row['Subsidiary']}"
        )

        st.write(
            f"Ownership : {row['Ownership']}%"
        )

        st.write(
            f"Country : {row['Country']}"
        )

        st.write(
            f"Sector : {row['Sector']}"
        )

        risks = []

        if row["Ownership"] < 50:
            risks.append("Minority Ownership")

        if row["Ownership"] == 100:
            risks.append("Full Control")

        if row["Country"] != "France":
            risks.append("Foreign Exposure")

        for risk in risks:
            st.warning(risk)
