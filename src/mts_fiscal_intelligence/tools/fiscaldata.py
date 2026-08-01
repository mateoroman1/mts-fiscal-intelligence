from __future__ import annotations
from mts_fiscal_intelligence.models import AppModel, SourceReference, ToolResult, Field
from typing import Literal, Any
import httpx
from datetime import date

BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

DATASETS: dict[str, dict[str, str]] = {
    "reciepts_summary": {
        "endpoint": "/v1/accounting/mts/mts_table_1",
        "title": "Summary of Receipts, Outlays, and the Deficit/Surplus of the U.S. Government"
    },
    "budget_results_summary": {
        "endpoint": "/v1/accounting/mts/mts_table_2",
        "title": "Summary of Budget and Off-Budget Results and Financing of the U.S. Government"
    }
}

class FiscalDataQuery(AppModel):
    dataset: Literal[
        "reciepts_summary",
        "budget_results_summary"
        ]
    filters: dict[str, str] = Field(default_factory=dict)
    fields: list[str] = Field(default_factory=list)
    sort: list[str] = Field(default_factory=list)
    start_date: date | None = None
    end_date: date | None = None
    page_size: int = Field(default=100, ge=1, le=10_000)

def get_dataset_config(dataset: str) -> dict[str, str]:

    try:
        return DATASETS[dataset]
    except KeyError as e:
        supported_datasets = ", ".join(DATASETS)
        raise ValueError(
            f"Unsupported dataset: {dataset}"
            f"Not found in available datasets: {supported_datasets}"
        ) from e

def serialize_filters(filters) -> str | None:

    if not filters:
        return None

    serialized_filters: list[str] = []

    for field_and_operator, value in filters.items():
        try:
            field, operator = field_and_operator.rsplit(":", maxsplit=1)
        except ValueError as e:
            raise ValueError("Filter keys must use 'field:operator'. e.g. 'record_date:gte'") from e

        serialized_filters.append(f"{field}:{operator}:{value}")

    return ",".join(serialized_filters)

def build_query_params(query, *, page_number = 1) -> dict[str, str | int]:

    params = {
        "format": "json",
        "page[number]": page_number,
        "page[size]": query.page_size
    }

    if query.fields:
        params["fields"] = ",".join(query.fields)

    if query.sort:
        params["sort"] = ",".join(query.sort)

    serialized_filters = serialize_filters(query.filters)

    if serialized_filters is not None:
        params["filter"] = serialized_filters

    return params

def get_total_pages(meta) -> int:

    total_pages = meta.get("total-pages")

    if total_pages is None:
        return 1
    parsed = int(total_pages)
    return max(parsed, 1)

def query_fiscaldata(query, *, client: httpx.Client | None = None) -> ToolResult:

    dataset_config = get_dataset_config(query.dataset)
    url = f"{BASE_URL}{dataset_config['endpoint']}"
    params = build_query_params(query)

    owns_client = client is None

    if client is None:
        client = httpx.Client(
            timeout=httpx.Timeout(15.0),
            follow_redirects=True
        )

    try:
        response = client.get(url, params=params)
        response.raise_for_status()

        payload = response.json()

    except httpx.TimeoutException:
        return ToolResult(
            success=False,
            error="The Fiscaldata request timed out.",
            data={
                "dataset": query.dataset,
                "url": url
            }
        )
    except httpx.HTTPStatusError as e:
        return ToolResult(
            success=False,
            error=f"Fiscaldata returned HTTP {e.response.status_code}",
            data={
                "dataset": query.dataset,
                "url": url,
                "response": e.response.text
            }
        )
    except httpx.RequestError as e:
        return ToolResult(
            success=False,
            error=f"FiscalData request failed: {e}",
            data={
                "dataset": query.dataset,
                "url": url,
            },
        )

    except ValueError as e:
        return ToolResult(
            success=False,
            error=f"FiscalData returned invalid JSON: {e}",
            data={
                "dataset": query.dataset,
                "url": str(response.request.url),
            },
        )
    
    finally:
        if owns_client:
            client.close()

    # Probably want to define a model for records at some point
    records = payload.get("data")
    metadata = payload.get("meta")
    page_count = get_total_pages(metadata)

    if not isinstance(records, list):
        return ToolResult(
            success=False,
            error=("Response data was malformed"),
            data = {
                "dataset": query.dataset,
                "response_keys": list(payload)
            }
        )

    return ToolResult(
        success=True,
        data = {
            "dataset": query.dataset,
            "records": records,
            "record_count": int(metadata.get("total-count", 0)),
            "meta": metadata
        },
        sources=[
            SourceReference(
                title = dataset_config["title"],
                url = str(response.request.url)
            )
        ]
    )