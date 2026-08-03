# MTS Fiscal Intelligence Agent
#### Experimental agentic MTS Data Intelligence pipeline

```
Ask an MTS Question:
> What was the year-to-date current month gross receipts amount from the June 2026 Monthly Treasury Statement?

Answer:

From FiscalData, the year-to-date current month gross receipts for June 2026 equals $9,386,026,100,356.27.

Source: FiscalData API, Monthly Treasury Statement Table 1, record_date 2026-06-30.

Tool Trace:
- Step 1: query_fiscaldata [OK]
 Retrieved 3064 rows.
- Step 2: query_fiscaldata [Failed]
 Unexpected error in tool execution, query_fiscaldata: Filter keys must use 'field:operator'. e.g. 'record_date:gte'
- Step 3: query_fiscaldata [OK]
 Retrieved 1 rows.
```

A lightweight, llm-powered, retrieval and tool-calling system focusing on Monthly Treasury Statement data from Fiscaldata.Treasury.gov.

## About

MTS Fiscal Intelligence Agent is a weekend project I started to familiarize myself with building reasoning architecture in Python. The application answers questions using two primary Treasury Data sources:

- Structured MTS data from the Fiscaldata API
- Narrative Economic context released in the Treasury Bulletin

## Current Capabilities

- Query selected MTS data, making use of filter, sort, and select fields
- Search Treasury Bulletin documents via local embeddings
- Autonomously choose between structured data and document search based on the question
- Tool call argument validation
- Produce a final answer with tool trace and source location

## Setup

To run the project locally, follow these steps:

### Prerequisites

- Python 3.12
- uv
- OpenAI API Key

### Installation

1. Clone the repo
```sh
git clone https://github.com/mateoroman1/mts-fiscal-intelligence.git
```
2. Set up virtual environment
```sh
uv sync
```
3. Create .env and configure API key and model
```
OPENAI_API_KEY=replace-me
LLM_MODEL=gpt-5-mini
MAX_AGENT_STEPS=8
```
4. Run
```sh
uv run src\mts_fiscal_intelligence\app.py
```

## Useage

