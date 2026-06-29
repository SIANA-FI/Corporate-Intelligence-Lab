import pdfplumber


class PDFParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):

        text = ""

        with pdfplumber.open(self.file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    def get_page_count(self):

        with pdfplumber.open(self.file_path) as pdf:
            return len(pdf.pages)

    def extract_tables(self):

        tables = []

        with pdfplumber.open(self.file_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_tables()

                if extracted:
                    tables.extend(extracted)

        return tables

    def extract_tables_from_pages(
        self,
        start_page,
        end_page
    ):

        tables = []

        with pdfplumber.open(self.file_path) as pdf:

            total_pages = len(pdf.pages)

            start_page = max(0, start_page)
            end_page = min(total_pages, end_page)

            for page in pdf.pages[start_page:end_page]:

                extracted = page.extract_tables()

                if extracted:
                    tables.extend(extracted)

        return tables

    def financial_keywords(self):

        text = self.extract_text().lower()

        keywords = {
            "revenue": "revenue" in text,
            "net_income": (
                "net income" in text
                or "net profit" in text
            ),
            "assets": "assets" in text,
            "liabilities": "liabilities" in text,
            "equity": "equity" in text
        }

        return keywords

    def extract_first_pages_text(
        self,
        pages=30
    ):

        text = ""

        with pdfplumber.open(
            self.file_path
        ) as pdf:

            for page in pdf.pages[:pages]:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    def extract_page_range(
        self,
        start_page,
        end_page
    ):

        text = ""

        with pdfplumber.open(self.file_path) as pdf:

            for page in pdf.pages[start_page:end_page]:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text
