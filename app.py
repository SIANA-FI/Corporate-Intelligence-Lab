import streamlit as st
import pandas as pd
import plotly.express as px

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

page = st.sidebar.radio(
    "Navigation",
    [
        "Financial Analysis",
        "Document Intelligence",
        "Company Profile",
        "Ownership Analysis",
        "Ownership Graph",
        "UBO Search",
        "Risk Engine",
        "Risk Scanner",
        "Analyst Conclusion",
        "Analyst Report"
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

    st.markdown("---")

    st.header("🎯 Executive Summary")

    best_company = score_df.loc[
        score_df["Corporate Score"].idxmax()
    ]

    best_growth = score_df.loc[
        score_df["CAGR Revenue"].idxmax()
    ]

    lowest_risk = score_df.loc[
        score_df["Debt/Equity"].idxmin()
    ]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success(
            f"🏆 MARKET LEADER\n\n{best_company['Company']}\n\n{best_company['Corporate Score']:.2f}"
        )

    with c2:
        st.info(
            f"📈 FASTEST GROWER\n\n{best_growth['Company']}\n\n{best_growth['CAGR Revenue']:.2f}%"
        )

    with c3:
        st.warning(
            f"🛡️ LOWEST RISK\n\n{lowest_risk['Company']}\n\n{lowest_risk['Debt/Equity']:.2f}"
        )

    st.markdown("---")

    st.subheader("🏆 Ranking")

    ranking = score_df.sort_values(
        by="Corporate Score",
        ascending=False
    )

    medals = ["🥇", "🥈", "🥉"]

    for i in range(min(3, len(ranking))):
        st.write(
            f"{medals[i]} {ranking.iloc[i]['Company']} ({ranking.iloc[i]['Corporate Score']:.2f})"
        )


    st.subheader("📊 Corporate Score Ranking")

    fig_ranking = px.bar(
        ranking,
        x="Company",
        y="Corporate Score",
        title="Corporate Score Ranking"
    )

    fig_ranking.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_ranking,
        use_container_width=True
    )

    st.subheader("📈 Revenue Trend")

    selected_company = st.selectbox(
        "Choose a company",
        score_df["Company"].tolist()
    )

    financial_df = pd.read_excel(
        "data/financial_data.xlsx",
        sheet_name="Income_Statement"
    )

    company_df = financial_df[
        financial_df["Company"] == selected_company
    ].sort_values("Year")

    fig = px.line(
        company_df,
        x="Year",
        y="Revenue",
        markers=True,
        title=f"Revenue Evolution - {selected_company}"
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# Document Intelligence
# ============================================================
elif page == "Document Intelligence":

    st.title("📂 Document Intelligence")

    uploaded_file = st.file_uploader(
        "Upload Financial File",
        type=["xlsx", "xls", "pdf"]
    )

    if uploaded_file:

        import os

        os.makedirs("uploads", exist_ok=True)

        temp_path = f"uploads/{uploaded_file.name}"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.name.lower().endswith(".pdf"):

            from src.document_intelligence.pdf_parser import PDFParser

            parser = PDFParser(temp_path)

            st.success("PDF successfully analyzed")

            c1, c2 = st.columns(2)

            c1.metric(
                "Pages",
                parser.get_page_count()
            )

            keywords = parser.financial_keywords()

            detected = sum(
                1 for value in keywords.values()
                if value
            )

            c2.metric(
                "Financial Keywords",
                detected
            )

            st.subheader("Detected Keywords")

            st.json(keywords)

            # ==========================
            # Financial Extractor
            # ==========================

            from src.document_intelligence.financial_extractor import (
                FinancialExtractor
            )

            text = parser.extract_text()

            import re

            match = re.search(
            r"Consolidated Financial Statements\s+(\d+)",
            text,
            re.IGNORECASE
            )

            if match:

            page_ref = int(match.group(1))

            start_page = max(
            page_ref - 5,
            0
            )

            text = parser.extract_first_pages_text(
            pages=437
            )

            else:

            text = parser.extract_first_pages_text(
             pages=437
            )

            lines = text.split("\n")
            financial_start = 0

            for i, line in enumerate(lines):
                lower_line = line.lower()
                if (
                    "financial statements" in lower_line
                    or "consolidated financial statements" in lower_line
                    or "income statement" in lower_line
                    or "balance sheet" in lower_line
                ):
                    financial_start = i
                    break

            text = "\n".join(lines[financial_start:])

            st.subheader(
                "Financial Text Sample"
            )

            st.text_area(
                "Financial Content Preview",
                text[:10000],
                height=400
            )

            extractor = FinancialExtractor(
                text
            )

            metrics = extractor.extract_metrics()

            st.subheader(
                "Extracted Financial Metrics"
            )

            st.json(metrics)

            non_empty_metrics = {
                k: v
                for k, v in metrics.items()
                if v not in [None, "", " ", ",", ", "]
            }

            if non_empty_metrics:
                st.success(
                    f"{len(non_empty_metrics)} financial metrics extracted"
                )
            else:
                st.warning(
                    "No reliable financial metrics found in the extracted text. Financial statements pages should be targeted next."
                )

            from src.document_intelligence.statement_detector import (
                StatementDetector
            )

            detector = StatementDetector(
                text
            )

            statements = detector.detect()

            st.subheader(
                "Detected Financial Statements"
            )

            st.json(statements)

            st.subheader(
                "Financial Statement Detection"
            )

            statement_pages = {}

            lines = text.split("\n")

            for line in lines:

                lower_line = line.lower()

                if (
                    "consolidated financial statements" in lower_line
                    and any(char.isdigit() for char in line)
                ):
                    statement_pages[
                        "Consolidated Financial Statements"
                    ] = line

                if (
                    "income statement" in lower_line
                    and any(char.isdigit() for char in line)
                ):
                    statement_pages[
                        "Income Statement"
                    ] = line

                if (
                    "balance sheet" in lower_line
                    and any(char.isdigit() for char in line)
                ):
                    statement_pages[
                        "Balance Sheet"
                    ] = line

                if (
                    "cash flow" in lower_line
                    and any(char.isdigit() for char in line)
                ):
                    statement_pages[
                        "Cash Flow Statement"
                    ] = line

            if statement_pages:
                st.json(statement_pages)

            # ==========================
            # PDF Intelligence Summary
            # ==========================

            tables = parser.extract_tables()

            valid_tables = []

            for table in tables:
                if table and len(table) > 1:
                    valid_tables.append(table)

            st.subheader(
                "Document Intelligence Summary"
            )

            col_a, col_b = st.columns(2)

            col_a.metric(
                "Tables Detected",
                len(tables)
            )

            col_b.metric(
                "Text Length",
                len(text)
            )

            col_c, col_d = st.columns(2)

            col_c.metric(
                "Valid Tables",
                len(valid_tables)
            )

            col_d.metric(
                "Detected Statements",
                sum(statements.values())
            )

            st.subheader(
                "Text Preview"
            )

            st.text_area(
                "First Extracted Characters",
                text[:5000],
                height=300
            )

            if valid_tables:

                st.subheader(
                    "First Valid Financial Table"
                )

                try:
                    import pandas as pd

                    financial_table = None

                    for table in valid_tables:

                        flat_text = " ".join(
                            str(cell)
                            for row in table
                            for cell in row
                            if cell
                        )

                        score = sum(
                            keyword in flat_text.lower()
                            for keyword in [
                                "revenue",
                                "sales",
                                "assets",
                                "equity",
                                "income",
                                "cash flow",
                                "profit",
                                "liabilities"
                            ]
                        )

                        if score >= 2:
                            financial_table = table
                            break

                    if financial_table is None:
                        financial_table = valid_tables[0]
                    st.caption(
                        f"Financial table selected from {len(valid_tables)} candidate tables"
                    )

                    table_df = pd.DataFrame(financial_table)

                    st.dataframe(
                        table_df,
                        use_container_width=True
                    )

                except Exception as e:
                    st.warning(
                        f"Unable to display table: {e}"
                    )
            else:
                st.info(
                    "No structured financial table could be extracted from the PDF."
                )

        else:

            from src.document_intelligence.ingestion_pipeline import (
                IngestionPipeline
            )

            pipeline = IngestionPipeline(
                temp_path
            )

            results = pipeline.run()

            st.success(
                "Excel successfully analyzed"
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Sheets",
                results["sheet_count"]
            )

            c2.metric(
                "Companies",
                len(results["companies"])
            )

            c3.metric(
                "Years",
                len(results["years"])
            )

            st.json(results)

# ============================================================
# Company Profile
# ============================================================

elif page == "Company Profile":

    st.title("🏢 Company Profile")

    company = st.selectbox(
        "Select Company",
        score_df["Company"].tolist()
    )

    row = score_df[
        score_df["Company"] == company
    ].iloc[0]

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("ROE", f"{row['ROE']}%")
    c2.metric("Net Margin", f"{row['Net Margin']}%")
    c3.metric("Debt/Equity", round(row["Debt/Equity"], 2))
    c4.metric("CAGR Revenue", f"{row['CAGR Revenue']}%")
    c5.metric("Corporate Score", round(row["Corporate Score"], 2))

    st.markdown("---")

# ============================================================
# Ownership Analysis
# ============================================================

elif page == "Ownership Analysis":

    st.title("🏢 Ownership Analysis")

    st.dataframe(
        ownership_df,
        use_container_width=True
    )

# ============================================================
# Ownership Graph
# ============================================================

elif page == "Ownership Graph":

    st.title("🕸️ Ownership Graph")

    try:
        st.image(
            "outputs/ownership_graph.png",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Unable to load ownership graph: {e}")

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
# Risk Engine
# ============================================================

elif page == "Risk Engine":

    st.title("⚡ Risk Engine")

    company = st.selectbox(
        "Select Company",
        score_df["Company"].tolist()
    )

    row = score_df[
        score_df["Company"] == company
    ].iloc[0]

    risk_score = 0

    if row["Debt/Equity"] > 1:
        risk_score += 30

    if row["ROE"] < 10:
        risk_score += 20

    if row["Net Margin"] < 5:
        risk_score += 20

    st.metric("Global Risk Score", risk_score)
    st.progress(min(risk_score, 100) / 100)

    if risk_score <= 40:
        st.success("🟢 LOW RISK")
    elif risk_score <= 70:
        st.warning("🟡 MEDIUM RISK")
    else:
        st.error("🔴 HIGH RISK")

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

# ============================================================
# Analyst Conclusion
# ============================================================

elif page == "Analyst Conclusion":

    st.title("🧠 Analyst Conclusion")

    company = st.selectbox(
        "Select Company",
        score_df["Company"].tolist()
    )

    row = score_df[
        score_df["Company"] == company
    ].iloc[0]

    summary = []

    if row["ROE"] > 20:
        summary.append("Strong profitability")

    if row["Debt/Equity"] < 0.7:
        summary.append("Healthy balance sheet")

    if row["CAGR Revenue"] > 8:
        summary.append("Strong growth")

    st.info("Executive View: " + ", ".join(summary) if summary else "Executive View: Mixed profile")

    st.subheader("💪 Strengths")

    if row["ROE"] > 20:
        st.success("Excellent profitability")

    if row["Debt/Equity"] < 0.7:
        st.success("Low leverage")

    st.subheader("⚠️ Weaknesses")

    if row["ROE"] <= 20:
        st.warning("Moderate profitability")

    st.subheader("🚨 Risks")

    if row["Debt/Equity"] >= 0.7:
        st.error("Debt exposure")

    st.subheader("🚀 Opportunities")

    if row["CAGR Revenue"] > 8:
        st.info("Strong growth profile")

# ============================================================
# Analyst Report
# ============================================================

elif page == "Analyst Report":

    st.title("📄 Analyst Report")

    report_text = score_df.to_csv(index=False)

    st.download_button(
        label="📥 Export Due Diligence Data",
        data=report_text,
        file_name="due_diligence_report.csv",
        mime="text/csv"
    )

    ranking = score_df.sort_values(
        by="Corporate Score",
        ascending=False
    )

    for _, row in ranking.iterrows():

        st.markdown("---")

        st.subheader(row["Company"])

        st.write(f"ROE : {row['ROE']}%")
        st.write(f"Net Margin : {row['Net Margin']}%")
        st.write(f"Debt/Equity : {row['Debt/Equity']}")
        st.write(f"CAGR Revenue : {row['CAGR Revenue']}%")

        if row["ROE"] > 20:
            st.success("Excellent profitability")
        else:
            st.info("Good profitability")

        if row["CAGR Revenue"] > 8:
            st.success("Strong growth profile")
        else:
            st.info("Stable growth profile")

        if row["Debt/Equity"] < 0.7:
            st.success("Low financial risk")
        else:
            st.warning("Moderate financial risk")

        # Corporate Score metric block removed as now shown in main metrics above
