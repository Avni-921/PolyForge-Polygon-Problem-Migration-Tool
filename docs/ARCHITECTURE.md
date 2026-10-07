# Architecture Overview

## Data Flow Diagram

```text
User (Browser)
   |
   v
[ Django Web App ] <---(Redis Cache)---> [ Redis ]
   |         |
   |         v
   |    [ Polygon API ] (Fetches Problem & Tests)
   |
   |---> (Structured Data: Name, Tags, Difficulty) ---> [ PostgreSQL DB ]
   |
   |---> (Raw Files: Tests 01, 01.a) ---> [ Storage Abstraction ]
                                                |
                                    +-----------+-----------+
                                    |           |           |
                                [ S3/R2 ]   [ Azure ]   [ Local ]
```

## Roles
- **Polygon**: Source of truth for competitive programming problems.
- **PostgreSQL**: Relational database storing the *structured* data (Problem title, difficulty, tags, and the total count of test cases).
- **Redis**: Caches temporary problem data between the "Fetch" and "Migrate" steps, and acts as a task broker for Celery.
- **Cloud Storage**: Object storage (S3, R2, Azure Blob) holding the *unstructured* raw test case files, which are often too massive to store efficiently in a SQL database.

## Saving to DB vs Uploading to Storage
- **Saving to DB** means recording the metadata (e.g. `Problem ID: 123`, `Test Count: 50`) into PostgreSQL rows so the platform can query and display the problem.
- **Uploading to Storage** means taking the actual multi-megabyte `tests/01` input files and uploading them to a scalable cloud bucket so the code evaluation sandboxes can download them directly during submissions.
