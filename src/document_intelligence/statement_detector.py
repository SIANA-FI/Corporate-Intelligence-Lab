class StatementDetector:

    def __init__(self, text):
        self.text = text.lower()

    def detect(self):

        return {
            "income_statement": (
                "income statement" in self.text
                or "statement of income" in self.text
                or "profit and loss" in self.text
            ),

            "balance_sheet": (
                "balance sheet" in self.text
                or "statement of financial position" in self.text
            ),

            "cash_flow_statement": (
                "cash flow statement" in self.text
                or "statement of cash flows" in self.text
            )
        }