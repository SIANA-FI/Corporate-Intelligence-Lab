import re


class FinancialExtractor:

    def __init__(self, text):
        self.text = text

    def _clean_value(self, value):

        if not value:
            return None

        numbers = re.findall(
            r"\d{1,3}(?:,\d{3})*(?:\.\d+)?",
            value
        )

        cleaned = []

        for number in numbers:

            try:
                numeric_value = float(
                    number.replace(",", "")
                )

                if numeric_value > 1000:
                    cleaned.append(number)

            except ValueError:
                pass

        return cleaned

    def extract_metrics(self):

        metrics = {
            "revenue": None,
            "assets": None,
            "equity": None,
            "liabilities": None
        }

        patterns = {
            "revenue": [
                r"revenue[^\n]{0,120}?([\d,\.\s]{8,})",
                r"sales[^\n]{0,120}?([\d,\.\s]{8,})",
                r"net sales[^\n]{0,120}?([\d,\.\s]{8,})"
            ],

            "assets": [
                r"total assets[^\n]{0,120}?([\d,\.\s]{8,})",
                r"assets \(in millions[^\n]{0,500}?total assets[^\n]{0,120}?([\d,\.\s]{8,})",
                r"assets[^\n]{0,120}?([\d,\.\s]{8,})"
            ],

            "equity": [
                r"total equity[^\n]{0,120}?([\d,\.\s]{8,})",
                r"equity attributable[^\n]{0,120}?([\d,\.\s]{8,})",
                r"equity[^\n]{0,120}?([\d,\.\s]{8,})"
            ],

            "liabilities": [
                r"total liabilities[^\n]{0,120}?([\d,\.\s]{8,})",
                r"total liabilities and equity[^\n]{0,120}?([\d,\.\s]{8,})",
                r"non-current liabilities[^\n]{0,120}?([\d,\.\s]{8,})",
                r"current liabilities[^\n]{0,120}?([\d,\.\s]{8,})",
                r"liabilities[^\n]{0,120}?([\d,\.\s]{8,})"
            ]
        }

        for metric, regex_list in patterns.items():

            for pattern in regex_list:

                match = re.search(
                    pattern,
                    self.text,
                    re.IGNORECASE
                )

                if match:

                    values = self._clean_value(
                        match.group(1)
                    )

                    if values:

                        if len(values) >= 2:

                            metrics[metric] = {
                                "2023": float(
                                    values[-2].replace(",", "")
                                ),
                                "2024": float(
                                    values[-1].replace(",", "")
                                )
                            }

                        else:

                            metrics[metric] = {
                                "2024": float(
                                    values[0].replace(",", "")
                                )
                            }

                        break

        if (
            metrics.get("assets")
            and metrics.get("equity")
            and not metrics.get("liabilities")
        ):

            try:

                liabilities_2023 = (
                    metrics["assets"]["2023"]
                    - metrics["equity"]["2023"]
                )

                liabilities_2024 = (
                    metrics["assets"]["2024"]
                    - metrics["equity"]["2024"]
                )

                metrics["liabilities"] = {
                    "2023": round(liabilities_2023, 1),
                    "2024": round(liabilities_2024, 1)
                }

            except Exception:
                pass

        return metrics