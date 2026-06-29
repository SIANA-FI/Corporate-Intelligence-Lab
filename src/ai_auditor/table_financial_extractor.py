import re


class TableFinancialExtractor:

    def extract(self, tables):

        metrics = {
            "revenue": {},
            "assets": {},
            "equity": {},
            "liabilities": {}
        }

        best_scores = {
            "revenue": -1,
            "assets": -1,
            "equity": -1,
            "liabilities": -1
        }

        for table in tables:

            for row in table:

                cleaned_row = [
                    str(cell).strip()
                    if cell is not None
                    else ""
                    for cell in row
                ]

                row_text = " ".join(
                    cleaned_row
                ).lower()

                values = []

                for cell in cleaned_row:

                    cell = (
                        str(cell)
                        .replace(",", "")
                        .replace(" ", "")
                    )

                    if re.match(
                        r"^\d+(\.\d+)?$",
                        cell
                    ):
                        try:
                            values.append(
                                float(cell)
                            )
                        except Exception:
                            pass

                if len(values) < 2:
                    continue

                # =====================
                # Revenue
                # =====================

                revenue_score = 0

                if "revenue" in row_text:
                    revenue_score += 5

                if "net sales" in row_text:
                    revenue_score += 5

                if revenue_score > best_scores["revenue"]:

                    metrics["revenue"] = {
                        "2023": values[-2],
                        "2024": values[-1]
                    }

                    best_scores["revenue"] = revenue_score

                # =====================
                # Assets
                # =====================

                assets_score = 0

                if "total assets" in row_text:
                    assets_score += 20

                elif (
                    "assets" in row_text
                    and "total" in row_text
                ):
                    assets_score += 15

                elif row_text.startswith("assets"):
                    assets_score += 5

                if assets_score > best_scores["assets"]:

                    metrics["assets"] = {
                        "2023": values[-2],
                        "2024": values[-1]
                    }

                    best_scores["assets"] = assets_score

                # =====================
                # Equity
                # =====================

                equity_score = 0

                if "total equity" in row_text:
                    equity_score += 20

                if (
                    "total shareholders"
                    in row_text
                ):
                    equity_score += 20

                elif (
                    "equity"
                    in row_text
                    and "total" in row_text
                ):
                    equity_score += 15

                elif (
                    "equity attributable"
                    in row_text
                ):
                    equity_score -= 10

                if equity_score > best_scores["equity"]:

                    metrics["equity"] = {
                        "2023": values[-2],
                        "2024": values[-1]
                    }

                    best_scores["equity"] = equity_score

                # =====================
                # Liabilities
                # =====================

                liabilities_score = 0

                if "total liabilities" in row_text:
                    liabilities_score += 20

                elif (
                    "liabilities"
                    in row_text
                    and "total" in row_text
                ):
                    liabilities_score += 15

                elif (
                    "current liabilities"
                    in row_text
                ):
                    liabilities_score -= 10

                if (
                    liabilities_score
                    > best_scores["liabilities"]
                ):

                    metrics["liabilities"] = {
                        "2023": values[-2],
                        "2024": values[-1]
                    }

                    best_scores["liabilities"] = liabilities_score

        return metrics
    