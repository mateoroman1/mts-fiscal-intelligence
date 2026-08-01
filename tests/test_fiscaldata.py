import pytest
import httpx
from mts_fiscal_intelligence.tools.fiscaldata import FiscalDataQuery, build_query_params, get_dataset_config, serialize_filters, query_fiscaldata

def test_serialize_filters() -> None:
    filters = {
        "record_date:gte": "2026-05-01",
        "record_date:lte": "2026-06-30",
    }

    result = serialize_filters(filters)

    assert result == (
        "record_date:gte:2026-05-01,"
        "record_date:lte:2026-06-30"
    )

def test_serialize_empty_filters() -> None:
    assert serialize_filters({}) is None

def test_filter_requires_operator() -> None:
    with pytest.raises(ValueError):
        serialize_filters(
            {"record_date": "2026-06-30"}
        )

def test_build_query_params() -> None:
    query = FiscalDataQuery(
        dataset="budget_results_summary",
        filters={
            "record_date:gte": "2026-05-01",
        },
        fields=[
            "record_date",
            "current_month_gross_rcpt_amt",
        ],
        sort=["record_date"],
        page_size=50,
    )

    params = build_query_params(
        query,
        page_number=2,
    )

    assert params == {
        "format": "json",
        "page[number]": 2,
        "page[size]": 50,
        "fields": (
            "record_date,"
            "current_month_gross_rcpt_amt"
        ),
        "sort": "record_date",
        "filter": "record_date:gte:2026-05-01",
    }

def test_unknown_dataset_fails() -> None:
    with pytest.raises(ValueError):
        get_dataset_config("foo")

def test_query_fiscaldata_success() -> None:
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        assert request.url.params["page[size]"] == "100"
        assert request.url.params["format"] == "json"

        return httpx.Response(
            status_code=200,
            json={
                "data": [
                    {
                        "record_date": "2026-06-30",
                        "current_month_gross_rcpt_amt": "500000",
                    }
                ],
                "meta": {
                    "count": 1,
                },
            },
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(
        transport=transport,
    ) as client:
        result = query_fiscaldata(
            FiscalDataQuery(
                dataset="budget_results_summary",
            ),
            client=client,
        )

    assert result.success is True
    assert result.error is None
    assert result.data["record_count"] == 1
    assert len(result.sources) == 1

def test_query_fiscaldata_http_error() -> None:
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=400,
            json={
                "error": "invalid field",
            },
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(
        transport=transport,
    ) as client:
        result = query_fiscaldata(
            FiscalDataQuery(
                dataset="budget_results_summary",
            ),
            client=client,
        )

    assert result.success is False
    assert "HTTP 400" in result.error

def test_query_fiscaldata_rejects_bad_shape() -> None:
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={
                "data": "this should be a list",
            },
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(
        transport=transport,
    ) as client:
        result = query_fiscaldata(
            FiscalDataQuery(
                dataset="budget_results_summary",
            ),
            client=client,
        )

    assert result.success is False
    assert "data was malformed" in result.error