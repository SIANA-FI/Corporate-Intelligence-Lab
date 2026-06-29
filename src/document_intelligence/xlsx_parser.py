import pandas as pd


class XLSXParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_workbook(self):
        return pd.ExcelFile(self.file_path)

    def get_sheet_names(self):
        workbook = self.load_workbook()
        return workbook.sheet_names

    def load_sheet(self, sheet_name):
        return pd.read_excel(
            self.file_path,
            sheet_name=sheet_name
        )

    def extract_companies(self, dataframe):

        if "Company" not in dataframe.columns:
            return []

        return dataframe["Company"].dropna().unique().tolist()

    def extract_years(self, dataframe):

        if "Year" not in dataframe.columns:
            return []

        return sorted(
            dataframe["Year"].dropna().unique().tolist()
        )
    