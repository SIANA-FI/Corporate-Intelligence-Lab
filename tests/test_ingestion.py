from src.document_intelligence.ingestion_pipeline import (
    IngestionPipeline
)


def test_ingestion():

    pipeline = IngestionPipeline(
        "data/financial_data.xlsx"
    )

    results = pipeline.run()

    assert results["status"] == "PASS"
    assert len(results["companies"]) > 0
    assert len(results["years"]) > 0