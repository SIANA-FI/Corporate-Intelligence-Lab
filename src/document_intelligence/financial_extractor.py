import re


class FinancialExtractor:

    def __init__(self, text):
        self.text = text

    def extract_metrics(self):

        metrics = {}

        patterns = {
            "revenue": r"Revenue[s]?\s*[:\-]?\s*([\d\., ]+)",
            "assets": r"Assets\s*[:\-]?\s*([\d\., ]+)",
            "equity": r"Equity\s*[:\-]?\s*([\d\., ]+)",
            "liabilities": r"Liabilities\s*[:\-]?\s*([\d\., ]+)"
        }

        for metric, pattern in patterns.items():

            match = re.search(
                pattern,
                self.text,
                re.IGNORECASE
            )

            metrics[metric] = (
                match.group(1)
                if match
                else None
            )

        return metrics