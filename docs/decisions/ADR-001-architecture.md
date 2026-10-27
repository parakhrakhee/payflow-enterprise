# ADR-001: Initial PayFlow Architecture

## Status
Accepted for the learning project; subject to review.

## Context
PayFlow must demonstrate reliable payment-data ingestion,
validation, duplicate handling, reconciliation, and analytics.

## Decision
Start with a modular Python data pipeline, SQL, and PostgreSQL.
Develop and test locally before introducing cloud services.

Introduce Docker Compose for reproducible local dependencies.
Add Airflow when the pipeline can be run and tested independently.
Add AWS S3 and PySpark when their capabilities are justified.

## Alternatives considered

### Local Python and SQL pipeline
Advantages:
- Simple to debug.
- Low cost.
- Fast feedback during development.

Tradeoffs:
- Does not initially demonstrate distributed processing.
- Requires later work to model cloud deployment.

### Cloud-first distributed architecture
Advantages:
- Closer to a deployed enterprise data platform.
- Can demonstrate managed cloud services.

Tradeoffs:
- More configuration and operational complexity.
- Can incur cloud costs before the core logic is correct.

## Consequences
- Establish data contracts and quality checks first.
- Make ingestion idempotent so reruns do not create duplicates.
- Preserve invalid records for investigation.
- Test reconciliation and recovery.
- Document each technology decision.

## Success criteria
- Local ingestion runs reproducibly.
- Duplicate records are handled correctly.
- Invalid records are identified and reported.
- Reconciliation discrepancies can be detected.
- Automated tests verify expected behavior.
