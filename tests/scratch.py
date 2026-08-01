from mts_fiscal_intelligence.tools.fiscaldata import FiscalDataQuery, query_fiscaldata

if __name__ == "__main__":
    query = FiscalDataQuery(
        dataset="reciepts_summary",
        filters={
            "record_date:gte": "2026-05-01",
            "record_date:lte": "2026-06-30",
        },
        page_size=10,
    )

    result = query_fiscaldata(query)

    print(result.model_dump_json(indent=2))