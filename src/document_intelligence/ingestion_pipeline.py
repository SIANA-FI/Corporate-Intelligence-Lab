from .xlsx_parser import XLSXParser
from .validation_engine import ValidationEngine


class IngestionPipeline:

    def __init__(self, file_path):
        self.file_path = file_path
        self.parser = XLSXParser(file_path)

    def run(self):

        sheets = self.parser.get_sheet_names()

        first_sheet = sheets[0]

        dataframe = self.parser.load_sheet(
            first_sheet
        )

        companies = self.parser.extract_companies(
            dataframe
        )

        years = self.parser.extract_years(
            dataframe
        )

        columns_validation = (
            ValidationEngine.validate_columns(
                dataframe
            )
        )

        revenue_validation = (
            ValidationEngine.validate_revenue(
                dataframe
            )
        )

        return {
            "status": "PASS",
            "sheet_count": len(sheets),
            "companies": companies,
            "years": years,
            "column_validation": columns_validation,
            "revenue_validation": revenue_validation
        }