from src.document_intelligence.pdf_parser import (
    PDFParser
)


def test_pdf_import():

    parser = PDFParser(
        "sample_report.pdf"
    )

    assert parser.get_page_count() > 0