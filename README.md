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

A lightweight, llm-powered, retrieval and tool-calling system, focusing on Monthly Treasury Statement data available through Fiscaldata.Treasury.gov.

## About

MTS Fiscal Intelligence Agent is a weekend project I started to familiarize myself with building reasoning architecture in Python. The application answers questions using two primary Treasury Data sources:

- Structured MTS data from the Fiscaldata API
- Narrative Economic context released in the Treasury Bulletin

### Project Structure
```
src/mts_fiscal_intelligence/
├── app.py 
├── agent.py 
├── config.py 
├── llm.py 
├── models.py 
├── orchestrator.py 
├── prompts.py
│ 
└── tools/ 
    ├── document_search.py 
    ├── fiscaldata.py 
    └── fiscal_datasets.py 
src/utils/ 
├── document_chunks.py 
├── document_embeddings.py 
└── document_extract.py
```

### Main Modules
- app.py - Runs the application
- agent.py - Manages agent loop
- fiscaldata.py - Fiscaldata API query tool
- document_search.py - Treasury Bulletin search tool

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

## Usage

### Treasury Bulletin (Document Search) Examples

```
Ask an MTS Question:
> What did the June 2026 Treasury Bulletin say about Labor market conditions?
```

```
Answer:

Statements found in the June 2026 Treasury Bulletin (Profile of the Economy, "Labor Markets and Wages," p.9):

- "Labor markets have improved in recent months, with job growth picking up thus far in 2026, the unemployment rate ticking lower, and selected measures of labor force participation increasing."

- "Payroll employment growth slowed materially in 2025, in part because of federal government payrolls declining, but growth has picked up so far in 2026, underscoring labor market resilience."

- "Total payroll growth has accelerated sharply thus far in 2026 to an average of 76,000 per month, significantly higher than the 2025 average."

- "The employment report for April showed total payrolls increasing by 115,000, with private sector payrolls advancing by 123,000."

- "Excluding health care and social assistance industries, private industries added an average of 31,000 net jobs per month from January to April."

- "The unemployment rate has trended lower since November and stood at 4.3 percent in April 2026."

- "A broader measure, the underemployment rate ... stood at 8.7 percent in November 2025 but has since pulled back to 8.2 percent as of April 2026."

Tool Trace:
- Step 1: search_documents [OK]
 Found 5 matching sections.
- Step 2: search_documents [OK]
 Found 20 matching sections.
- Step 3: search_documents [OK]
 Found 5 matching sections.
```

```
Ask an MTS Question:
> How did multi-family permits perform in 2026?
```
```
Answer:

Statement found in Treasury Bulletin (June 2026), page 13:
- The Bulletin reports multi-family permits fell an average 5.8 percent per month in Q1 2026.
- The Bulletin reports multi-family permits surged 21.8 percent in April 2026.
- The Bulletin reports multi-family permits rose 9.2 percent over the twelve months through April 2026.

Analyst inference:
- Permits were highly volatile in early 2026.
- The large April gain largely offset the Q1 monthly declines by April.

Do you want the monthly permit series or related multi-family starts data?

Tool Trace:
- Step 1: search_documents [OK]
 Found 10 matching sections.
```

## Roadmap

- [] Add deterministic analysis tool for comparisons
- [] Optimize document chunking and filtering
- [] Add report and chart generation tools
- [] Conversation persistence

## Limitations

This project is experimental, and should not be used as an authoritative source for financial decisions.

Current dataset and document support is limited to:
- MTS Table 1
- MTS Table 2
- Treasury Bulletin

Additionally: 

- Document search is a basic semantic retrieval. Results may exclude relevant data points.
- No deterministic analysis. Requests for comparisons will be handled by the model.
- No persistent conversation state

Treasury Bulletin commentary may provide relevant economic context, but that does not necessarily establish any direct causal explanations for changes in statements. The agent is instructed to distinguish between facts, statements, and inferences it makes.

## Background

I started this project after realizing that, while I was familiar with the core concepts of tool calling and agentic workflows, that I had not built one myself before. I have some experience working with MTS data, as well as having worked on an SDK for the Fiscaldata API in my spare time, which made this a great choice for the project. 

The project is intentionally narrow in its current state for exactly that reason. Its purpose is primarily for me to learn how the pieces connect in a working implementation. However, I do see a genuine use case in a tool like this, and will likely continue work on it as I learn more.