class TableExtractor:

    def __init__(self, tables):
        self.tables = tables

    def find_financial_tables(self):

        financial_tables = []

        keywords = [
            "revenue",
            "sales",
            "assets",
            "equity",
            "liabilities",
            "income"
        ]

        for table in self.tables:

            table_text = str(table).lower()

            if any(
                keyword in table_text
                for keyword in keywords
            ):
                financial_tables.append(table)

        return financial_tables

    def table_count(self):

        return len(
            self.find_financial_tables()
        )