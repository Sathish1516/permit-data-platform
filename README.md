# US Building Permits Data Pipeline

End-to-end data engineering pipeline that ingests public building permit data, validates records, applies incremental transformations, and produces analytics-ready datasets.

This project demonstrates production-style ETL architecture including raw ingestion, data validation, incremental processing, and aggregation layers.


## Architecture

The pipeline follows a modern medallion architecture:

Raw Layer (Bronze)
- Stores original JSON payloads from source API.
- Ensures data traceability and auditability.

Staging Layer (Silver)
- Extracts structured fields from raw JSON.
- Applies validation rules.
- Rejects invalid records into audit table.
- Implements idempotent and incremental processing.

Analytics Layer (Gold)
- Aggregates cleaned data into business-ready summary tables.
- Example: Monthly permits per borough.

Pipeline supports:
- Incremental loading via checkpoint tracking
- Idempotent transformations
- Data validation with rejection handling
- Backfill capability



## Pipeline Flow Diagram
```text
                ┌──────────────────────────┐
                │   Source API (NYC Data)  │
                └─────────────┬────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Ingestion Layer │
                    │  fetch_raw.py    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Raw Layer      │
                    │ raw_permits      │
                    │ (JSONB storage)  │
                    └────────┬─────────┘
                             │
                    Validation & Cleaning
                             │
                             ▼
                    ┌──────────────────┐
                    │  Staging Layer   │
                    │ staging_permits  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Rejected Layer  │
                    │ rejected_permits │
                    └──────────────────┘

                             │
                             ▼
                    ┌──────────────────┐
                    │  Gold Layer      │
                    │ monthly_summary  │
                    └──────────────────┘
```


## Tech Stack

- Python 3
- PostgreSQL (JSONB storage)
- psycopg2
- Incremental checkpoint processing
- Idempotent upsert logic
- SQL aggregation



## Data Model

### Tables

**raw_permits**
- id
- fetched_at
- raw_data (JSONB)
- source_file

**staging_permits**
- permit_id
- issue_date
- borough
- job_type
- building_type
- work_type
- zip_code
- latitude
- neighborhood
- raw_id (FK)

**rejected_permits**
- raw_id
- reason
- raw_data
- rejected_at

**permits_monthly_summary**
- borough
- year
- month
- permit_count


## Features

- Configurable ingestion via environment variables
- Structured logging
- PostgreSQL JSONB raw storage
- Incremental processing using checkpoint table
- Idempotent upsert logic
- Multi-format date parsing
- Data quality validation rules
- Reject handling and audit trail
- Aggregation layer for analytics consumption


## How to Run

1. Create PostgreSQL database:
   CREATE DATABASE permits_db;

2. Install dependencies:
   pip install -r requirements.txt

3. Run ingestion:
   python -m src.ingestion.fetch_raw

4. Load raw to database:
   python -m src.ingestion.load_to_db

5. Run transformation:
   python -m src.transform.clean_permits

6. Build analytics summary:
   python -m src.analytics.build_monthly_summary


## Engineering Concepts Demonstrated

- ETL pipeline design
- Data warehouse layering (Bronze/Silver/Gold)
- Incremental data processing
- Idempotent data transformations
- Data validation and rejection patterns
- Checkpoint-based recovery
- Backfill workflows
- SQL aggregation modeling

## Running with Docker

This project supports running the entire data pipeline using Docker.

### Start the containers

```bash
docker compose up --build